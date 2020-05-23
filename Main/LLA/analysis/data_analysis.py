import pandas as pd

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
