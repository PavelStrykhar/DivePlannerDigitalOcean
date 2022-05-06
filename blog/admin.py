from django.contrib import admin
from .models import Post, Comment, Profile
from django import forms
from ckeditor.widgets import CKEditorWidget
from .models import *
from ckeditor_uploader.widgets import CKEditorUploadingWidget


# class PostAdminForm(forms.ModelForm):
#     content = forms.CharField(widget=CKEditorUploadingWidget())
#     class Meta:
#         model = Post
#         fields = '__all__'
        
# class PostsAdmin(admin.ModelAdmin):
#     form = PostAdminForm
#     prepopulated_fields =  {"slug":("title",)}


admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Comment)