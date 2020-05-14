from django.shortcuts import render, HttpResponse
from analysis.models import peaple
# Create your views here.


def home(request):
    return render(request, "website/Home.html",
                  {"subjects": peaple.objects.all()})


def about(request):
    return render(request, "website/About.html",
                  {"subjects": peaple.objects.all()})


def technical(request):
    return render(request, "website/Tech.html",
                  {"subjects": peaple.objects.all()})
