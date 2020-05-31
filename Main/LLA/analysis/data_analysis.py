import numpy as np
import pandas as pd
from scipy import signal
import math
from scipy.signal import find_peaks
from scipy.signal import argrelextrema


def find_IC(midSwing, local_min):
    lst_IC = []
    lst_TO = []
    j = 0
    for item in midSwing:
        while (item > local_min[j]):
            if (j < len(local_min) - 1):
                j = j + 1
            else:
                break
        if (local_min[j] > item):
            lst_IC.append(local_min[j])
            if(j>0):
                lst_TO.append(local_min[j - 1])
        else:
            lst_TO.append(local_min[j])
    return lst_IC, lst_TO


def activity_segmentation(df, lst_mode):
    lst_activity = []
    for item in lst_mode:
        df_temp = df.loc[df['Mode'] == item]
        lst_activity.append(df_temp['Right_Shank_Gy'])
    return lst_activity


def activity_intervals(df, fs, fc, mode):
    w = fc / (fs / 2)
    b, a = signal.butter(5, w, 'low')
    right_Gy = signal.filtfilt(b, a, np.array(df))
    sum=0
    sum_iv=0
    min_ind = min(len(right_Gy), 4000)
    test = right_Gy[:min_ind]
    peaks, _ = find_peaks(test, height=1)
    peaks2, _ = find_peaks(test*-1, height=1)
    min_p=min(len(peaks),len(peaks2))
    for i in range(min_p):
        sum+=abs(right_Gy[peaks[i]])
        sum_iv+=abs(right_Gy[peaks2[i]])
    if(sum_iv>sum):
        right_Gy*=-1

    lst_index = list(df.index)
    start = 0
    lst_right = []
    for i in range(len(lst_index) - 1):
        if (lst_index[i + 1] > lst_index[i] + 5):
            lst_right.append(right_Gy[start:i + 1])
            start = i + 1
    if (start == 0):
        lst_right.append(right_Gy)
    else:
        lst_right.append(right_Gy[start:len(lst_index)])
    return lst_right


#data_raw= pd.read_csv(r'C:\Users\Abdullah\Desktop\visualization\AB188_Circuit_Raw.csv')
data_out1 = pd.read_csv('analysis/data_out1.csv')
data_out2 = pd.read_csv('analysis/data_out2.csv')
grd=data_out1.loc[data_out1['Activity']=='Level ground walking']
asc=data_out1.loc[data_out1['Activity']=='Ramp ascent']
des=data_out1.loc[data_out1['Activity']=='Ramp descent']
grd_2=data_out2.loc[data_out2['Activity']=='Level ground walking']
asc_2=data_out2.loc[data_out2['Activity']=='Ramp ascent']
des_2=data_out2.loc[data_out2['Activity']=='Ramp descent']
grd_stride_length=list(grd.Stride_length)
#grd_stride_length = [x for x in grd_stride_length if str(x) != 'nan']
des_stride_length = list(des.Stride_length)
asc_stride_length = list(asc.Stride_length)
grd_speed = list(grd.Speed)
asc_speed = list(asc.Speed)
des_speed =list(des.Speed)
grd_time = list(grd.Stride_time)
asc_time = list(asc.Stride_time)
des_time = list(des.Stride_time)
grd_2_time = list(grd_2.Total_time)
asc_2_time = list(asc_2.Total_time)
des_2_time = list(des_2.Total_time)
def calcal(time):
    calories = 0
    for i in range(time):
        calories += 3.4
    return calories
grd_total_time = int(grd_2_time[0])
asc_total_time =  int(asc_2_time[0])
des_total_time = int(des_2_time[0])
Calories = [calcal(grd_total_time), calcal(asc_total_time), calcal(des_total_time)]
data_out2['Calories'] =Calories
describe_Stride_length = data_out1.groupby('Activity')['Stride_length'].describe().to_html()
describe_Speed = data_out1.groupby('Activity')['Speed'].describe().to_html()




data_out1['msa']=data_out1['Speed'].rolling(window=60).mean()
data_out1['mast']=data_out1['Stride_length'].rolling(window=60).mean()
data_out1.head()

mean_val = [data_out1['Stride_length'].mean(), data_out1['Speed'].mean()]
mas_ = list(data_out1.msa)
mas_1 =[x for x in mas_ if x == x]
mast_= list(data_out1.mast)
mast_2 =[x for x in mast_ if x == x]
