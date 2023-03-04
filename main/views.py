from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db.models import Q

from django.db.models import Count
from .forms import *
from .models import *
import datetime

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

from django.contrib.auth.models import Group


# The major backend logic for online guest house booking system

# Function to display the Homepage of the web system
def home(request):
    return render(request=request, template_name="user/home.html")


# Function to Sign up new user
def sign_up(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            messages.info(request, "Welcome to KGP")
            return redirect('index')
        else:
            messages.error(request, "Invalid Form Details")
    else:
        form = SignupForm()
    return render(request, 'user/sign-up.html', {'form': form})


# Fuction to edit User details
def edit_user(request):
    if not request.user.is_authenticated:
        return redirect('login')
    user = get_object_or_404(User, pk=request.user.pk)
    if request.method == 'POST':

        form = UserEditForm(request.POST)
        if form.is_valid():

            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.email = form.cleaned_data.get('email')
            user.save()
            messages.info(request, "User Details Updated Succesfully")
            return redirect("index")
        else:
            messages.error(request, "Invalid Form Details")

    else:

        form = UserEditForm(initial={
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        })
    return render(request, 'user/user-edit.html', {'form': form})


# Function to Login in a new user
def login_request(request):  # request variable takes a GET or POST HTTP request
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user.is_staff or user.is_superuser:
                messages.error(request, "Visitor's login only!")
                return redirect('login')

            if user is not None:
                # Checking if a user if a staff
                if user.is_staff and not user.groups.filter(name='Staff').exists():
                    group = Group.objects.get(name='Staff')
                    user.groups.add(group)
                login(request, user)
                messages.info(request, f"You are now logged in as {username}")
                return redirect('index')
            else:
                messages.error(request, "Invaild username or password")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request, "user/login.html", context={"form": form})


# Function to logout the user
def logout_request(request):  # request variable takes a GET or POST HTTP request
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect('home')


# Function to change the password of the user
def change_password(request):  # request variable takes a GET or POST HTTP request
    user = request.user
    if user.username and user.is_staff is False and user.is_superuser is False:
        if request.method == 'POST':
            form = PasswordChangeForm(request.user, request.POST)
            if form.is_valid():  # here user details are verified from database
                user = form.save()
                update_session_auth_hash(request.user)
                messages.success(request, 'Your password was successfully updated!')
                return redirect('change_password')
            else:
                messages.error(request, 'Please correct the error below:')
        else:
            form = PasswordChangeForm(request.user)
        return render(request, 'user/change_password.html', {'form': form})
    else:
        messages.warning(request, 'You are not logged in. Please login')
        return redirect('home')
