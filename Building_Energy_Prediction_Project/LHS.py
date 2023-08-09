from pyDOE import lhs
import pandas as pd
import os

def sampling(n_samples, template_name):
    # 파라미터 범위
    # 열관류율(외벽), 열관류율(지붕), 열관류율(바닥), 열관류율(창호), 창면적비, 실내 냉방 설정 온도, 실내 난방 설정 온도, 재실밀도, 기기밀도, 조명밀도, 침기율
    param_min = [0.130, 0.130, 0.170, 0.630, 0.100, 23.3, 20.0, 6.0, 10.0, 4.0, 0.100]  # 예시: 첫 번째 파라미터의 최솟값, 두 번째 파라미터의 최솟값
    param_max = [1.000, 1.000, 1.000, 6.000, 1.000, 26.0, 23.2, 15.0, 25.0, 24.0, 0.500]  # 예시: 첫 번째 파라미터의 최댓값, 두 번째 파라미터의 최댓값

    # LHS 샘플링 수행
    samples = lhs(len(param_min), samples=n_samples)  # samples는 (n_samples, n_dimensions) 크기의 배열

    # 실제 파라미터 값을 계산
    parameter_values = []
    for i in range(len(samples)):
        param_value = [param_min[j] + samples[i][j] * (param_max[j] - param_min[j]) for j in range(len(param_min))]
        parameter_values.append(param_value)

    if len(parameter_values) == 1:
        parameter_values = parameter_values[0]

    # return parameter_values
    sample_df = pd.DataFrame(parameter_values)
    sample_df.columns = ['열관류율(외벽)', '열관류율(지붕)', '열관류율(바닥)', '열관류율(창호)', '창면적비',
                         '실내 냉방 설정 온도', '실내 난방 설정 온도', '재실밀도', '기기밀도', '조명밀도', '침기율']

    folder_path = "./data"
    file_name = "samples_"+template_name+".csv"
    file_path = os.path.join(folder_path, file_name)

    sample_df.to_csv(file_path, encoding='utf-8', index=False)