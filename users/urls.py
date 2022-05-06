from django.urls import path
from . import views
from .views import PasswordsChangeView, PasswordResetConfirmView, CreateProfilePageView, ShowProfilePageView, EditProfileSettingsView, EditProfileInfoView
from django.contrib.auth import views as auth_views
urlpatterns = [
    
    path('signin', views.signin, name="signin"),
    path('signout', views.signout, name='signout'),
    path('signup', views.signup, name='signup'),
	path('password/', PasswordsChangeView.as_view(template_name='registration/change-password.html')),
    path('password_success', views.password_success, name="password_success"),
    path('create_profile/', CreateProfilePageView.as_view(), name='create_profile'),
    path('<int:pk>/profile/', ShowProfilePageView.as_view(), name='show_profile'),
    path('profile_settings/', EditProfileSettingsView.as_view(), name='profile_settings'),
    path('<int:pk>/profile_info/', EditProfileInfoView.as_view(), name='profile_info'),
    path('activate/<uidb64>/<token>', views.activate, name="activate"),
    
    
]
