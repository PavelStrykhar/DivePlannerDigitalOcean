from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib import admin
from blog.views import *
from django.conf.urls.static import static
from django.conf import settings
from blog.models import *
from .views import PostDetailView, AddPostView, UpdatePostView, DeletePostView, LikeView
from blog.views import searchBlog
app_name = 'blog'

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('post/<int:pk>', PostDetailView.as_view(), name='post-detail'),
    path('add_post/', AddPostView.as_view(), name='add_post'),
    path('post/update/<int:pk>', UpdatePostView.as_view(), name='update_post'),
    path('post/<int:pk>/remove', DeletePostView.as_view(), name='delete_post'),
    path("q/", searchBlog, name='search'),
    path('like/<int:pk>', LikeView, name='like_post'),
    path('<int:year>/<str:month>/', index, name="calendar"),
]
