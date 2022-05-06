from django.core.mail import EmailMessage, send_mail
from django.conf import settings
from django.http import BadHeaderError, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.views import generic
from django.contrib.auth.forms import PasswordResetForm, UserCreationForm, PasswordChangeForm
from .forms import PasswordChangingForm, EditProfileForm, ProfilePageForm
from django.contrib.auth.views import PasswordChangeView, PasswordResetConfirmView
from django.urls import reverse_lazy
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from . tokens import generate_token

from django.contrib.auth.tokens import default_token_generator
from django.views.generic import DetailView, UpdateView, CreateView
from blog.models import Profile


def signin(request):
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			return redirect('home')
		else:
			messages.success(request, ("Nazwa użytkownika lub hasło są nieprawidłowe, spróbuj ponownie"))	
			return redirect('signin')	


	else:
		return render(request, 'registration/login.html', {})

def signout(request):
	logout(request)
	#messages.success(request, ("Zostałeś wylogowany!"))
	return redirect('home')


def signup(request):
	
	if request.method == 'POST':
		username = request.POST['username']
		first_name = request.POST['first_name']
		last_name = request.POST['last_name']
		email = request.POST['email']
		password1 = request.POST['password1']
		password2 = request.POST['password2']
		
		if User.objects.filter(username=username):
			messages.error(request, "Nazwa użytkownika już istnieje. Proszę spróbować innej nazwy użytkownika")
			return redirect('signup')

		if len(username)<5:
			messages.error(request, "Nazwa użytkownika musi mieć co najmniej 5 znaków")
			return redirect('signup') 
  
		if len(password1)<6:
			messages.error(request, "Hasło musi mieć co najmniej 6 znaków") 
			return redirect('signup') 
			
		if password1 != password2:
			messages.error(request, "Hasła się nie zgadzają")
			return redirect('signup')
		
		if not username.isalnum():
			messages.error(request, "Nazwa użytkownika musi być alfanumeryczna")
			return redirect('signup')
     
		myuser = User.objects.create_user(username, email, password1)
		myuser.first_name = first_name
		myuser.last_name = last_name
		myuser.is_active = False
		myuser.save()
        
		messages.success(request, ("Użytkownik pomyślnie zarejestrowany! Wysłaliśmy Ci wiadomość e-mail z potwierdzeniem, potwierdź swój adres e-mail, aby aktywować konto"))
		

		#Email-message
		subject = "Welcome to Diveplanner - Django Login"
		message = "Hello " + myuser.first_name + "\n" + "Welcome to Diveplanner \n Thank you for visiting our website \n We have also sent you a confirmation email, please confirm your email address in order to activate your account. \n\n Thanking You \n Pavel Strykhar"
		from_email = settings.EMAIL_HOST_USER
		to_list = [myuser.email]
		send_mail(subject, message, from_email, to_list, fail_silently = True)
        
        
        #Email confirmation
		current_site = get_current_site(request)
		email_subject = "Confirm your email "
		message2 = render_to_string('registration/email_confirmation.html', {
			'name': myuser.first_name,
			'domain': current_site.domain,
			'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
			'token': generate_token.make_token(myuser)
		})
		email = EmailMessage(
			email_subject,
			message2, 
			settings.EMAIL_HOST_USER, 
			[myuser.email]
		)
		email.fail_silently = True
		email.send()

		return redirect('signin')

			
	return render(request, 'registration/signup.html')

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        myuser = None
        
    if myuser is not None and generate_token.check_token(myuser, token):
        myuser.is_active = True
        myuser.save()
        login(request, myuser)
        return redirect('home')
    else:
        return render(request, 'registration/activation_failed.html')

class CreateProfilePageView(CreateView):
	model = Profile
	form_class = ProfilePageForm
	template_name = "registration/create_profile.html"
	
	# короче есть пользователь заполянющий эту форму, давай захватим этого пользователя
	# а потом сделаем его доступным для его формы(например бил.ид=7(ид = селф))
	def form_valid(self, form):
		form.instance.user = self.request.user
		return super().form_valid(form)

class ShowProfilePageView(DetailView):
	model = Profile
	template_name = 'registration/profile.html'

	def get_context_data(self, *args, **kwargs):
		#users = Profile.objects.all()
		context = super(ShowProfilePageView, self).get_context_data(*args, **kwargs)
		
		page_user = get_object_or_404(Profile, id=self.kwargs['pk'])

		context["page_user"] = page_user
		return context

class EditProfileInfoView(generic.UpdateView):
	model = Profile
	template_name = 'registration/profile_info.html'
	fields = ['biography', 'profile_image']
	success_url = reverse_lazy('home')

class EditProfileSettingsView(generic.UpdateView):
    
    form_class = EditProfileForm
    template_name = 'registration/profile_settings.html'
    success_url = reverse_lazy('home')
    
    def get_object(self):
        return self.request.user

class PasswordsChangeView(PasswordChangeView):
	form_class = PasswordChangingForm
	success_url = reverse_lazy('password_success')
	#success_url = reverse_lazy('home')
 

 
def password_success(request):
	return render(request, 'registration/password_success.html', {})