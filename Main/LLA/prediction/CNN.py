import pandas as pd
import numpy as np

from tensorflow import keras
from tensorflow.keras import layers

from sklearn.preprocessing import StandardScaler
import scipy.stats as stats


def create_model():
    input1 = keras.Input(shape=(1500, 3), name='in1')

    x1 = layers.Conv1D(32, 3, activation='relu')(input1)
    x1 = layers.Dropout(0.1)(x1)
    x1 = layers.Conv1D(64, 3, activation='relu')(x1)
    block_1_output = layers.Dropout(0.2)(x1)

    input2 = keras.Input(shape=(1500, 3), name='in2')

    x2 = layers.Conv1D(32, 3, activation='relu')(input2)
    x2 = layers.Dropout(0.1)(x2)
    x2 = layers.Conv1D(64, 3, activation='relu')(x2)
    block_2_output = layers.Dropout(0.2)(x2)

    input3 = keras.Input(shape=(1500, 3), name='in3')

    x3 = layers.Conv1D(32, 3, activation='relu')(input3)
    x3 = layers.Dropout(0.1)(x3)
    x3 = layers.Conv1D(64, 3, activation='relu')(x3)
    block_3_output = layers.Dropout(0.2)(x3)

    input4 = keras.Input(shape=(1500, 3), name='in4')

    x4 = layers.Conv1D(32, 3, activation='relu')(input4)
    x4 = layers.Dropout(0.1)(x4)
    x4 = layers.Conv1D(64, 3, activation='relu')(x4)
    block_4_output = layers.Dropout(0.2)(x4)

    x = layers.concatenate([block_1_output, block_2_output, block_3_output, block_4_output])

    z = layers.Flatten()(x)

    Y = layers.Dense(128, activation='relu')(z)
    Y = layers.Dropout(0.5)(Y)

    output = layers.Dense(7, activation='softmax')(Y)

    model = keras.Model(inputs=[input1, input2, input3, input4], outputs=output)

    model.load_weights(r'prediction\CNN_Triple_weights.h5')

    return model


Model = create_model()


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
    df = data[['Right_Shank_Ax', 'Right_Shank_Ay', 'Right_Shank_Az', 'Right_Shank_Gx', 'Right_Shank_Gy',
                'Right_Shank_Gz', 'Right_Thigh_Ax', 'Right_Thigh_Ay', 'Right_Thigh_Az', 'Right_Thigh_Gx',
                'Right_Thigh_Gy', 'Right_Thigh_Gz']]

    y = data['Mode']

    scaler = StandardScaler()
    xxx = scaler.fit_transform(df)

    scaled_X = pd.DataFrame(data=xxx, columns=['Right_Shank_Ax', 'Right_Shank_Ay', 'Right_Shank_Az', 'Right_Shank_Gx',
                                               'Right_Shank_Gy', 'Right_Shank_Gz', 'Right_Thigh_Ax', 'Right_Thigh_Ay',
                                               'Right_Thigh_Az', 'Right_Thigh_Gx', 'Right_Thigh_Gy', 'Right_Thigh_Gz'])
    scaled_X['Mode'] = y.values

    frame_size = 1500  # 200 "2 seconds"
    hop_size = 200  # 1000
    xx, y = get_frames(scaled_X, frame_size, hop_size)

    xx1 = xx[:, :, 0:3]
    xx2 = xx[:, :, 3:6]
    xx3 = xx[:, :, 6:9]
    xx4 = xx[:, :, 9:]

    y_proba = Model.predict([xx1, xx2, xx3, xx4])
    y_pred = y_proba.argmax(axis=-1)

    big_list = []
    flag = 0
    x = 0
    for i in y_pred:
        if flag == 0:
            for m in range(1100):
                big_list.append(i)
                flag = 1
        for j in range(200):
            big_list.append(i)
        x = i
    for k in range(xxx.shape[0] - len(big_list)):
        big_list.append(x)

    df = pd.DataFrame(data=df['Right_Shank_Gy'], columns=['Right_Shank_Gy'])
    df['Mode'] = big_list

    return df
