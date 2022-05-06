from dataclasses import field
from multiprocessing import context
from operator import concat
from re import template
import calendar
from calendar import HTMLCalendar
from datetime import datetime
from requests import request
from cms.models import CmsSlider
from django import views
from django.conf.urls import handler404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse, HttpResponseRedirect
from django.http.response import HttpResponseNotFound
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView
from django.views.generic.edit import FormView
from django.db.models import Count
from blog.forms import CommentForm
from blog.models import Comment, Post
from .forms import *
from .forms import CommentForm
from .models import *
from django.db.models import Q

def index(request):
    posts = Post.objects.all().order_by('-time_create')
    #ordering = ['-id']
    slider_list = CmsSlider.objects.all()
    top_posts = Post.objects.annotate(countlikes=Count('likes')).order_by('-countlikes')[:3]
    
    page = request.GET.get("page")
    paginator = Paginator(posts, 3)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    
    context = {
        'posts' : posts, 
		'slider_list' : slider_list,
		'top_posts':top_posts,
	}
    return render(request, 'blog/index.html', context=context)

class AddPostView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/add_post.html'
    #fields = '__all__'

class UpdatePostView(UpdateView):
	model = Post
	form_class = UpdateForm
	template_name = 'blog/update_post.html'
	#fields = ['title', 'content']

class DeletePostView(DeleteView):
	model = Post
	template_name = 'blog/delete_post.html'
	success_url = reverse_lazy('home')

def LikeView(request, pk):
	post = get_object_or_404(Post, id=request.POST.get('post_id'))
	liked = False
	if post.likes.filter(id=request.user.id).exists():
		post.likes.remove(request.user)
		liked = False
	else:
		post.likes.add(request.user)
		liked = True
	
	return HttpResponseRedirect(reverse('blog:post-detail', args=[str(pk)]))


class PostDetailView(DetailView):
	model = Post
	template_name = 'blog/post-detail.html'
	form = CommentForm
	
	def post(self, request, *args, **kwargs):
		form = CommentForm(request.POST)
		if form.is_valid():
			post = self.get_object()
			form.instance.user = request.user
			form.instance.post = post
			form.save()
			return redirect(reverse('blog:post-detail', kwargs={
				'pk':post.id
			}))
   
	def get_context_data(self, *args, **kwargs):
		context = super(PostDetailView, self).get_context_data(*args, **kwargs)	
		stuff = get_object_or_404(Post, id=self.kwargs['pk'])
		count_likes = stuff.count_likes()	
		liked = False

		if stuff.likes.filter(id=self.request.user.id).exists():
			liked = True
		context["liked"] = liked
		context["count_likes"] = count_likes
		context["form"]=self.form
		return context
 

def searchBlog(request):
    context = {}
    posts = Post.objects.all()
    if request.method == "GET":
        query = request.GET.get("search")
        queryset = posts.filter(Q(title__icontains=query))

        page = request.GET.get("page")
        paginator = Paginator(queryset, 1)
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)
        total = queryset.count()
        context.update({
            "page":page,
            "total":total,
            "query":query,
            "posts":posts,

        })

        return render(request, "blog/search-blog.html", context)