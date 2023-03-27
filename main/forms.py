from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *


class SignupForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={
        "class": "form__input",
        'placeholder': 'First Name'
    }))
    last_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={
        "class": "form__input",
        'placeholder': 'Last Name'
    }))
    email = forms.EmailField(max_length=200, help_text='required', widget=forms.TextInput(attrs={
        "class": "form__input",
        'placeholder': 'Email'
    }))
    password1 = forms.CharField(max_length=200, help_text='required', widget=forms.PasswordInput(attrs={
        "class": "form__input",
        'placeholder': 'Password'
    }))
    password2 = forms.CharField(max_length=200, help_text='required', widget=forms.PasswordInput(attrs={
        "class": "form__input",
        'placeholder': 'Confirm Password'
    }))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name',
                  'email', 'password1', 'password2')

        widgets = {
            'username': forms.TextInput(attrs={"class": "form__input", 'placeholder': 'username'}),
            'first_name': forms.TextInput(attrs={"class": "form__input", 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={"class": "form__input", 'placeholder': 'Last Name'}),
            'email': forms.TextInput(attrs={"class": "form__input", 'placeholder': 'Email'}),
            'password1': forms.PasswordInput(attrs={"class": "form__input", 'placeholder': 'Password'}),
            'password2': forms.PasswordInput(attrs={"class": "form__input", 'placeholder': 'Confirm Password'}),
        }


class UserEditForm(forms.Form):
    first_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={
        "class": "form__input",
        'placeholder': 'First Name'
    }))
    last_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={
        "class": "form__input",
        'placeholder': 'Last Name'
    }))
    email = forms.EmailField(max_length=200, widget=forms.TextInput(attrs={
        "class": "form__input",
        'placeholder': 'Email'
    }))


class DateInput(forms.DateInput):
    input_type = 'date'


class ReservationForm(forms.Form):
    date = forms.DateField(widget=forms.widgets.DateInput(
        attrs={'type': 'date',
        "class": "form__input",
        }), required=True,)

class FeedbackForm(forms.ModelForm):
    feed = forms.CharField(widget=forms.Textarea(attrs={"class": "form__input", "placeholder": "Write Here", }))
    class Meta:
        model = Feedback
        fields = ['feed']

