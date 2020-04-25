from django import forms
from django.forms import ModelForm
from .models import Patient, IRM


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['first_name', 'last_name',
                  'age', 'gender', 'Address', 'email']


class IRMForm(forms.ModelForm):
    class Meta:
        model = IRM
        fields = ['irm_pic', 'irm_date']
