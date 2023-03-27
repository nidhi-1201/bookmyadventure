from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm

from django.views import View

from .forms import *
from .models import *


from django.contrib.auth.models import Group


# Function to display the Homepage of the web system
class home(View):
    def get(self, request):
        return render(request=request, template_name="user/home.html")



def sign_up(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, "Invalid Form Details")
    else:
        form = SignupForm()
    return render(request, 'user/sign-up.html', {'form': form})


# Function for editing user details
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


# Function for signing user in
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


# Function for logouut
def logout_request(request):  # request variable takes a GET or POST HTTP request
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect('home')
