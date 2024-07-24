from django.shortcuts import render, redirect
from .forms import SignupForm
from django.contrib.auth import login, update_session_auth_hash
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
from forum.models import *
from blog.models import *
import random

def signin(request):
    context = None
    if request.user.is_authenticated:
        return redirect('user_overview')
    else:
        if request.method == 'POST':

            if 'form_id' in request.POST:
                form_id = request.POST['form_id']
                print(f"form_submitted: {form_id}")
                if form_id == 'signin':
                    username = request.POST.get('username')
                    password = request.POST.get('password')

                    user = authenticate(request, username=username, password=password)

                    if user is not None:
                        login(request, user)
                        messages.success(request, 'Login Success.')
                        return redirect('user_overview')
                    else:
                        messages.error(request, 'Email or Password is incorrect.')
                elif form_id == 'signup':
                    signup_form = SignupForm(request.POST)
                    if signup_form.is_valid():
                        user = signup_form.save()
                        login(request, user)
                        # Redirect to a success page or login page
                        return redirect('user_edit_profile')

        else:
            signup_form = SignupForm()

            context = {
                'signup_form': signup_form
            }

    return render(request,'accounts/signin.html', context)

@login_required
def user_overview(request):
    user = request.user
    try:
        current_professional = Professional.objects.get(user=user)
        url = f"/professional/{current_professional.unique_id}"
        week_profile_data = users_visited_overview(url)
        week_profile_visits_data_cleaned = [week_profile_data[0][1],week_profile_data[1][1],week_profile_data[2][1],week_profile_data[3][1]]
        curr_pro_topics = current_professional.specialties.all()

        top_questions = ForumQuestion.objects.filter(resolved_status=False)
        top_questions_related = top_questions.filter(topics__in=curr_pro_topics)
        print(f"wa: {top_questions}")
        random_question_related = top_questions_related.order_by('?').first()


        context = {
            'user': user,
            'week_profile_visits_data_cleaned': week_profile_visits_data_cleaned,
            'random_question_related': random_question_related
        }
    except:
        return redirect('user_edit_profile')

    return render(request, 'accounts/user-overview.html', context)

@login_required
def user_analytics(request):
    user = request.user
    current_professional = Professional.objects.get(user=user)
    num_of_reviews = Review.objects.filter(reviewed_professional=current_professional).count()
    url = f"/professional/{current_professional.unique_id}"

    #visited_users = users_visited(url)
    #top5_cities_arr = top5_cities(url)

    context = {
        'user':user,
        'current_professional': current_professional,
        'num_of_reviews': num_of_reviews,
        #'visited_users':visited_users,
        #'top5_cities_arr':top5_cities_arr,
        'url': url
    }
    return render(request, 'accounts/user-analytics.html', context)

@csrf_exempt
def api_overview_analytics(request):
    user = request.user
    current_professional = Professional.objects.get(user=user)
    url = f"/professional/{current_professional.unique_id}"
    visited_users = users_visited_overview(url)

    data = {
        'visited_users': visited_users,
    }
    print(f"data:  {data}")

    if visited_users:
        return JsonResponse({'status': "success", 'message': data})

    return JsonResponse({'status': "success", 'message': data})

@csrf_exempt
def api_analytics_calls(request):
    user = request.user
    current_professional = Professional.objects.get(user=user)
    url = f"/professional/{current_professional.unique_id}"
    visited_users = users_visited(url)
    visited_users_past = users_visited_past(url)
    top5_cities_arr = top5_cities(url)
    time_spent_on_page = time_spent(url)


    data = {
        'visited_users': visited_users,
        'visited_users_past': visited_users_past,
        'top5_cities_arr': top5_cities_arr,
        'time_spent_on_page': time_spent_on_page,
    }

    return JsonResponse(data)

