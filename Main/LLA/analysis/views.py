from django.shortcuts import render, get_object_or_404
from .models import peaple
# Create your views here.


def person(request, id):
    subject = get_object_or_404(peaple, pk=id)
    return render(request, "analysis/person.html",
                  {"sub": subject,
                   "subjects": peaple.objects.all()})
