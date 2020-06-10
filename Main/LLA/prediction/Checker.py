import pandas as pd

def Check_data_frame(df):
    New = set(df.columns)
    count_row = df.shape[0]
    Old = set(['Right_Shank_Ax', 'Right_Shank_Ay', 'Right_Shank_Az', 'Right_Shank_Gx', 'Right_Shank_Gy', 'Right_Shank_Gz', 'Right_Thigh_Ax', 'Right_Thigh_Ay', 'Right_Thigh_Az', 'Right_Thigh_Gx', 'Right_Thigh_Gy', 'Right_Thigh_Gz', 'Mode'])
    if New == Old and count_row > 1500:
        return True
    else:
        return False