@login_required
def user_answer_forum(request):
    user = request.user
    current_professional = Professional.objects.get(user=request.user)
    curr_pro_topics = current_professional.specialties.all()

    top_questions = ForumQuestion.objects.filter(resolved_status=False)
    top_questions_related = top_questions.filter(topics__in=curr_pro_topics)

    if top_questions_related: top_questions=top_questions_related

    top_questions = top_questions.distinct()
    top_questions_list = list(top_questions)
    num_questions_to_sample = min(10, len(top_questions_list))
    top_questions = random.sample(top_questions_list, num_questions_to_sample)


    questions_answered = 0
    questions_resolved = 0

    for answers in ForumAnswers.objects.all():
        if answers.professional_answered.user == user:
            questions_answered += 1
            if answers.forum_question.resolved_status == True:
                questions_resolved += 1
    

    context = {
        'top_questions_list': top_questions_list,
        'questions_answered': questions_answered,
        'questions_resolved': questions_resolved
    }



    return render(request, 'accounts/user-answer-forum.html', context)

@login_required
def blog_index(request):
    user=request.user

    user_blogs = Blog.objects.filter(author=user)


    total_blog_views = 0
    total_blog_likes = 0
    blogs_posted = 0

    for blog in user_blogs:
        total_blog_views += blog.blog_views
        total_blog_likes += blog.blog_likes_count
        blogs_posted += 1


    context = {
        'user_blogs':user_blogs,
        'total_blog_views': total_blog_views,
        'blogs_posted': blogs_posted,
        'total_blog_likes': total_blog_likes,
    }

    return render(request, 'accounts/user-blog-index.html', context)

@login_required
def delete_blog_post(request):
    blog_id = request.POST.get('blogId')
    print(f"blog_id: {blog_id}")
    blog_post = get_object_or_404(Blog, pk=blog_id)

    try:
        blog_post.delete()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False})

@login_required
def create_blog_post(request):
    user = request.user
    topics = Specialties.objects.all().order_by('specialty').values
    provinces = Province.objects.all().order_by('province').values

    context = {
        'user': user,
        'topics': topics,
        'provinces': provinces
    }
    return render(request, 'accounts/user-create-blog.html', context)

def post_blog(request):
    user = request.user

    if request.method == 'POST':
        blog_title = request.POST['blog_title']
        blog_text = request.POST['blog_text']
        topic_tag = request.POST['topic_tag']
        province_tag = request.POST['province_tag']

        topic_grabbed=get_object_or_404(Specialties, specialty=topic_tag)
        location_grabbed=get_object_or_404(Province,province=province_tag)

        blog_len = round((len(blog_text.split())/200))

        blog_post = Blog(author=user,
                         blog_title=blog_title,
                         blog_text=blog_text,
                         blog_len=blog_len,
                         topic=topic_grabbed,
                         location=location_grabbed,
                         photo_path = get_random_blog_photo()
                        )
        blog_post.blog_views = 0
        
        blog_post.save()

        if blog_post.pk:
            messages.info(request, ("Your blog has been successfully posted."))
            return JsonResponse({'status': 'success', 'message': 'Blog posted successfully'})
        else:
            messages.error(request, ("There has been an error posting your blog. Please try again or contact support."))
            return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

@login_required
def edit_blog_post(request, pk):
    user = request.user
    blog_post = get_object_or_404(Blog, pk=pk)
    topics = Specialties.objects.all().order_by('specialty').values
    provinces = Province.objects.all().order_by('province').values
    if blog_post.author != user:
        return redirect('user_blog_index')
    else:
        context = {
            'user': user,
            'blog_post': blog_post,
            'topics': topics,
            'provinces': provinces
        }
        return render(request, 'accounts/user-edit-blog.html', context)
    
