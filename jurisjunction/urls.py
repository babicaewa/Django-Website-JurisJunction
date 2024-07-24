"""
URL configuration for jurisjunction project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from core import views as core_views
from accounts import views as accounts_views
from forum import views as forum_views
from blog import views as blog_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', core_views.index, name = 'index'),
    path('pricing/', core_views.pricing, name = 'pricing'),
    path('login-signup/', accounts_views.signin, name = 'signin'),
    path('support-feedback/', core_views.support_feedback, name = 'support_feedback'),
    path('about-us/', core_views.about_us, name = 'about_us'),
    path('faq/', core_views.faq, name = 'faq'),
    path('features/', core_views.features, name = 'features'),
    path('search_results/', core_views.search_results, name = 'search_results'),
    path('profile_overview/', accounts_views.user_overview, name = "user_overview"),
    path('profile_overview/api/overview_analytics/',accounts_views.api_overview_analytics, name ='api_overview_analytics'),
    path('profile_analytics/', accounts_views.user_analytics, name = "user_analytics"),
    path('profile_answer_forums/', accounts_views.user_answer_forum, name = "user_answer_forums"),
    path('edit_profile/', accounts_views.user_edit_profile, name = "user_edit_profile"),
    path('user_blogs/', accounts_views.blog_index, name="user_blog_index"),
    path('user_blogs/delete_blog_post/', accounts_views.delete_blog_post, name = "user_delete_blog_post"),
    path('user_blogs/create_blog/', accounts_views.create_blog_post, name='create_blog_post'),
    path('user_blogs/post_blog/', accounts_views.post_blog, name='post_blog'),
    path('user_blogs/edit_blog_post_<int:pk>', accounts_views.edit_blog_post, name='edit_blog_post'),
    path('user_blogs/edit_blog/', accounts_views.edit_blog, name='edit_blog'),
    path('profile_settings/', accounts_views.user_settings, name = "user_settings"),
    path('change_password/', accounts_views.change_password, name = "change_password"),
    path('user_logout/', accounts_views.user_logout, name = "user_logout"),
    path('professional/<str:unique_id>', core_views.professional_page, name ='professional_page'),
    path('create_review', core_views.create_review, name = 'create_review'),
    path('api/analytics_calls/', accounts_views.api_analytics_calls, name='api_analytics_calls'),
    path('get_reviews/', core_views.get_reviews, name='get_reviews'),
    path('forum/', forum_views.forum_index, name='forum_home'),
    path('forum/search_results/', forum_views.forum_search, name='forum_search_results'),
    path('forum/forum_question/<int:pk>', forum_views.forum_question, name='forum_question'),
    path('forum/ask-a-question/', forum_views.forum_ask, name='forum_ask'),
    path('create_forum_question/', forum_views.create_forum_question, name='create_forum_question'),
    path('create_forum_answer/', forum_views.create_forum_answer, name='create_forum_answer'),
    path('blogs/', blog_views.blog_index, name='blog_index'),
    path('blogs/blog_post/<str:blog_title>_<int:pk>/', blog_views.blog_post, name='blog_post'),
    path('blogs/blog_search_results/', blog_views.blog_search_results, name='blog_search_results'),
    path('update_blog_likes', blog_views.update_blog_likes, name='update_blog_likes'),
    path('check_blog_liked', blog_views.check_blog_liked, name='check_blog_liked'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

