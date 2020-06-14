from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from analysis.models import peaple
from django.http import HttpResponse
from .Checker import Check_data_frame
import pandas as pd
from . import data_analysis


def upload(request):
    if request.method == 'POST' and 'up' in request.POST:
        try:
            uploaded_file = request.FILES['document']

        except:
            return render(request, 'prediction/prediction.html',
                          {"subjects": peaple.objects.all()})

        fs = FileSystemStorage()
        fs.save(uploaded_file.name, uploaded_file)
        data_in = pd.read_csv("media/" + uploaded_file.name)
        if Check_data_frame(data_in):
            largedata, data_out1, data_out2, activity_list = data_analysis.analysis(data_in)
            fs.delete(uploaded_file.name)
            grd = data_out1.loc[data_out1['Activity'] == 'Level ground walking']
            asc = data_out1.loc[data_out1['Activity'] == 'Ramp ascent']
            des = data_out1.loc[data_out1['Activity'] == 'Ramp descent']
            grd_sl = list(grd.Stride_length)
            des_sl = list(des.Stride_length)
            asc_sl = list(asc.Stride_length)
            grd_speed = list(grd.Speed)
            asc_speed = list(asc.Speed)
            des_speed = list(des.Speed)
            grd_time = list(grd.Stride_time)
            asc_time = list(asc.Stride_time)
            des_time = list(des.Stride_time)
            data_out2['Calories'] = [0, 0, 0, 0, 0]
            mean_val = [data_out1['Stride_length'].mean(), data_out1['Speed'].mean()]
            mas_ = list(data_out1.msa)
            mas_1 = [x for x in mas_ if x == x]
            mast_ = list(data_out1.mast)
            mast_2 = [x for x in mast_ if x == x]
            describe_sl = data_out1.groupby('Activity')['Stride_length'].describe()
            describe_sd = data_out1.groupby('Activity')['Speed'].describe()
            describe_sl.rename(columns={'50%': 'median'}, inplace=True)
            describe_sd.rename(columns={'50%': 'median'}, inplace=True)
            for i in range(len(describe_sl.columns)):
                for j in range(len(describe_sl)):
                    describe_sl[describe_sl.columns[i]][j] = round(describe_sl[describe_sl.columns[i]][j], 2)
                    describe_sd[describe_sd.columns[i]][j] = round(describe_sd[describe_sd.columns[i]][j], 2)
            for i in range(len(mean_val)):
                mean_val[i] = round(mean_val[i], 2)

            return render(request, "prediction/New.html",
                          {'grd_sl': grd_sl,
                           'asc_sl': asc_sl, 'des_sl': des_sl,
                           'grd_speed': grd_speed, 'asc_speed': asc_speed,
                           'des_speed': des_speed, 'grd_time': grd_time, 'large_data': largedata,
                           'asc_time': asc_time, 'des_time': des_time,
                           'data_out2': data_out2, 'mas_1': mas_1,
                           'mast_2': mast_2,
                           'mean_val': mean_val,
                           'describe_sl': describe_sl,
                           'describe_sd': describe_sd,
                           'activity_all': activity_list,
                           "subjects": peaple.objects.all()})

        else:
            fs.delete(uploaded_file.name)
            return render(request, 'prediction/Wrongformat.html',
                          {"subjects": peaple.objects.all()})

    elif request.method == 'POST' and 'back' in request.POST:
        return render(request, 'prediction/prediction.html',
                      {"subjects": peaple.objects.all()})

    return render(request, 'prediction/prediction.html',
                  {"subjects": peaple.objects.all()})
