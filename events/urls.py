from calendar import calendar
from django import views
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from blog.views import *
from events.views import *
urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    #path('<int:year>/<str:month>/', calendar, name='calendar'),
    path('all_events', all_events, name="all_events"),
    path('my_events', my_events, name="my_events"),
    path('all_venues', all_venues, name="all_venues"),
    path('show_venue/<venue_id>', show_venue, name="show_venue"),
    path('show_event/<event_id>', show_event, name="show_event"),
    path('event_chat_window/<event_id>', event_chat_window, name="event_chat_window"),
    path('add_venue', add_venue, name="add_venue"),
    path('add_event', add_event, name="add_event"),
    path('update_venue/<venue_id>', update_venue, name="update_venue"),
    path('update_event/<event_id>', update_event, name="update_event"),
    path('delete_venue/<venue_id>', delete_venue, name="delete_venue"),
    path('delete_event/<event_id>', delete_event, name="delete_event"),
    path('admin_panel', admin_panel, name="admin_panel"),
    path('venue_events/<venue_id>', venue_events, name='venue_events'),
    
    path('search_events', search_events, name="search_events"),
    path('search_venues', search_venues, name="search_venues"),
]