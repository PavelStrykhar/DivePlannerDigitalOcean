from cProfile import label
from django import forms

from blog.models import Post, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'author', 'short_content', 'content', 'image')
        labels = {
            'title': 'Tytuł',
            'author': 'Autor',
            'short_content': 'Krótka treść',
            'content': 'Treść posta',
            'image': 'Obraz nagłówka'
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.TextInput(attrs={'class': 'form-control', 'value':'', 'id':'elder', 'type':'hidden'}),
            'short_content': forms.Textarea(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            
        }
        
class UpdateForm(forms.ModelForm):
    class Meta:
        model = Post 
        fields = ('title', 'image' , 'short_content', 'content')
        labels = {
            'title': 'Tytuł',
            'image': 'Obraz nagłówka',
            'short_content': 'Krótka treść',
            'content': 'Treść posta'
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'short_content': forms.Textarea(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
        }

class CommentForm(forms.ModelForm):
    
    class Meta:
        model = Comment
        fields = ['content']
    
        widgets = {
            'content': forms.TextInput(attrs={'class':'form-control'}),
        }