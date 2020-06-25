from django.shortcuts import render, get_object_or_404
from .models import peaple
from . import data_analysis

from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse

from .pdf import dynamic_save_pdf
from io import BytesIO
from PIL import Image
import re
import base64


def makeImg(request, name, saveName):
    image_data = request.POST.get(name, '')
    image_data = re.sub("^data:image/png;base64,", "", image_data)
    image_data = base64.b64decode(image_data)
    image_data = BytesIO(image_data)

    fs = FileSystemStorage()
    fs.save(saveName, image_data)



# Create your views here.


def person(request, id):

    global describe_sl
    global describe_sd
    global grd_sl
    global data_out2
    global mean_val

    if request.method == 'POST' and 'save' in request.POST:

        makeImg(request, 'image_1', 'out_1.jpg')

        makeImg(request, 'image_2_1', 'out_2_1.jpg')
        makeImg(request, 'image_2_2', 'out_2_2.jpg')

        makeImg(request, 'image_3_1_1', 'out_3_1_1.jpg')
        makeImg(request, 'image_3_1_2', 'out_3_1_2.jpg')
        makeImg(request, 'image_3_1_3', 'out_3_1_3.jpg')

        makeImg(request, 'image_3_2_1', 'out_3_2_1.jpg')
        makeImg(request, 'image_3_2_2', 'out_3_2_2.jpg')
        makeImg(request, 'image_3_2_3', 'out_3_2_3.jpg')

        makeImg(request, 'image_3_3_1', 'out_3_3_1.jpg')
        makeImg(request, 'image_3_3_2', 'out_3_3_2.jpg')
        makeImg(request, 'image_3_3_3', 'out_3_3_3.jpg')

        makeImg(request, 'image_4_1', 'out_4_1.jpg')

        makeImg(request, 'image_4_2', 'out_4_2.jpg')

        makeImg(request, 'image_4_3', 'out_4_3.jpg')

        makeImg(request, 'image_4_4', 'out_4_4.jpg')

        makeImg(request, 'image_4_5', 'out_4_5.jpg')

        makeImg(request, 'image_4_6', 'out_4_6.jpg')

        makeImg(request, 'image_4_7', 'out_4_7.jpg')

        dynamic_save_pdf(describe_sl, describe_sd, grd_sl, data_out2, mean_val)

        fs = FileSystemStorage()

        fs.delete('out_1.jpg')

        fs.delete('out_2_1.jpg')
        fs.delete('out_2_2.jpg')

        fs.delete('out_3_1_1.jpg')
        fs.delete('out_3_1_2.jpg')
        fs.delete('out_3_1_3.jpg')

        fs.delete('out_3_2_1.jpg')
        fs.delete('out_3_2_2.jpg')
        fs.delete('out_3_2_3.jpg')

        fs.delete('out_3_3_1.jpg')
        fs.delete('out_3_3_2.jpg')
        fs.delete('out_3_3_3.jpg')

        fs.delete('out_4_1.jpg')
        fs.delete('out_4_2.jpg')
        fs.delete('out_4_3.jpg')
        fs.delete('out_4_4.jpg')

        with fs.open('output.pdf', 'rb') as pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment;filename=output.pdf'

            fs.delete('output.pdf')

            return response

    else:
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
