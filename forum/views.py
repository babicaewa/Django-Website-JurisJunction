from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import *
from django.http import HttpResponseRedirect
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from core.utils import *
from core.forms import *
import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_protect
from geopy.distance import geodesic
from django.db.models import Q
from django.core.paginator import Paginator
import json

def forum_index(request):
    if request.user:
        user = request.user
    
    message = request.GET.get('message')
    forum_questions = ForumQuestion.objects.all().order_by('-created_at')
    paginator = Paginator(forum_questions, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    provinces = Province.objects.all()
    topics = list(Specialties.objects.values_list('specialty', flat=True))
    topics.sort()

    context = {
        'page_obj': page_obj,
        'topics': topics,
        'provinces': provinces,
        'message': message,
        'user': user
    }
    return render(request,'forum/forum-index.html', context)

def forum_search(request):

    if request.user:
        user = request.user

    print(f"province: {request.GET.get('province')}")

    topics = list(Specialties.objects.values_list('specialty', flat=True))
    topics.sort()

    if request.method == 'GET':
        keywords_entered = request.GET.get('keyword_search')
        topic_selected = request.GET.get('topic')
        province_selected = request.GET.get('province')

        search_questions = ForumQuestion.objects.all().order_by('-created_at')
        provinces = Province.objects.all()

        if keywords_entered:
            keywords = keywords_entered.split()

            query = Q()
            for keyword in keywords:
                query |= Q(forum_question_title__icontains=keyword)

            if keywords_entered:
                search_questions = search_questions.filter(query)
        
        if topic_selected:
            search_questions = search_questions.filter(topics__specialty=topic_selected)
        if province_selected:
            print(f"Province selected: {province_selected}")
            province = get_object_or_404(Province, province=province_selected)
            search_questions = search_questions.filter(location=province)
            print(f"Filtered questions: {search_questions}")
        
        paginator = Paginator(search_questions, 5)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
    
    print(f"keyword_sleelc: {keywords_entered}, topics_seletecx: {topic_selected}, provinces_seletecgt: {province_selected}")

    context = {
        'keyword': keywords_entered,
        'topic_selected': topic_selected,
        'province_selected': province_selected,
        'page_obj': page_obj,
        'topics': topics,
        'provinces': provinces,
        'user': user
    }

    return render(request,'forum/forum-search-results.html', context)

def forum_question(request, pk):
    if request.user:
        user = request.user

    keyword = request.GET.get('keyword')
    topic = request.GET.get('topic')
    province = request.GET.get('province')
    question = get_object_or_404(ForumQuestion, pk=pk)
    answers = ForumAnswers.objects.all()
    answers = answers.filter(forum_question=question)
    num_of_reviews = answers.count()
    print(f"keyword: {keyword}, topic: {topic}, province: {province}")

    context = {
        'question': question,
        'answers': answers,
        'keyword': keyword,
        'topic': topic,
        'province': province,
        'num_of_reviews': num_of_reviews,
        'user':user
    }
    print(f"answers: {answers}")
    print(f"user: {user}")

    return render(request, 'forum/forum-question.html', context)

def forum_ask(request):
    topics = Specialties.objects.all().order_by('specialty').values
    provinces = Province.objects.all().order_by('province').values

    context = {
        'topics': topics,
        'provinces': provinces
    }
    return render(request, 'forum/forum-ask.html', context)

def create_forum_question(request):
    if request.method == 'POST':
        question_email = request.POST['email']
        question_title = request.POST['question_title']
        question_text = request.POST['question_text']
        topics_arr = json.loads(request.POST['topics_arr'])
        province = request.POST['province']
        print(f"email: {question_email}")
        print(f"title: {question_title}")
        print(f"question text: {question_text}")
        print(f"topicArr: {topics_arr}")
        print(f"proinvnce: {province}")

        if len(topics_arr) != 0 and province:
            forum_question = ForumQuestion(asker_email=question_email, 
                                        forum_question_title=question_title,
                                        forum_question=question_text,
                                        view_count=0,
                                        location=get_object_or_404(Province, province=province),
                                        resolved_status = False)
            forum_question.save()

            for topic in topics_arr:
                specialty = get_object_or_404(Specialties, specialty=topic)
                forum_question.topics.add(specialty)

            forum_question.save()

            if forum_question.pk:
                messages.info(request, ("Your question has been posted. We have sent a confirmation email."))
                return JsonResponse({'status': 'success', 'message': 'Review submitted successfully'})
            else:
                messages.error(request, ("There has been an error submitting your question. Please try again or contact support."))
                return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

        else:
            print("WHYNOTWORK")
            return JsonResponse({'status': 'error', 'message': 'You must fill out at least 1 topic and a province.'})
        
def create_forum_answer(request):
    if request.method == 'POST':
        user = request.user
        professional_answered = get_object_or_404(Professional, user=user)
        question_pk = request.POST.get('pk') 
        print(f"pk: {question_pk}")
        question = get_object_or_404(ForumQuestion, pk=question_pk)
        answer_text = request.POST['answer_text']

        forum_answer = ForumAnswers(forum_question = question,
                                    professional_answered = professional_answered,
                                    response = answer_text)
        forum_answer.save()
        if question.resolved_status == False:
            question.resolved_status = True
            question.save()

        if forum_answer.pk:
                messages.info(request, ("Thank you for contributing. We have let them know you've answered."))
                return JsonResponse({'status': 'success', 'message': 'Review submitted successfully'})
        else:
            messages.error(request, ("There has been an error submitting your answer. Please try again or contact support."))
            return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


