import pandas as pd
import numpy as np
from tensorflow.keras.models import load_model
from sklearn.preprocessing import StandardScaler
import scipy.stats as stats


Model = load_model(r'C:\Users\user\Desktop\DeskTop\Lower_Limb_Analysis_Website\Main\LLA\prediction\static\prediction\CNN_Triple_version2.h5')


def get_frames(df, frame_size, hop_size):
    N_FEATURES = 12
    frames = []
    labels = []
    for i in range(0, len(df) - frame_size, hop_size):
        x1 = df['Right_Shank_Ax'].values[i: i + frame_size]
        x2 = df['Right_Shank_Ay'].values[i: i + frame_size]
        x3 = df['Right_Shank_Az'].values[i: i + frame_size]
        x4 = df['Right_Shank_Gx'].values[i: i + frame_size]
        x5 = df['Right_Shank_Gy'].values[i: i + frame_size]
        x6 = df['Right_Shank_Gz'].values[i: i + frame_size]
        x7 = df['Right_Thigh_Ax'].values[i: i + frame_size]
        x8 = df['Right_Thigh_Ay'].values[i: i + frame_size]
        x9 = df['Right_Thigh_Az'].values[i: i + frame_size]
        x10 = df['Right_Thigh_Gx'].values[i: i + frame_size]
        x11 = df['Right_Thigh_Gy'].values[i: i + frame_size]
        x12 = df['Right_Thigh_Gz'].values[i: i + frame_size]

        # Retrieve the most often used label in this segment
        label = stats.mode(df['Mode'][i: i + frame_size])[0][0]
        frames.append([x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11, x12])
        labels.append(label)

    # Bring the segments into a better shape
    frames = np.asarray(frames).reshape(-1, frame_size, N_FEATURES)
    labels = np.asarray(labels)

    return frames, labels


def prep(data):
    x = data[['Right_Shank_Ax', 'Right_Shank_Ay', 'Right_Shank_Az', 'Right_Shank_Gx', 'Right_Shank_Gy', 'Right_Shank_Gz', 'Right_Thigh_Ax', 'Right_Thigh_Ay', 'Right_Thigh_Az', 'Right_Thigh_Gx', 'Right_Thigh_Gy', 'Right_Thigh_Gz']]
    y = data['Mode']

    scaler = StandardScaler()
    x = scaler.fit_transform(x)

    scaled_X = pd.DataFrame(data = x, columns = ['Right_Shank_Ax', 'Right_Shank_Ay', 'Right_Shank_Az', 'Right_Shank_Gx', 'Right_Shank_Gy', 'Right_Shank_Gz', 'Right_Thigh_Ax', 'Right_Thigh_Ay', 'Right_Thigh_Az', 'Right_Thigh_Gx', 'Right_Thigh_Gy', 'Right_Thigh_Gz'])
    scaled_X['Mode'] = y.values

    frame_size = 1500 # 200 "2 seconds"
    hop_size = 200 # 1000
    xx, y = get_frames(scaled_X, frame_size, hop_size)

    xx1 = xx[:, :, 0:3]
    xx2 = xx[:, :, 3:6]
    xx3 = xx[:, :, 6:9]
    xx4 = xx[:, :, 9:]

    y_proba = Model.predict([xx1, xx2, xx3, xx4])
    y_pred = y_proba.argmax(axis=-1)

    return y_pred