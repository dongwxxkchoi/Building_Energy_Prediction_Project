from pyDOE import lhs
import pandas as pd
import os
import random
import numpy as np
import change

columns = ['열관류율(외벽)','열관류율(지붕)','열관류율(바닥)','열관류율(창호)','창면적비','실내 냉방 설정 온도','실내 난방 설정 온도','재실밀도','기기밀도','조명밀도','침기율']


def sampling(res=False):
    # 파라미터 범위
    # 열관류율(외벽), 열관류율(지붕(Off, Ret)), 열관류율(지붕(Res)), 열관류율(바닥), 열관류율(창호), 창면적비, 실내 냉방 설정 온도, 실내 난방 설정 온도, 재실밀도, 기기밀도, 조명밀도, 침기율

    samples_conductivity = []

    if res is True:
        sheet_names = ['Facade', 'Ground(Res)', 'Roof', 'Window']

    for sheet_name in sheet_names:
        samples = sampling_conductivity(sheet_name)
        samples_conductivity.append(samples)

    param_min = [0.100, 23.3, 20.0, 6.0, 10.0, 4.0, 0.100]
    param_max = [1.000, 26.0, 23.2, 15.0, 25.0, 24.0, 0.500]

    samples_conductivity = np.array(samples_conductivity)
    # LHS 샘플링 수행
    samples = lhs(len(param_min), samples=1000)  # samples는 (n_samples, n_dimensions) 크기의 배열

    # 실제 파라미터 값을 계산
    samples_non_conductivity = []
    for i in range(len(samples)):
        param_value = [param_min[j] + samples[i][j] * (param_max[j] - param_min[j]) for j in range(len(param_min))]
        samples_non_conductivity.append(param_value)

    if len(samples_non_conductivity) == 1:
        samples_non_conductivity = samples_non_conductivity[0]

    samples_non_conductivity = np.array(samples_non_conductivity).T
    total_samples = np.concatenate((samples_conductivity, samples_non_conductivity), axis=0).T

    return total_samples

def sampling_conductivity(sheet_name):
    interval_path = 'data/lhs_sample/interval.xlsx'

    df = pd.read_excel(interval_path, sheet_name=sheet_name, header=None)

    interval_start = df[0].iloc[0:50].tolist()
    interval_end = df[0].iloc[1:51].tolist()

    samples = lhs(len(interval_start), samples=20)  # samples는 (n_samples, n_dimensions) 크기의 배열
    # 실제 파라미터 값을 계산
    parameter_values = []
    for i in range(len(samples)):
        param_value = [interval_start[j] + samples[i][j] * (interval_end[j] - interval_start[j]) for j in range(len(interval_start))]
        parameter_values.append(param_value)

    if len(parameter_values) == 1:
        parameter_values = parameter_values[0]

    parameter_values = [item for sublist in parameter_values for item in sublist]
    random.shuffle(parameter_values)

    return parameter_values


def samples_to_csv(template_name):
    folder_path = "./data"
    file_name = "samples_" + template_name + ".csv"
    file_path = os.path.join(folder_path, file_name)
    columns = ['열관류율(외벽)','열관류율(지붕)','열관류율(바닥)','열관류율(창호)','창면적비','실내 냉방 설정 온도','실내 난방 설정 온도','재실밀도','기기밀도','조명밀도','침기율']
    total_samples = sampling(res=True)
    df = pd.DataFrame(total_samples, columns=columns)
    df.to_csv(file_path, encoding='utf-8', index=False)


keys = ['Boston_Off_0', 'Boston_Ret_0', 'Boston_Res_0_Masonry']
samples_to_csv(keys[0])