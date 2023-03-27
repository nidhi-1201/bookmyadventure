from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home.as_view(), name='home'),
    path('home/', views.home.as_view(), name='home'),
    path('signup/', views.sign_up, name='signup'),
    path('logout/', views.logout_request, name='logout'),
    path('login/', views.login_request, name='login'),
    path('password_change/', auth_views.PasswordChangeView.as_view(), {'template_name': 'user/change_password.html'},
         name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
]