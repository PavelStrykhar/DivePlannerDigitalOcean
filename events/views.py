from dataclasses import field
from re import template
from django.shortcuts import get_object_or_404, render, redirect, reverse
import calendar
from calendar import HTMLCalendar
from datetime import datetime
from django.http import HttpResponseRedirect
from django.http import HttpResponse
import csv
from django.db.models import Count
from django.views.generic.edit import CreateView
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Event, Participant, Venue
from .forms import VenueForm, EventForm, EventFormAdmin, ParticipantForm, ChatForm
from blog.views import Post
from django.core.paginator import Paginator
from blog.models import Post
def all_events(request):
    event_list = Event.objects.all().order_by('-id')
    participants = Participant.objects.all()#filter(participant.event.id)
    
    paginator = Paginator(event_list, 3)
    page = request.GET.get("page")
    events = paginator.get_page(page)
    nums = "a" * events.paginator.num_pages
    return render(request, 
        'events/all_events.html', {
        'participants': participants,
        'event_list': event_list,
        'events':events,
        'nums':nums
        })    

def all_venues(request):
    venue_list = Venue.objects.all()
    return render(request, 
        'events/all_venues.html', {
        'venue_list': venue_list,
        })    

def show_event(request, event_id):
    submitted = False
    event = Event.objects.get(pk=event_id)
    participant_list = Participant.objects.filter(event=event.id)
    
    mapbox_access_token = 'pk.eyJ1IjoicGF2ZWxzdHJ5a2hhciIsImEiOiJjbDI2ZmJmcTkyajBwM2lscDd6aDVwOG4xIn0.15o8i7eD1qwyQcnsx2iBmg'
    form = ParticipantForm(request.POST or None, initial={
        'user' : request.user,
        'event': event
        })
    if request.method == "POST":
        if form.is_valid():
            form.save()
            
            messages.success(request, ("Twoje zgłoszenie zostanie wkrótce zatwierdzone."))
            return HttpResponseRedirect("{}?sended=True".format(reverse('show_event', kwargs={'event_id':event.id})))
            
    return render(request, 
        'events/show_event.html', {
        'form':form,
        'event': event,
        'participant_list': participant_list,
        'sended': request.GET.get('sended', False),
        'mapbox_access_token': mapbox_access_token,
        })

def send_message(request, event_id):
    event = Event.objects.get(pk=event_id)
    if request.method == 'POST':
        form = ChatForm(request.POST)
        if form.is_valid():
            form.instance.user = request.user
            form.instance.event = event
            form.save()
            return redirect('event:show_event', event_id=event.id)
    else:
        form = ChatForm()
    context = {'event': event, 
                'form': form}
        
    return render(request, 'event:show_event.html', context=context)

def show_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    venue_owner = User.objects.get(pk=venue.owner)
    mapbox_access_token = 'pk.eyJ1IjoicGF2ZWxzdHJ5a2hhciIsImEiOiJjbDI2ZmJmcTkyajBwM2lscDd6aDVwOG4xIn0.15o8i7eD1qwyQcnsx2iBmg'
    return render(request, 
        'events/show_venue.html', {
        'venue': venue,
        'venue_owner':venue_owner,
        'mapbox_access_token': mapbox_access_token,
        })     

def add_venue(request):
    submitted = False
    if request.method == "POST":
        form = VenueForm(request.POST, request.FILES)
        if form.is_valid():
            venue = form.save(commit=False)
            venue.owner = request.user.id
            venue.save()
            return HttpResponseRedirect('/events/add_venue?submitted=True')
    else:
        form = VenueForm
        if 'submitted' in request.GET:
            submitted = True 
            
    return render(request, 
        'events/add_venue.html', {
        'form':form,
        'submitted':submitted
        })

