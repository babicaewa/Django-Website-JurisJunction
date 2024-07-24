from django.shortcuts import render, redirect, get_object_or_404
from .models import Blog, BlogLikes
from forum.models import Specialties, Province
from django.db.models import Q
from django.http import JsonResponse
from core.utils import get_client_ip


def blog_index(request):

    top_three_juris_blogs = Blog.objects.all()
    topics = Specialties.objects.all().order_by('specialty').values
    provinces = Province.objects.all().order_by('province').values

    context = {
        'top_three_juris_blogs': top_three_juris_blogs,
        'topics': topics,
        'provinces': provinces
    }
    return render(request, 'blog/blog-index.html', context)

def blog_post(request, blog_title, pk):

    blog = get_object_or_404(Blog, pk=pk)

    blog.blog_views = blog.blog_views + 1
    blog.save()

    context = {
        'blog': blog,
    }

    return render(request, 'blog/blog-post.html', context)

def blog_search_results(request):
    keyword = request.GET.get('keyword_search')
    query = Q(author__professional__first_name__icontains=keyword) | Q(author__professional__last_name__icontains=keyword) | Q(blog_title__icontains=keyword) | Q(topic__specialty__icontains=keyword) | Q(location__province__icontains=keyword)
    
    blogs_found = Blog.objects.filter(query) 

    context = {
        'blogs_found': blogs_found,
        'keyword': keyword
    }

    return render(request, 'blog/blog-search-results.html', context)


def update_blog_likes(request):
    blog_id = request.POST.get('blog_id')
    print(f"blog_id: {blog_id}")
    like_status = request.POST.get('like_status')
    blog = get_object_or_404(Blog, pk=blog_id)
    ip_address=get_client_ip(request)

    print(f"like status: {like_status}")
    if like_status == 'true':
        print(f"hehehehe")
        existing_like = BlogLikes.objects.filter(blog=blog, ip_address=ip_address)
        print(f"existkng like: {existing_like}")
        if not existing_like:
            print("whasdadsa")
            new_like = BlogLikes(blog=blog, ip_address=get_client_ip(request))
            new_like.save()
            return JsonResponse({'status': 'success', 'message': 'Added Like'})
    else:
        like_to_delete = get_object_or_404(BlogLikes, blog=blog, ip_address=ip_address)   #NEEDS TO BE FIXED, IP ADDRESS KINDA MESSES THSI UP BUT RN IDK
        like_to_delete.delete()
        return JsonResponse({'status': 'success', 'message': 'Removed Like'})
    
    return JsonResponse({'status': 'error', 'message': 'Error in changing like status'})

def check_blog_liked(request):
    blog_id = request.POST.get('blog_id')
    ip_address=get_client_ip(request)
    blog = get_object_or_404(Blog, pk=blog_id)
    existing_like = BlogLikes.objects.filter(blog=blog, ip_address=ip_address)
    if existing_like:
        return JsonResponse({'status': 'success', 'message': 'Already Liked'})
    else:
        return JsonResponse({'status': 'success', 'message': 'Not Liked Yet'})



