from django import forms
from django_select2 import forms as s2forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from bootstrap_datepicker_plus import DatePickerInput
from crispy_forms.helper import FormHelper
from .models import *


class UserLoginForm(forms.Form):
    email = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Email'}))
    password = forms.CharField(
        widget=forms.PasswordInput, )


class UserRegistrationForm(UserCreationForm):

    birth_date = forms.DateField(
        widget=DatePickerInput(

        )
    )

    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Password Confirmation',
        widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ['email', 'birth_date', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email):
            raise forms.ValidationError('Email addresses must be unique.')
        return email

    def clean_password(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if not password1 or not password2:
            raise ValidationError("Password must not be empty")

        if password1 != password2:
            raise ValidationError("Passwords do not match")

        return password2


class DoctorRegistration(forms.ModelForm):

    hopital = forms.ModelChoiceField(
        queryset=Hopital.objects.all()
    )

    class Meta:
        model = Doctor
        fields = ['first_name', 'last_name',
                  'hopital', 'specialite', 'grade']


class ReceptionistForm(forms.ModelForm):

    hopital = forms.ModelChoiceField(
        queryset=Hopital.objects.all()
    )

    class Meta:
        model = Receptionist
        fields = ['first_name', 'last_name',
                  'hopital']


class updateUser(forms.ModelForm):

    birth_date = forms.DateField(
        widget=DatePickerInput(

        )
    )

    class Meta:
        model = User
        fields = ['email', 'birth_date']
