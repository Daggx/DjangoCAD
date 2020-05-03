from django.shortcuts import render, redirect, get_object_or_404
from sprint2.forms import *
from sprint2.models import IRM
from scripts.test import cf
from scripts.CBIRcomplet import CBIR
from django.core.files.storage import FileSystemStorage


# Create your views here.


def classification(request, pk):
    irm = get_object_or_404(IRM, pk=pk)
    if request.method == 'POST':
        print(irm.irm_pic.name)
        images = CBIR(irm.irm_pic)
        imgs = []
        for i in images:
            i = i.replace("mask", "")
            imgs.append(i)

        return render(request, 'sprint3/classification.html', {'irm': irm, 'imgs': imgs})
    return render(request, 'sprint3/classification.html', {'irm': irm})


def cff(request, pk):
    if request.method == 'POST':
        irm = get_object_or_404(IRM, pk=pk)
        spt = "n3adin bande de chien j'en ai marre"
        return render(request, 'sprint3/classification.html', {'irm': irm, 'spt': spt})
