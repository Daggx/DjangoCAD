from django import forms
from django_select2 import forms as s2forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django_select2.forms import ModelSelect2Widget

from .models import User, Doctor, Receptionist, Wilaya, Hopital


class UserLoginForm(forms.Form):
    email = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(UserCreationForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Password Confirmation',
        widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']

        def clean_email(self):
            email = self.cleaned_data.get('email')

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if not password1 or not password2:
            raise ValidationError("Password must not be empty")

        if password1 != password2:
            raise ValidationError("Passwords do not match")

        return password2


class DoctorRegistration(forms.ModelForm):
    wilaya = forms.ModelChoiceField(
        queryset=Wilaya.objects.all(), widget=ModelSelect2Widget(Model=Wilaya, search_fields=['nom'],
            dependent_fields={'hopital': 'hopital'},
                                                                 )
    )

    hopital = forms.ModelChoiceField(
        queryset=Hopital.objects.all(), widget=ModelSelect2Widget(Model=Hopital, search_fields=['name','wilaya'], dependent_fields={'wilaya': 'wilaya'}, max_results=500,
                                                                  )
    )

    class Meta:
        model = Doctor
        fields = ['first_name', 'last_name', 'wilaya',
                  'hopital', 'specialite', 'grade']


class ReceptionistForm(forms.ModelForm):
    class Meta:
        model = Receptionist
        fields = ['first_name', 'last_name', 'hopital']
