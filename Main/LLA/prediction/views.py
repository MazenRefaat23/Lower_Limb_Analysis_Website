from django.shortcuts import render
from django.core.files.storage import FileSystemStorage


def prediction(request):
    return render(request, "prediction/prediction.html")


def upload(request):
    if request.method == 'POST':
        uploaded_file = request.files['document']
        fs = FileSystemStorage
        fs.save(uploaded_file.name, uploaded_file)
    return render(request, 'prediction.html')
