import pandas as pd
import matplotlib.pyplot as plt
import LHS

off_df = pd.read_csv("data/lhs_sample/samples_Boston_Off_0.csv")
res_df = pd.read_csv("data/lhs_sample/samples_Boston_Res_0_Masonry.csv")
ret_df = pd.read_csv("data/lhs_sample/samples_Boston_Ret_0.csv")

# print(off_df.describe())
# print(res_df.describe())
# print(ret_df.describe())

samples = LHS.sampling(res=True)

# plt.hist(off_df['기기밀도'], bins=30)
# plt.hist(off_df['재실밀도'], bins=30)
plt.hist(off_df['열관류율(외벽)'], bins=50)
plt.xlabel('Value')
plt.ylabel('Frequency')
plt.title('Data Distribution')
plt.show()