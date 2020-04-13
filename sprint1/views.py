from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from .forms import UserLoginForm, UserRegistrationForm, DoctorRegistration, ReceptionistForm
from django.contrib import messages
from django.contrib import auth
from .models import *
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseRedirect

# Create your views here.


def accueil(request):
    #     if request.POST.get('submit') == "register":
    #         user_form = UserRegistrationForm(request.POST)
    #         doc_form = DoctorRegistration(request.POST, request.FILES)

    #         if user_form.is_valid() and doc_form.is_valid():
    #             user = user_form.save()
    #             doc = doc_form.save(commit=False)
    #             doc.user = user
    #             doc.save()

    #             u = user_form.cleaned_data['email']
    #             p = user_form.cleaned_data['password1']
    #             b = user_form.cleaned_data['birth_date']

    #             user = authenticate(email=u, password=p, birth_date=b)
    #             if user is not None:
    #                 auth.login(request, user)
    #                 return redirect("sprint1:accueil")

    #         else:
    #             for msg in user_form.error_messages:
    #                 messages.error(
    #                     request, f"{msg}: {user_form.error_messages[msg]}")
    if request.method == "POST":
        #     elif request.POST.get('submit') == "login":
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

    login_form = UserLoginForm(request.POST)
    return render(request, "sprint1/accueil.html", {'form': login_form})


def logout(request):
    auth.logout(request)
    return redirect("sprint1:accueil")


def DoctorRegister(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        doc_form = DoctorRegistration(request.POST, request.FILES)
        if user_form.is_valid() and doc_form.is_valid():
            user = user_form.save()

            doc = doc_form.save(commit=False)
            context = {}
            doc.user = user
            doc.save()

            user.is_doctor = True
            user.save()
            u = user_form.cleaned_data['email']
            p = user_form.cleaned_data['password1']
            b = user_form.cleaned_data['birth_date']

            user = authenticate(email=u, password=p, birth_date=b)
            if user is not None:
                auth.login(request, user)
                return render(request, "sprint1/accueil.html", {'doc': doc})

    user_form = UserRegistrationForm()
    doc_form = DoctorRegistration()
    form = UserLoginForm()

    return render(request, "sprint1/doctor_registration.html", {'user_form': user_form, 'doc_form': doc_form, 'form': form})


def RecipRegister(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        rec_form = ReceptionistForm(request.POST, request.FILES)
        if user_form.is_valid() and rec_form.is_valid():
            user = user_form.save()

            rec = rec_form.save(commit=False)
            rec.user = user
            rec.save()
            user.is_receptionist = True
            user.save()

            u = user_form.cleaned_data['email']
            p = user_form.cleaned_data['password1']
            b = user_form.cleaned_data['birth_date']

            user = authenticate(email=u, password=p, birth_date=b)
            if user is not None:
                auth.login(request, user)
                return render(request, "sprint1/accueil.html", {'rec': rec})

    user_form = UserRegistrationForm()
    form = UserLoginForm()
    rec_form = ReceptionistForm()
    return render(request, "sprint1/receptionnist_registration.html", {'user_form': user_form, 'rec_form': rec_form, 'form': form})
