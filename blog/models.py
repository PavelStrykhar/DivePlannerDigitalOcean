import email
from email.policy import default
from autoslug import AutoSlugField
from ckeditor.fields import RichTextField
from django.conf import settings

from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.forms import DateTimeField
from django.shortcuts import reverse
from django.urls import reverse
from ckeditor.fields import RichTextField

class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    profile_image = models.ImageField(null=True, blank=True, upload_to="images/profile/")
    biography = models.TextField()
    
    def __str__(self):
        return str(self.user)
    
    def get_absolute_url(self):
        return reverse('home')

class Post(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    short_content = models.TextField(max_length=600)
    content = RichTextField(blank=True, null=True)
    image = models.ImageField(upload_to="images/%Y/%m/%d/")
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    
    # is_published = models.BooleanField(default=True)    
    likes = models.ManyToManyField(User, related_name='blog_posts')
   
    def count_likes(self):
        return self.likes.count()
    
    def __str__(self):
        return self.title + ' | ' + str(self.author)
    
    def get_absolute_url(self):
        return reverse('home')
    
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    content = models.TextField(verbose_name='Komentarz')
    post = models.ForeignKey('Post', related_name='comments', on_delete=models.CASCADE)
    

    def __str__(self):
        return self.user.username + ' | ' + str(self.content) + ' | ' + str(self.date) + ' | ' + str(self.post)
