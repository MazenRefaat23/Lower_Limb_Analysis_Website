from django.shortcuts import render, get_object_or_404
from .models import peaple
from . import data_analysis
# Create your views here.


def person(request, id):
    subject = get_object_or_404(peaple, pk=id)
    string = str(subject)
    data_out1, data_out2, activity_list,lst_map = data_analysis.analysis(string[0:5])
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
    data_out2['Calories'] = [0,0,0,0,0]
    mean_val = [data_out1['Stride_length'].mean(), data_out1['Speed'].mean()]
    mas_ = list(data_out1.msa)
    mas_1 = [x for x in mas_ if x == x]
    mast_ = list(data_out1.mast)
    mast_2 = [x for x in mast_ if x == x]
    describe_sl=data_out1.groupby('Activity')['Stride_length'].describe()
    describe_sd=data_out1.groupby('Activity')['Speed'].describe()
    describe_sl.rename(columns={'50%':'median'},inplace=True)
    describe_sd.rename(columns={'50%': 'median'}, inplace=True)
    for i in range(len(describe_sl.columns)):
        for j in range(len(describe_sl)):
            describe_sl[describe_sl.columns[i]][j]=round(describe_sl[describe_sl.columns[i]][j],2)
            describe_sd[describe_sd.columns[i]][j] = round(describe_sd[describe_sd.columns[i]][j], 2)
    for i in range(len(mean_val)):
        mean_val[i] = round(mean_val[i], 2)

    return render(request, "analysis/New.html",
                  {"sub": subject,'grd_sl':grd_sl,
                   'asc_sl':asc_sl,'des_sl':des_sl,
                   'grd_speed':grd_speed,'asc_speed':asc_speed,
                   'des_speed':des_speed,'grd_time':grd_time,
                   'asc_time':asc_time,'des_time':des_time,
                   'data_out2':data_out2,'mas_1':mas_1,
                   'mast_2':mast_2,
                   'mean_val':mean_val,
                   'describe_sl':describe_sl,
                   'describe_sd': describe_sd,
                   'activity_all': activity_list,
                   'lst_map': lst_map,
                   "subjects": peaple.objects.all()})
