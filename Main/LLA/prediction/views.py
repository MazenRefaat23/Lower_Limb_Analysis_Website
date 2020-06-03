from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from analysis.models import peaple
from django.http import HttpResponse
import pandas as pd

from .CNN import prep


def prediction(request):
    return render(request, "prediction/prediction.html",
                  {"subjects": peaple.objects.all()})


def upload(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        fs.save(uploaded_file.name, uploaded_file)
        data_in = pd.read_csv("media/" + uploaded_file.name)
        data_pred = pd.DataFrame(prep(data_in))
        return HttpResponse(data_pred.to_html())

    return render(request, 'prediction/prediction.html',
                  {"subjects": peaple.objects.all()})
