from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import *
from sprint1.decorators import doctor_required
from .forms import PatientForm, IRMForm
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.


@login_required
def list(request):
    patients = Patient.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(patients, 5)
    try:
        patient = paginator.page(page)
    except PageNotAnInteger:
        patient = paginator.page(1)
    except EmptyPage:
        patient = paginator.page(paginator.num_pages)
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
def addIRMPatient(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        irm_form = IRMForm(request.POST, request.FILES)
        if irm_form.is_valid():
            irm = irm_form.save(commit=False)
            irm.id_patient = patient
            irm.save()
            messages.info(
                request, f'  An new MRI has been added to the patient {patient}.')
            return redirect('sprint2:patient_list')
    irm_form = IRMForm()
    return render(request, 'sprint2/addIrm.html', {'irm_form': irm_form})


@login_required
def editPatient(request, pk):
    patient = get_object_or_404(Patient, pk=pk)

    form = PatientForm(request.POST or None, instance=patient)

    if form.is_valid():
        form.save()

        messages.info(
            request, f'  The patient {patient} has been updated')
        return redirect('sprint2:patient_list')
    return render(request, 'sprint2/editPatient.html', {'form': form})


@login_required
def irm_list(request):
    irms = IRM.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(irms, 5)
    try:
        irm = paginator.page(page)
    except PageNotAnInteger:
        irm = paginator.page(1)
    except EmptyPage:
        irm = paginator.page(paginator.num_pages)
    return render(request, 'sprint2/list_irms.html', {'irms': irms, 'irm': irm})


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
