from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import *
from django.http import HttpResponseRedirect
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .utils import *
from .forms import *
import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_protect
from geopy.distance import geodesic
from django.db.models import Q
from django.core.paginator import Paginator

# Create your views here.

def index(request):
    if request.user:
        user = request.user
    all_specialties = Specialties.objects.all().order_by('specialty')
    all_languages = Languages.objects.all().order_by('language')
    google_maps_api_key = settings.GOOGLE_MAPS_API_KEY

    context = {
        'all_specialties': all_specialties,
        'all_languages': all_languages,
        'google_maps_api_key': google_maps_api_key,
        'user': user
    }
    return render(request,'core/normal_pages/index.html', context)

def search_results(request):
    if request.user:
        user = request.user
    specialty = request.GET.get('specialtyInput')
    print(f"specialtyy: {specialty}")
    location = request.GET.get('autocomplete')
    range = float(request.GET.get('radius',15))
    min_rating = request.GET.get('avg-rating')
    language = request.GET.get('language')
    keyword= request.GET.get('keyword')

    print(f"languge: {language}")

    all_specialties = Specialties.objects.all().order_by('specialty')
    all_languages = Languages.objects.all().order_by('language')

    
    print(f"range:{range} type: {type(range)}")

    professionals = Professional.objects.all()
    if specialty:
        professionals = professionals.filter(specialties__specialty=specialty)
    if location:
        try:
            search_lat, search_long = nearby_professional_locations(location)
            pros_in_radius = []
            for pro in professionals:
                print(f"pro: {pro.first_name} pro distance: {geodesic((search_lat, search_long), (pro.location_lat, pro.location_long)).km}")
                if geodesic((search_lat, search_long), (pro.location_lat, pro.location_long)).km <= range: #need to fix temp number
                    pros_in_radius.append(pro)
            professionals =professionals.filter(id__in=pros_in_radius)
        except:
            print("location invalid")
        print(f"HELLOrange: {range}")

    if int(min_rating) > 0:
        professionals = professionals.filter(average_rating__gte=min_rating)
    if language:
         professionals = professionals.filter(languages__language=language)
    if keyword:
        split_keyword = keyword.split(" ")
        query = Q()
        for keyword in split_keyword:
            query |= Q(first_name__icontains=keyword) | Q(last_name__icontains=keyword) | Q(
                firm_name__icontains=keyword) | Q(school_studied_at__icontains=keyword) | Q(
                credentials__icontains=keyword) | Q(description__icontains=keyword)
        professionals = professionals.filter(query)
        keyword = " ".join(split_keyword)

    google_maps_api_key = settings.GOOGLE_MAPS_API_KEY


    context = {
        'professionals': professionals,
        'user':user,
        'inputted_specialty': specialty,
        'inputted_location': location,
        'inputted_range': int(range),
        'inputted_min_rating': min_rating,
        'inputted_language': language,
        'inputted_keyword': keyword,
        'all_specialties': all_specialties,
        'all_languages': all_languages,
        'google_maps_api_key': google_maps_api_key,
    }

    return render(request, 'core/normal_pages/search_results.html', context)


def pricing(request):
    if request.user:
        user = request.user
    
    context = {
        'user':user
    }

    return render(request,'core/normal_pages/pricing.html',context)

def support_feedback(request):
    if request.user:
        user = request.user
    
    context = {
        'user':user
    }

    return render(request,'core/normal_pages/support-feedback.html',context)

def about_us(request):
    if request.user:
        user = request.user
    
    context = {
        'user':user
    }
    
    return render(request,'core/normal_pages/about-us.html',context)

def faq(request):
    if request.user:
        user = request.user
    
    context = {
        'user':user
    }
    
    return render(request,'core/normal_pages/faq.html',context)

def features(request):
    if request.user:
        user = request.user
    
    context = {
        'user':user
    }
    
    return render(request,'core/normal_pages/features.html',context)

def professional_page(request, unique_id):
    if request.user:
        user = request.user

    professional = get_object_or_404(Professional, unique_id=unique_id)
    reviews = professional.review_set.all()


    context = {
        'professional': professional,
        'reviews': reviews,
        'user':user
    }

    return render(request, 'core/normal_pages/professional-page.html', context)

def create_review(request):
    if request.method == 'POST':
        reviewer_name = request.POST['inputNameReview']
        reviewer_email = request.POST['inputEmail']
        rating = request.POST['starRating']
        comment = request.POST['inputReview']
        professional_id = request.POST['professional']
        reviewer_ip = get_client_ip(request)
        reviewed_professional = Professional.objects.get(id=professional_id)

        if Review.objects.filter(reviewer_ip=reviewer_ip, reviewed_professional=reviewed_professional).exists() or Review.objects.filter(reviewed_professional=reviewed_professional, reviewer_email=reviewer_email).exists():
            return JsonResponse({'status': 'error', 'message': 'You have already reviewed this professional.'}, status=400)
            
        
        

        new_review = Review(reviewer_name=reviewer_name, reviewer_email=reviewer_email, reviewer_ip=reviewer_ip,
                            rating=rating, comment=comment, reviewed_professional=reviewed_professional)
        new_review.save()

        return JsonResponse({'status': 'success', 'message': 'Review submitted successfully'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
    
def get_reviews(request):
    if request.method == 'GET':
        professional_pk = request.GET.get('professional_pk')
        professional = get_object_or_404(Professional, pk=professional_pk)
        reviews = professional.review_set.order_by('-created_at').values('reviewer_name', 'rating', 'comment', 'created_at')
        
        # Convert queryset to list of dictionaries
        reviews_list = list(reviews)
        
        return JsonResponse({'reviews': reviews_list})
    else:
        return JsonResponse({'error': 'Invalid request method'})
    

