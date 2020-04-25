from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import PatientForm, IRMForm
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.


@login_required
def list(request):
    patients = Patient.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(patients, 8)
    try:
        patient = paginator.page(page)
    except PageNotAnInteger:
        patient = paginator.page(1)
    except EmptyPage:
        irm = paginator.page(paginator.num_pages)
    return render(request, 'sprint2/list_patients.html', {'patients': patients, 'patient': patient})


@login_required
def addPatient(request):
    if request.method == 'POST':
        p_form = PatientForm(request.POST)
        irm_form = IRMForm(request.POST, request.FILES)
        if p_form.is_valid() and irm_form.is_valid():
            patient = p_form.save()
            irm = irm_form.save(commit=False)
            irm.id_patient = patient
            irm.save()
            return redirect('sprint2:patient_list')
    p_form = PatientForm()
    irm_form = IRMForm()
    return render(request, 'sprint2/addPatient.html', {'p_form': p_form, 'irm_form': irm_form})


@login_required
def editPatient(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    irm = IRM.objects.filter(id_patient=patient).first()
    form = PatientForm(request.POST or None, instance=patient)
    irm_form = IRMForm(request.POST or None, request.FILES, instance=irm)
    if form.is_valid() and irm_form.is_valid():
        form.save()
        irm_form.save()
        messages.info(
            request, f'  The patient {patient} has been updated')
        return redirect('sprint2:patient_list')
    return render(request, 'sprint2/editPatient.html', {'form': form, 'irm_form': irm_form})


@login_required
def irm_list(request):
    irms = IRM.objects.all()
    return render(request, 'sprint2/list_irms.html', {'irms': irms})


@login_required
def addIRM(request):
    if request.method == 'POST':
        irm_form = IRMForm(request.POST, request.FILES)
        if irm_form.is_valid():
            patient = Patient.objects.create()
            irm = irm_form.save(commit=False)
            irm.id_patient = patient
            irm.save()
            return redirect('sprint2:irm_list')
    irm_form = IRMForm()
    return render(request, 'sprint2/addIrm.html', {'irm_form': irm_form})