def add_event(request):
    submitted = False
    if request.method == "POST":
        if request.user.is_superuser:
            form = EventFormAdmin(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/events/add_event?submitted=True')
        else:
            form = EventForm(request.POST)            
            if form.is_valid():
                event = form.save(commit=False)
                event.manager = request.user
                event.save()
                return HttpResponseRedirect('/events/add_event?submitted=True')
    else:
        if request.user.is_superuser:
            form = EventFormAdmin
        else:
            form = EventForm
        if 'submitted' in request.GET:
            submitted = True 
            
    return render(request, 
        'events/add_event.html', {
        'form':form,
        'submitted':submitted
        })

def update_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    form = VenueForm(request.POST or None, request.FILES or None, instance=venue)#автозаполнение формы старыми данными, обновление данных
    if form.is_valid():
            form.save()
            return redirect('all_venues')
    return render(request, 
        'events/update_venue.html', {
        'venue': venue,
        'form':form
        })

# def is_attending(request, event_id):
#     """set user as attending an event."""
#     event = get_object_or_404(Event, id=event_id)
#     attendance  = Participant(
#         participant = request.user, 
#         event = event,
#         is_attending = True
#         )
#     attendance.save()
#     return redirect('show_event')

def update_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    participant_list = Participant.objects.filter(event = event_id)
    # gys = Participant.objects.filter(event_id=Event.pk)
    if request.user.is_superuser:
        form = EventFormAdmin(request.POST or None, instance=event)
        form.fields['participants'].queryset = Participant.objects.filter(event = event_id)
    else:
        form = EventForm(request.POST or None, instance=event)
        form.fields['participants'].queryset = Participant.objects.filter(event = event_id)
    
    if form.is_valid():
        form.save()
        return redirect('all_events')
    return render(request, 
        'events/update_event.html', {
        'event': event,
        'form':form,
        'participant_list':participant_list,
        })    

def delete_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    venue.delete()
    return redirect('all_venues')

def delete_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    if request.user == event.manager:
        event.delete()
        messages.success(request, ("Wydarzenie usunięte"))
        return redirect('all_events')
    else:
        messages.success(request, ("Nie jesteś organizatorem tego wydarzenia"))
        return redirect('all_events')

def search_events(request):
    if request.method == "POST":
        searched = request.POST['searched']    
        events = Event.objects.filter(name__contains=searched)
        return render(request, 
            'events/search_events.html', {
                'searched':searched,
                'events':events,
            })
    else:
        return render(request, 
            'events/search_events.html', {
            })

def search_venues(request):
    if request.method == "POST":
        searched = request.POST['searched']    
        venues = Venue.objects.filter(name__contains=searched)
        return render(request, 
            'events/search_venues.html', {
                'searched':searched,
                'venues':venues,
            })
    else:
        return render(request, 
            'events/search_venues.html', {
            })

def my_events(request):
    if request.user.is_authenticated:
        me = request.user.id
        i_member = Event.objects.filter(participants__user=me)


        events = Event.objects.filter(manager=me)
        return render(request, 
            'events/my_events.html', {
            'events':events,
            'i_member':i_member,
            })
    else:
        messages.success(request, ("M"))
        return redirect('all_events')

def admin_panel(request):
    all_venues = Venue.objects.all()
    post_count = Post.objects.all().count()
    event_count = Event.objects.all().count()
    venue_count = Venue.objects.all().count()
    user_count = User.objects.all().count()

    all_events = Event.objects.all().order_by('-event_date')
    if request.user.is_superuser:
        if request.method == "POST":
            # Get list of checked box id's
            id_list = request.POST.getlist('boxes')

            # Uncheck all events
            all_events.update(event_status=False)

            # Update the database
            for x in id_list:
                Event.objects.filter(pk=int(x)).update(event_status=True)

            # Show Success Message and Redirect
            messages.success(request, ("Lista wydarzeń zaktualizowana!"))
            return redirect('all_events')

        else:
            return render(request, 'events/admin_panel.html',
                {"all_events": all_events,
                "post_count":post_count,
                "event_count":event_count,
                "venue_count":venue_count,
                "user_count":user_count,
                "all_venues":all_venues})
    else:
        messages.success(request, ("Nie masz uprawnień do przeglądania tej strony!"))
        return redirect('home')

    return render(request, 'events/admin_panel.html')

def venue_events(request, venue_id):
	# Grab the venue
	venue = Venue.objects.get(id=venue_id)	
	# Grab the events from that venue
	events = venue.event_set.all()
	if events:
		return render(request, 'events/venue_events.html', {
			"events":events
			})
	else:
		messages.success(request, ("W tym miejscu nie ma żadnych wydarzeń w tej chwili"))
		return redirect('all_venues')