def edit_blog(request):
    user = request.user
    print(f"what the f goin on in miami bruh!")
    if request.method == 'POST':
        blog_id = request.POST['blog_id']
        blog_post = get_object_or_404(Blog, pk=blog_id)
        blog_title = request.POST['blog_title']
        blog_text = request.POST['blog_text']
        topic_tag = request.POST['topic_tag']
        province_tag = request.POST['province_tag']

        topic_grabbed=get_object_or_404(Specialties, specialty=topic_tag)
        location_grabbed=get_object_or_404(Province,province=province_tag)

        blog_len = round((len(blog_text.split())/200))


        blog_post.blog_title=blog_title
        blog_post.blog_text=blog_text
        blog_post.blog_len=blog_len
        blog_post.topic=topic_grabbed
        blog_post.location=location_grabbed
        
        blog_post.save()

        if blog_post.pk:
            messages.info(request, ("Your blog has been successfully changed."))
            return JsonResponse({'status': 'success', 'message': 'Blog posted successfully'})
        else:
            messages.error(request, ("There has been an error posting your blog. Please try again or contact support."))
            return JsonResponse({'status': 'error', 'message': 'Invalid request method'})




@login_required
def user_edit_profile(request):
    google_maps_api_key = settings.GOOGLE_MAPS_API_KEY
    user = request.user
    specialties = Specialties.objects.all().order_by('specialty')
    languages = Languages.objects.all().order_by('language')
    designations = Designations.objects.all().order_by('designation')
    try:
        current_professional = Professional.objects.get(user=user)
    except Professional.DoesNotExist:
        current_professional = None
    submitted = False 
    if request.method == "POST":

        selected_specialties = json.loads(request.POST.get('specialties_array'))
        selected_langauges = json.loads(request.POST.get('languages_array'))
        selected_designations = json.loads(request.POST.get('designations_array'))
        print(f"here is array: {selected_specialties}")
        form = EditProfileForm(request.POST or None, request.FILES or None, instance=current_professional)
        if form.is_valid():

            #new_pfp = form.data['profile_picture']

            #if new_pfp:
                #current_professional.profile_picture.delete()
            #print(f"new_pfp: {new_pfp}")
            
            professional = form.save(commit=False)
            if not professional.num_of_reviews:
                professional.num_of_reviews = 0
            professional.user = user 
            professional.save()
            form.save_m2m()

            pros_specialties = []
            for pro_specialty in selected_specialties:
               pros_specialties.append(get_object_or_404(Specialties, specialty=pro_specialty))

            professional.specialties.clear()
            professional.specialties.add(*pros_specialties)

            pros_languages = []
            for pro_language in selected_langauges:
               pros_languages.append(get_object_or_404(Languages, language=pro_language))

            professional.languages.clear()
            professional.languages.add(*pros_languages)

            pros_designations = []
            for pro_designation in selected_designations:
               pros_designations.append(get_object_or_404(Designations, designation=pro_designation))

            professional.designations.clear()
            professional.designations.add(*pros_designations)

            professional.save()
            messages.success(request, 'Profile Sucessfully Updated.')
            return HttpResponseRedirect('/edit_profile/?submitted=True')
    else:
        form = EditProfileForm(instance=current_professional)
        if 'submitted' in request.GET:
            submitted = True

    context = {
        'user': user, 
        'form':form, 
        'submitted':submitted, 
        'google_maps_api_key': google_maps_api_key,
        'specialties':specialties,
        'languages': languages,
        'designations': designations
        
    }
    

    return render(request, 'accounts/user-edit-profile.html', context)

@login_required
def user_settings(request):
    user = request.user
    return render(request, 'accounts/user-settings.html', {'user': user})

def user_logout(request):
    logout(request)
    messages.info(request, ("You have been logged out."))
    return redirect('index')

def change_password(request):
    if request.method == "POST":
        old_password = request.POST.get('oldPassword')
        new_password = request.POST.get('newPassword')
        confirm_new_password = request.POST.get('confirmNewPassword')

        if new_password != confirm_new_password:
            messages.error(request, 'New passwords do not match.')
            return redirect('user_settings')
        else:
            user = authenticate(username=request.user.username, password=old_password)
            if user is not None:
                user.set_password(new_password)
                user.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Your password was successfully updated!')
                return redirect('user_settings')
            else:
                messages.error(request, 'Old password is incorrect.')
                return redirect('user_settings')
