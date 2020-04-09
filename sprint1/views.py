from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from .forms import UserLoginForm, UserRegistrationForm, DoctorRegistration
from django.contrib import auth
from .models import *
from django.contrib.auth.decorators import login_required
import json as simplejson
from django.http import HttpResponse


# Create your views here.


def accueil(request):
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        doc_form = DoctorRegistration(request.POST, request.FILES)

        if user_form.is_valid() and doc_form.is_valid():
            user = user_form.save()
            doc = doc_form.save(commit=False)
            doc.user = user
            doc.save()

            u = user_form.cleaned_data['email']
            p = user_form.cleaned_data['password1']
            user = authenticate(email=u, password=p)

            if user is not None:
                auth.login(request, user)
                return redirect("sprint1:accueil")
            else:
                user_form.add_error(None, "Can't log in now, try later.")
    else:
        user_form = UserRegistrationForm()
        doc_form = DoctorRegistration()

    return render(request, "sprint1/accueil.html", {'user_form': user_form, 'doc_form': doc_form})


def login(request):
    if request.method == "POST":
        login_form = UserLoginForm(request.POST)
        if login_form.is_valid():
            u = login_form.cleaned_data['email']
            p = login_form.cleaned_data['password']
            user = authenticate(email=u, password=p)

            if user is not None:
                auth.login(request, user)
                return redirect("sprint1:accueil")
            else:
                login_form.add_error(
                    None, "Your username or password are incorrect")
    else:
        login_form = UserLoginForm()

    return render(request, 'sprint1/login.html', {'form': login_form})


def logout(request):
    auth.logout(request)
    return redirect("sprint1:accueil")
