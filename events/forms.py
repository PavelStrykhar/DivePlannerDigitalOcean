from asyncio import events
from cProfile import label
from django import forms 
from django.forms import ModelForm
from .models import Venue, Event, Participant, Chat
from .views import *
from datetimepicker.widgets import DateTimePicker

class VenueForm(forms.ModelForm):
    class Meta:
        model = Venue 
        fields = ('name', 'address', 'image', 'postcode', 'phone', 'details') #"__all__"name
        labels = {
			'name': 'Nazwa',
			'address': 'Adres',
   			'image': 'Obrazek miejsca',
			'postcode': 'Kod pocztowy',
   			'phone': 'Numer telefonu właściciela',
			'details': 'Szczegóły lokalizacji',
		}
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control'}), 
            'address': forms.TextInput(attrs={'class':'form-control'}),
            'postcode': forms.TextInput(attrs={'class':'form-control'}),
            'phone': forms.TextInput(attrs={'class':'form-control'}),
            'details': forms.TextInput(attrs={'class':'form-control'}),
        }
#Admin form wirh 'manager'
class EventFormAdmin(forms.ModelForm):
    class Meta:
        model = Event 
        fields = ('name', 'manager', 'venue', 'event_date', 'participants', 'short_description', 'description',) #"__all__"name
        participants = forms.ModelChoiceField(queryset=Participant.objects.none(), empty_label=None,),
        labels = {
			'name': 'Nazwa',
			'manager': 'Organizator',
   			'venue': 'Lokalizacja',
			'event_date': 'Data rospoczęcia',
   			'participants': 'Uczestnicy',
            'short_description': 'Krótki opis',
			'description': 'Szczegóły',
		}
        widgets ={
            #participant_list = Participant.objects.all()
            'name' : forms.TextInput(attrs={'class':'form-control'}), 
            'manager' : forms.Select(attrs={'class':'form-select'}),
            'venue' : forms.Select(attrs={'class':'form-select'}),
            'event_date' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'YYYY-MM-DD HH:MM:SS'}),

            'participants': forms.SelectMultiple(attrs={'class':'form-control'}),
            'short_description' : forms.Textarea(attrs={'class': 'form-control'}),
            'description' : forms.Textarea(attrs={'class': 'form-control'}),    
        }


class EventForm(forms.ModelForm):
    class Meta:
        model = Event 
        fields = ('name', 'venue', 'event_date', 'participants', 'short_description', 'description') #"__all__"name
        participants = forms.ModelChoiceField(queryset=Participant.objects.none()),
        labels = {
			'name': 'Nazwa',
			'manager': 'Organizator',
   			'venue': 'Lokalizacja',
			'event_date': 'Data rospoczęcia YYYY-MM-DD HH:MM:SS',
   			'participants': 'Uczestnicy',
            'Krótki opis': 'short_description',
			'description': 'Szczegóły',
		}
        widgets ={
            'name' : forms.TextInput(attrs={'class':'form-control'}), 
            'manager' : forms.Select(attrs={'class':'form-select'}),
            'venue' : forms.Select(attrs={'class':'form-select'}),
            'event_date' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'YYYY-MM-DD HH:MM:SS'}),
            
            'short_description' : forms.Textarea(attrs={'class': 'form-control'}),
            'description' : forms.Textarea(attrs={'class': 'form-control'}),    
        }
        # def __init__(self, *args, **kwargs):
        #     super(EventForm, self).__init__(*args, **kwargs)
        #     self.fields['participants'] =  Participant(queryset=Participant.objects.all()),
        # def __init__(self, participant_list, *args, **kwargs):
        #     self.base_fields['participants'].choices = participant_list
        #     super(EventForm, self).__init__(*args, **kwargs)


class ParticipantForm(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.HiddenInput())
    event = forms.ModelChoiceField(queryset=Event.objects.all(), widget=forms.HiddenInput())
    class Meta:
        model = Participant
        fields = ['event', 'user']
    
class ChatForm(forms.ModelForm):
    
    class Meta:
        model = Chat
        fields = ['message']
        labels = {'message':'Spytaj o czymś'}
        widgets = {
            'message': forms.TextInput(attrs={'class':'form-control'}),
        }