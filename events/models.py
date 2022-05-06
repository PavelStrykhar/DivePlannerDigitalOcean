from email import message
from re import T
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
import geocoder

token = 'pk.eyJ1IjoicGF2ZWxzdHJ5a2hhciIsImEiOiJjbDI2ZmJmcTkyajBwM2lscDd6aDVwOG4xIn0.15o8i7eD1qwyQcnsx2iBmg'

class Participant(models.Model):
    
    user = models.ForeignKey(User, blank=True, null=True, related_name='attending', on_delete=models.CASCADE)
    event = models.ForeignKey('Event', blank=True, null=True, related_name='attedants', on_delete=models.CASCADE)
    # is_attending = models.BooleanField(default=False)
    def __str__(self):
        return str(self.user.first_name)  + ' ' + str(self.user.last_name)  + ' | ' + str(self.user)  + ' | ' + str(self.event)

class Venue(models.Model):
    name = models.CharField('Venue name', max_length=120)
    owner = models.IntegerField('Owner', blank=False, default=1)
    address = models.CharField(max_length=120)
    long = models.FloatField(blank=True, null=True)
    lat = models.FloatField(blank=True, null=True)
    image = models.ImageField(null=True, blank=True, upload_to="images/events/%Y/%m/%d/")
    postcode = models.CharField('Postcode', max_length=20)
    phone = models.CharField('Contact phone', max_length=15, blank=True)
    details = RichTextField(blank=True, null=True)
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs): #тип аргументы по ключевым словам
        g = geocoder.mapbox(self.address, key=token) #вызов апи
        g = g.latlng  # returns => [lat, long]
        self.lat = g[0]
        self.long = g[1]
        return super(Venue, self).save(*args, **kwargs)

class Event(models.Model):
    name = models.CharField('Event Name', max_length=60)
    description = RichTextField(blank=True, null=True)
    short_description = models.TextField(blank=True, null=True, max_length=500)
    venue = models.ForeignKey(Venue, blank=True, null=True, on_delete=models.CASCADE)
    event_date = models.DateTimeField('Event date')
    manager = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    participants = models.ManyToManyField(Participant, related_name='participant_list', blank=True)
    event_status = models.BooleanField(default=False)
    def __str__(self):
        return self.name

class Chat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    message = models.TextField(verbose_name='message')
    event = models.ForeignKey('Event', related_name='chat', on_delete=models.CASCADE)
    
    def __str__(self):
        return self.user.username + ' | ' + str(self.message) + ' | ' + str(self.date) + ' | ' + str(self.event)
