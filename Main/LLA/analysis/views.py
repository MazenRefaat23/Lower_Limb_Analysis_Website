from django.shortcuts import render, get_object_or_404
from .models import peaple
from . import data_analysis
# Create your views here.


def person(request, id):
    grd_sl = data_analysis.grd_stride_length
    asc_sl = data_analysis.asc_stride_length
    des_sl = data_analysis.des_stride_length
    grd_speed = data_analysis.grd_speed
    asc_speed = data_analysis.asc_speed
    des_speed = data_analysis.des_speed
    grd_time=data_analysis.grd_time
    asc_time=data_analysis.asc_time
    des_time=data_analysis.des_time
    data_out1 = data_analysis.data_out1
    data_out2=data_analysis.data_out2
    mas_1 = data_analysis.mas_1
    mast_2 =data_analysis.mast_2
    mean_val =data_analysis.mean_val
    describe_Stride_length = data_analysis.describe_Stride_length
    describe_Speed = data_analysis.describe_Speed
    subject = get_object_or_404(peaple, pk=id)
    return render(request, "analysis/person.html",
                  {"sub": subject,'grd_sl':grd_sl,
                   'asc_sl':asc_sl,'des_sl':des_sl,
                   'grd_speed':grd_speed,'asc_speed':asc_speed,
                   'des_speed':des_speed,'grd_time':grd_time,
                   'asc_time':asc_time,'des_time':des_time,
                   'data_out1': data_out1,
                   'data_out2':data_out2,
                   'mas_1':mas_1,
                   'mast_2':mast_2,
                   'mean_val':mean_val,
                   'describe_Stride_length' : describe_Stride_length,
                   'describe_Speed':describe_Speed,
                   "subjects": peaple.objects.all()})
