from django.contrib import admin
from .models import Participant, Venue, Event, Chat

@admin.register(Participant)
class Participant(admin.ModelAdmin):
    list_display = ('event',)

@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'phone')
    ordering = ('name',)
    search_fields = ('name',)

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    fields = (('name', 'venue'), 'event_date', 'description', 'manager', 'event_status')
    list_display = ('name', 'event_date', 'venue')
    list_filter = ('event_date', 'venue')
    ordering = ('event_date',)
admin.site.register(Chat)