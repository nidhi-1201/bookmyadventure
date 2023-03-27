from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
import datetime
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


class index(View):
    def get(self, request):  # request variable takes a GET or POST HTTP request
        user = request.user
        if user.username and user.is_staff is False and user.is_superuser is False:
            form = ReservationForm(request.POST)
            return render(request, "user/index.html", {'form': form})
        else:
            messages.warning(request, 'You are not logged in. Please login')
            return redirect('home')

    def post(self, request):
        user = request.user
        if user.username and user.is_staff is False and user.is_superuser is False:
            form = ReservationForm(request.POST)
            if form.is_valid():
                date = form.cleaned_data['date']
                if date < datetime.date.today():
                    messages.warning(request, 'Please Enter Proper dates')
                    return redirect('index')
                return redirect('book', date)
            else:
                for e in form.errors:
                    messages.error(request, e)
                return redirect('index')
        else:
            messages.warning(request, 'You are not logged in. Please login')
            return redirect('home')


# Function for cancelling reserved activity
def cancel(request, id):  # request variable takes a GET or POST HTTP request
    user = request.user
    if user.username and user.is_staff is False and user.is_superuser is False:

        reservation = Reservation.objects.get(id=id)
        p = PreReservation.objects.get(date=reservation.date, activity_id=reservation.activity_allocated.id)
        p.seats = p.seats + 1
        p.save()
        reservation.status = False
        reservation.save()


        messages.warning(request, 'Your Booking with Booking number  ' + str(
            reservation.bookingID) + ' is cancelled Succesfully')
        return render(request, "booking/cancel_successful.html", {'reservation': reservation})
    else:
        messages.warning(request, 'you are not logged in or have no access')
        return redirect('login')


def book(request, date):  # request variable takes a GET or POST HTTP request
    user = request.user
    if user.username and user.is_staff is False and user.is_superuser is False:
        if request.method == 'POST':
            return redirect('index')
        else:
            try:
                T = PreReservation.objects.filter(date=date)
            except PreReservation.DoesNotExist:
                T = PreReservation.objects.create(date=date)

            if not T:
                activity_available = activity.objects.all()
                for a in activity_available:
                    a.prereservation_set.create(date=date)

            activities = PreReservation.objects.filter(date=date)
        return render(request, 'booking/available.html', {'activities': activities})
    else:
        messages.warning(request, 'You are not logged in. Please login')
        redirect('home')


def activitydetails(request, id):  # request variable takes a GET or POST HTTP request
    user = request.user
    if user.username and user.is_staff is False and user.is_superuser is False:
        if request.method == 'POST':
            a = activity.objects.get(pk = id)
            return render(request, "booking/activitydetails.html", {'activity': a})
        else:
            messages.warning(request, 'something went wrong')
            return redirect('index')
    else:
        messages.warning(request, 'you are not logged in or have no access')
        return redirect('login')


# Function for displaying all user reserved activities
def my_bookings(request):  # request variable takes a GET or POST HTTP request
    user = request.user
    if user.username and user.is_staff is False and user.is_superuser is False:
        T = Reservation.objects.filter(user_booked=user).order_by('-booktime').filter(status=True)
        bookings = []

        for t in T:
            r = t.activity_allocated
            bookings.append({'T': t, 'R': r})
        context = {'bookings': bookings, 'reservation': T}
        return render(request, 'booking/my_bookings.html', context)
    else:
        messages.warning(request, 'You are not authorized to access the requested page. Please Login ')
        return redirect('home')


def feedback(request):  # request variable takes a GET or POST HTTP request
    user = request.user
    if user.username and user.is_staff is False and user.is_superuser is False:
        if request.method == 'POST':
            form = FeedbackForm(request.POST)
            if form.is_valid():
                feed = form.cleaned_data.get('feed')

                newfeedback = Feedback()
                newfeedback.user_of = user
                newfeedback.time = datetime.date.today()
                newfeedback.feed = feed
                newfeedback.feedbackID = str(user.username) + str(datetime.date.today()) + str(user.email)
                newfeedback.save()

                return render(request, "booking/feedback_successful.html")
            else:
                messages.error(request, "Invalid form details")

        form = FeedbackForm()
        return render(request, "booking/feedback.html", context={"form": form})

    else:
        messages.warning(request, 'You are not logged in. Please login')
        redirect('home')
