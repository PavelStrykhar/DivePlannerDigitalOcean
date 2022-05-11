from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from . import views
app_name = 'chat'
urlpatterns = [
    path('', views.chat, name='chat'),
    path('<str:room_name>/', views.room, name='room'),
]
