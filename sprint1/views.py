from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from .forms import UserLoginForm, UserRegistrationForm, DoctorRegistration, ReceptionistForm, updateUser
from django.contrib import messages
from django.contrib import auth
from .models import *
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponse


# Create your views here.


def accueil(request):
    if request.user.is_authenticated:
        return redirect('sprint1:UserHomePage')
    return render(request, "sprint1/accueil.html")


def login(request):
    if request.method == "POST":
        login_form = UserLoginForm(request.POST)
        if login_form.is_valid():
            u = login_form.cleaned_data['email']
            p = login_form.cleaned_data['password']
            user = authenticate(email=u, password=p)

            if user is not None:
                auth.login(request, user)
                return redirect('sprint1:UserHomePage')
            else:
                messages.error(
                    request, f"Your username or password are incorrect")

    else:
        login_form = UserLoginForm()
    if request.user.is_authenticated:
        return redirect('sprint1:UserHomePage')
    return render(request, "sprint1/login.html", {'form': login_form})


@login_required
def UserHomePage(request):
    if request.user.is_doctor:
        doc = Doctor.objects.filter(user=request.user).first()
        return render(request, "sprint1/accueil.html", {'doc': doc})
    elif request.user.is_receptionist:
        rec = Receptionist.objects.filter(user=request.user).first()
        return render(request, "sprint1/accueil.html", {'rec': rec})
    else:
        return render(request, 'sprint1/accueil.html')


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
            doc.user = user
            doc.save()
            user.is_doctor = True
            user.save()
            u = user_form.cleaned_data['email']
            p = user_form.cleaned_data['password1']
            b = user_form.cleaned_data['birth_date']
            messages.success(
                request, f' Compte crée, bienvenu(e) {u} ')
            user = authenticate(email=u, password=p, birth_date=b)
            if user is not None:
                auth.login(request, user)
                return redirect('sprint1:UserHomePage')
        else:
            return render(request, 'sprint1/doctor_registration.html', {'user_form': user_form, 'doc_form': doc_form})

    user_form = UserRegistrationForm()
    doc_form = DoctorRegistration()

    return render(request, "sprint1/doctor_registration.html", {'user_form': user_form, 'doc_form': doc_form})


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
                return redirect('sprint1:UserHomePage')
        else:
            return render(request, "sprint1/receptionnist_registration.html", {'user_form': user_form, 'rec_form': rec_form})

    user_form = UserRegistrationForm()
    rec_form = ReceptionistForm()
    return render(request, "sprint1/receptionnist_registration.html", {'user_form': user_form, 'rec_form': rec_form})


@login_required
def profile(request):
    doc = Doctor.objects.filter(user=request.user).first()
    if request.method == 'POST':
        u = updateUser(request.POST, instance=request.user)
        d = DoctorRegistration(request.POST, instance=doc)
        if u.is_valid() and d.is_valid():
            u.save()
            d.save()
            messages.success(request, f'Your profile has been updated')
            return redirect('sprint1:profileDoc')
    else:
        u = updateUser(instance=request.user)
        d = DoctorRegistration(instance=doc)

    return render(request, 'sprint1/profile.html', {'doc': doc, 'u': u, 'd': d})


@login_required
def profileRec(request):
    rec = Receptionist.objects.filter(user=request.user).first()
    if request.method == 'POST':
        u = updateUser(request.POST, instance=request.user)
        r = ReceptionistForm(request.POST, instance=rec)
        if u.is_valid() and r.is_valid():
            u.save()
            r.save()
            messages.success(request, f'your profile has been updated')
            return redirect('sprint1:profileR')
    else:
        u = updateUser(instance=request.user)
        r = ReceptionistForm(instance=rec)
    return render(request, 'sprint1/profileR.html', {'rec': rec, 'u': u, 'r': r})
