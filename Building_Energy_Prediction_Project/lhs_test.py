import numpy as np
from pyDOE import lhs
import matplotlib.pyplot as plt

# 구간을 정의합니다.
lower_bound = 0.13
upper_bound = 1  # 예를 들어, 10개의 구간을 생성하려면 9를 사용합니다.

# Latin Hypercube Sampling을 수행합니다.
num_samples = 1100  # 원하는 샘플 개수
num_dimensions = 1  # 1차원 구간

samples = lhs(num_dimensions, samples=num_samples)

# 구간을 계산하여 값들을 생성합니다.
values = lower_bound + samples * (upper_bound - lower_bound)

# 결과 출력
for val in values:
    print(val[0])

plt.hist(values, bins=50)
plt.xlabel('Value')
plt.ylabel('Frequency')
plt.title('Data Distribution')
plt.show()