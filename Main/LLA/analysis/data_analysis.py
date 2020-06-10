import numpy as np
import pandas as pd
from scipy import signal
import math
from scipy.signal import find_peaks
from scipy.signal import argrelextrema
from google.cloud import bigquery

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

def velocity(w, l, fs):
    t = 1 / fs
    theta = np.trapz(w, dx=t)
    sintheta = math.sin(theta / 2)
    time = len(w) / fs
    if (time == 0):
        return 1.14036
    vel = (2 * l * sintheta) / time
    return vel

def analysis(table_name):
    discarded=0
    data_out1 = pd.DataFrame()
    data_out2 = pd.DataFrame()
    walk_out1 = pd.DataFrame()
    walk_out2 = pd.DataFrame()
    ascent_out1 = pd.DataFrame()
    ascent_out2 = pd.DataFrame()
    descent_out1 = pd.DataFrame()
    descent_out2 = pd.DataFrame()
    stair_ascent_out2=pd.DataFrame()
    stair_descent_out2=pd.DataFrame()
    fs = 1000
    fc = 5
    L = 1

    #####################
    
    client = bigquery.Client.from_service_account_json("analysis/graduationproject-277217-1dbf1091220d.json")
    query = """
            SELECT  Mode,
            Right_Shank_Gy,
            FROM `graduationproject-277217.Raw_Data.{}`
            ORDER BY Row
            LIMIT 200000
        """.format(table_name)
    query_job = client.query(query)  # Make an API request.
    data_in = query_job.to_dataframe()
    
    ##############


    large_list = []

    data_in['Interval'] = (data_in.Mode != data_in.Mode.shift()).cumsum()
    arr = np.array(data_in.groupby('Interval')['Mode'].agg(['count', 'max']))

    start = 0
    finish = 0
    for i in range(len(arr)):
        finish += arr[i][0]/1000
        large_list.append([arr[i][1], start, finish])
        start = finish
    #data_in = pd.read_csv("analysis/" + name + ".csv", usecols=["Right_Shank_Gy", "Mode"])
    lst_activity = activity_segmentation(data_in, [1, 2, 3,4,5])
    stair_ascent=lst_activity[3]
    stair_descent=lst_activity[4]
    if (len(stair_ascent)>2000):
        w = fc / (fs / 2)
        b, a = signal.butter(5, w, 'low')
        str_asc = signal.filtfilt(b, a, np.array(stair_ascent))
        for i in range(2000):
            if(str_asc[i]<-2.2):
                str_asc*=-1
                break
        peaks, _ = find_peaks(str_asc, height=2)
        strA_steps=len(peaks)*2
        strA_time=len(str_asc)/fs
        strA_cad=int(strA_steps*60/strA_time)
        stair_ascent_out2['Total_strides']=[strA_steps]
        stair_ascent_out2['Total_time']=[strA_time]
        stair_ascent_out2['Activity']=['Stair ascent']
        stair_ascent_out2['Avg_cadence'] = [strA_cad]
    else:
        stair_ascent_out2['Total_strides'] = [0]
        stair_ascent_out2['Activity'] = ['Stair ascent']

    if (len(stair_descent)>2000):
        w = fc / (fs / 2)
        b, a = signal.butter(5, w, 'low')
        str_des = signal.filtfilt(b, a, np.array(stair_descent))
        for i in range(2000):
            if(str_des[i]<-2.2):
                str_des*=-1
                break
        peaks, _ = find_peaks(str_des, height=2)
        strD_steps=len(peaks)*2
        strD_time=len(str_des)/fs
        strD_cad=int(strD_steps*60/strD_time)
        stair_descent_out2['Total_strides']=[strD_steps]
        stair_descent_out2['Total_time']=[strD_time]
        stair_descent_out2['Activity']=['Stair descent']
        stair_descent_out2['Avg_cadence'] = [strD_cad]
    else:
        stair_descent_out2['Total_strides'] = [0]
        stair_descent_out2['Activity'] = ['Stair descent']

    if (len(lst_activity[0]) > 2000):
        walk_out1 = pd.DataFrame()
        walk_out2 = pd.DataFrame()
        grd_dis = []
        grd_vel = []
        grd_mode = []
        grd_time = []
        grd_swing = []
        grd_stance = []
        walk = activity_intervals(lst_activity[0], fs, fc, 1)
        for i in range(len(walk)):
            peaks, _ = find_peaks(walk[i], height=1.7)
            local_min = argrelextrema(walk[i], np.less)[0]
            IC_points, TO_points = find_IC(peaks, local_min)
            maxx = max(len(IC_points), len(TO_points))
            j = 0
            if (maxx > 1):
                if (TO_points[0] < IC_points[0] and len(TO_points) > 1):
                    for k in range(len(TO_points) - 1):
                        start = TO_points[k]
                        end = TO_points[k + 1]
                        stride_time = (end - start) / fs
                        while (IC_points[j] < start):
                            j += 1
                        ic = IC_points[j]
                        swing = (ic - start) / fs / stride_time * 100
                        stance = 100 - swing
                        if (swing < 38 or swing > 50):
                            continue
                        w = walk[i][start:ic]
                        vel = velocity(w, L, fs)
                        if (vel < 0.7):
                            continue
                        dis = vel * stride_time
                        grd_dis.append(round(dis, 2))
                        grd_vel.append(round(vel, 2))
                        grd_mode.append("Level ground walking")
                        grd_time.append(round(stride_time, 2))
                        grd_swing.append(round(swing, 2))
                        grd_stance.append(round(stance, 2))
                else:
                    for k in range(len(IC_points) - 1):
                        start = IC_points[k]
                        end = IC_points[k + 1]
                        stride_time = (end - start) / fs
                        while (TO_points[j] < start):
                            j += 1
                        to = TO_points[j]
                        swing = (end - to) / fs / stride_time * 100
                        stance = 100 - swing
                        if (swing < 38 or swing > 50):
                            continue
                        w = walk[i][to:end]
                        vel = velocity(w, L, fs)
                        if (vel < 0.7):
                            continue
                        dis = vel * stride_time
                        grd_dis.append(round(dis, 2))
                        grd_vel.append(round(vel, 2))
                        grd_mode.append("Level ground walking")
                        grd_time.append(round(stride_time, 2))
                        grd_swing.append(round(swing, 2))
                        grd_stance.append(round(stance, 2))

            i += 1

        walk_strides = len(grd_dis)
        walk_dis = sum(grd_dis)
        walk_time = sum(grd_time)
        walk_avg_dis = round(sum(grd_dis) / walk_strides, 2)
        walk_avg_vel = round(sum(grd_vel) / walk_strides, 2)
        walk_avg_time = round(sum(grd_time) / walk_strides, 2)
        walk_avg_swing = round(sum(grd_swing) / walk_strides, 2)
        walk_avg_stance = 100 - walk_avg_swing
        walk_cadence = int(walk_strides * 120 / sum(grd_time))

        walk_out1['Stride_length'] = grd_dis
        walk_out1['Speed'] = grd_vel
        walk_out1['Stride_time'] = grd_time
        walk_out1['Swing'] = grd_swing
        walk_out1['Stance'] = grd_stance
        walk_out1['Activity'] = grd_mode

        walk_out2["Total_strides"] = [walk_strides]
        walk_out2["Total_distance"] = [walk_dis]
        walk_out2["Total_time"] = [walk_time]
        walk_out2["Avg_stride_length"] = [walk_avg_dis]
        walk_out2["Avg_speed"] = [walk_avg_vel]
        walk_out2["Avg_stride_time"] = [walk_avg_time]
        walk_out2["Avg_swing"] = [walk_avg_swing]
        walk_out2["Avg_stance"] = [walk_avg_stance]
        walk_out2["Avg_cadence"] = [walk_cadence]
        walk_out2["Activity"] = ["Level ground walking"]
    else:
        walk_out2['Total_strides']=[0]
        walk_out2["Activity"] = ["Level ground walking"]

    if (len(lst_activity[1]) > 2000):
        asc_dis = []
        asc_vel = []
        asc_mode = []
        asc_time = []
        asc_swing = []
        asc_stance = []
        rampAscent = activity_intervals(lst_activity[1], fs, fc, 2)
        for i in range(len(rampAscent)):
            peaks, _ = find_peaks(rampAscent[i], height=1.9)
            local_min = argrelextrema(rampAscent[i], np.less)[0]
            IC_points, TO_points = find_IC(peaks, local_min)
            maxx = max(len(IC_points), len(TO_points))
            j = 0
            if (maxx > 1):
                if (TO_points[0] < IC_points[0] and len(TO_points) > 1):
                    for k in range(len(TO_points) - 1):
                        start = TO_points[k]
                        end = TO_points[k + 1]
                        stride_time = (end - start) / fs
                        while (IC_points[j] < start):
                            j += 1
                        ic = IC_points[j]
                        swing = (ic - start) / fs / stride_time * 100
                        stance = 100 - swing
                        if (swing < 30 or swing >= 50):
                            continue
                        w = rampAscent[i][start:ic]
                        vel = velocity(w, L, fs) / 0.98
                        if (vel < 0.7):
                            continue
                        dis = vel * stride_time
                        asc_dis.append(round(dis, 2))
                        asc_vel.append(round(vel, 2))
                        asc_mode.append("Ramp ascent")
                        asc_time.append(round(stride_time, 2))
                        asc_swing.append(round(swing, 2))
                        asc_stance.append(round(stance, 2))

                else:
                    for k in range(len(IC_points) - 1):
                        start = IC_points[k]
                        end = IC_points[k + 1]
                        stride_time = (end - start) / fs
                        while (TO_points[j] < start):
                            j += 1
                        to = TO_points[j]
                        swing = (end - to) / fs / stride_time * 100
                        stance = 100 - swing
                        if (swing < 30 or swing >= 50):
                            continue
                        w = rampAscent[i][to:end]
                        vel = velocity(w, L, fs) / 0.98
                        if (vel < 0.7):
                            continue
                        dis = vel * stride_time
                        asc_dis.append(round(dis, 2))
                        asc_vel.append(round(vel, 2))
                        asc_mode.append("Ramp ascent")
                        asc_time.append(round(stride_time, 2))
                        asc_swing.append(round(swing, 2))
                        asc_stance.append(round(stance, 2))

            i += 1

        ascent_strides = len(asc_dis)
        ascent_dis = sum(asc_dis)
        ascent_time = sum(asc_time)
        ascent_avg_dis = round(sum(asc_dis) / ascent_strides, 2)
        ascent_avg_vel = round(sum(asc_vel) / ascent_strides, 2)
        ascent_avg_time = round(sum(asc_time) / ascent_strides, 2)
        ascent_avg_swing = round(sum(asc_swing) / ascent_strides, 2)
        ascent_avg_stance = 100 - ascent_avg_swing
        ascent_cadence = int(ascent_strides * 120 / sum(asc_time))

        ascent_out1['Stride_length'] = asc_dis
        ascent_out1['Speed'] = asc_vel
        ascent_out1['Stride_time'] = asc_time
        ascent_out1['Swing'] = asc_swing
        ascent_out1['Stance'] = asc_stance
        ascent_out1['Activity'] = asc_mode

        ascent_out2["Total_strides"] = [ascent_strides]
        ascent_out2["Total_distance"] = [ascent_dis]
        ascent_out2["Total_time"] = [ascent_time]
        ascent_out2["Avg_stride_length"] = [ascent_avg_dis]
        ascent_out2["Avg_speed"] = [ascent_avg_vel]
        ascent_out2["Avg_stride_time"] = [ascent_avg_time]
        ascent_out2["Avg_swing"] = [ascent_avg_swing]
        ascent_out2["Avg_stance"] = [ascent_avg_stance]
        ascent_out2["Avg_cadence"] = [ascent_cadence]
        ascent_out2["Activity"] = ["Ramp ascent"]
    else:
        ascent_out2['Total_strides'] = [0]
        ascent_out2["Activity"] = ["Ramp ascent"]

    if (len(lst_activity[2]) > 2000):
        des_dis = []
        des_vel = []
        des_mode = []
        des_time = []
        des_swing = []
        des_stance = []
        rampDescent = activity_intervals(lst_activity[2], fs, fc, 3)
        for i in range(len(rampDescent)):
            peaks, _ = find_peaks(rampDescent[i], height=2.2)
            local_min = argrelextrema(rampDescent[i], np.less)[0]
            IC_points, TO_points = find_IC(peaks, local_min)
            maxx = max(len(IC_points), len(TO_points))
            j = 0
            if (maxx > 1):
                if (TO_points[0] < IC_points[0] and len(TO_points) > 1):
                    for k in range(len(TO_points) - 1):
                        start = TO_points[k]
                        end = TO_points[k + 1]
                        stride_time = (end - start) / fs
                        while (IC_points[j] < start):
                            j += 1
                        ic = IC_points[j]
                        swing = (ic - start) / fs / stride_time * 100
                        stance = 100 - swing
                        if (swing < 40 or swing >= 60):
                            continue
                        w = rampDescent[i][start:ic]
                        vel = velocity(w, L, fs) / 0.98
                        if (vel < 0.7):
                            continue
                        dis = vel * stride_time
                        des_dis.append(round(dis, 2))
                        des_vel.append(round(vel, 2))
                        des_mode.append("Ramp descent")
                        des_time.append(round(stride_time, 2))
                        des_swing.append(round(swing, 2))
                        des_stance.append(round(stance, 2))

                else:
                    for k in range(len(IC_points) - 1):
                        start = IC_points[k]
                        end = IC_points[k + 1]
                        stride_time = (end - start) / fs
                        while (TO_points[j] < start):
                            j += 1
                        to = TO_points[j]
                        swing = (end - to) / fs / stride_time * 100
                        stance = 100 - swing
                        if (swing < 40 or swing >= 60):
                            continue
                        w = rampDescent[i][to:end]
                        vel = velocity(w, L, fs) / 0.98
                        if (vel < 0.7):
                            continue
                        dis = vel * stride_time
                        des_dis.append(round(dis, 2))
                        des_vel.append(round(vel, 2))
                        des_mode.append("Ramp descent")
                        des_time.append(round(stride_time, 2))
                        des_swing.append(round(swing, 2))
                        des_stance.append(round(stance, 2))

            i += 1

        descent_strides = len(des_dis)
        descent_dis = sum(des_dis)
        descent_time = sum(des_time)
        descent_avg_dis = round(sum(des_dis) / descent_strides, 2)
        descent_avg_vel = round(sum(des_vel) / descent_strides, 2)
        descent_avg_time = round(sum(des_time) / descent_strides, 2)
        descent_avg_swing = round(sum(des_swing) / descent_strides, 2)
        descent_avg_stance = 100 - descent_avg_swing
        descent_cadence = int(descent_strides * 120 / sum(des_time))

        descent_out1['Stride_length'] = des_dis
        descent_out1['Speed'] = des_vel
        descent_out1['Stride_time'] = des_time
        descent_out1['Swing'] = des_swing
        descent_out1['Stance'] = des_stance
        descent_out1['Activity'] = des_mode

        descent_out2["Total_strides"] = [descent_strides]
        descent_out2["Total_distance"] = [descent_dis]
        descent_out2["Total_time"] = [descent_time]
        descent_out2["Avg_stride_length"] = [descent_avg_dis]
        descent_out2["Avg_speed"] = [descent_avg_vel]
        descent_out2["Avg_stride_time"] = [descent_avg_time]
        descent_out2["Avg_swing"] = [descent_avg_swing]
        descent_out2["Avg_stance"] = [descent_avg_stance]
        descent_out2["Avg_cadence"] = [descent_cadence]
        descent_out2["Activity"] = ["Ramp descent"]
    else:
        descent_out2['Total_strides'] = [0]
        descent_out2["Activity"] = ["Ramp descent"]

    data_out1 = pd.concat([walk_out1, ascent_out1, descent_out1], ignore_index=True)
    data_out2 = pd.concat([walk_out2, ascent_out2, descent_out2,stair_ascent_out2,stair_descent_out2], ignore_index=True)
    data_out1['msa'] = data_out1['Speed'].rolling(window=5).mean()
    data_out1['mast'] = data_out1['Stride_length'].rolling(window=5).mean()
  
    return large_list, data_out1, data_out2
