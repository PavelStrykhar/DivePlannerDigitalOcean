from cProfile import label
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, UserChangeForm
from django.contrib.auth.models import User
from django import forms

from blog.models import Profile


class PasswordChangingForm(PasswordChangeForm):
	old_password = forms.CharField(label ='Stare hasło', widget=forms.PasswordInput(attrs={'class': 'form-control', 'type':'password'}))
	new_password1 = forms.CharField(label = 'Nowe hasło', max_length=100, widget=forms.PasswordInput(attrs={'class': 'form-control', 'type':'password'}))
	new_password2 = forms.CharField(label = 'Powtórz hasło', max_length=100, widget=forms.PasswordInput(attrs={'class': 'form-control', 'type':'password'}))

	class Meta:
		model = User
		fields = ('new_password1', 'new_password2')


class ProfilePageForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ('profile_image', 'biography')
		labels = {
            'biography': 'Krótka informacja',
            'profile_image': 'Twoja awatara',  
        }
		
		widgets = {
			'biography': forms.Textarea(attrs={'class': 'form-control'}),
			# 'profile_image': forms.TextInput(attrs={'class': 'form-control'}),			
		}
  
class EditProfileForm(UserChangeForm):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    last_login = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    date_joined = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password', 'last_login', 'date_joined')
        labels = {
			'username': 'Username',
			'first_name': 'Imię',
   			'last_name': 'Nazwisko',
			'email': 'E-mail',
   			'password': 'Hasło',
			'last_login': 'Ostatnie logowanie',
   			'date_joined': 'Data stworzenia',
		}