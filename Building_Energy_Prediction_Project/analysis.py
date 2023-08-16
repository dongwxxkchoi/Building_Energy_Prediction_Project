import pandas as pd
import matplotlib.pyplot as plt
import LHS

off_df = pd.read_csv("data/lhs_sample/samples_Boston_Off_0.csv")
res_df = pd.read_csv("data/lhs_sample/samples_Boston_Res_0_Masonry.csv")
ret_df = pd.read_csv("data/lhs_sample/samples_Boston_Ret_0.csv")

column = ['열관류율(외벽)', '열관류율(지붕)', '열관류율(바닥)', '열관류율(창호)']
print(off_df[column].describe())
print(res_df[column].describe())
print(ret_df[column].describe())

# off_df.loc[0]

# plt.hist(off_df['기기밀도'], bins=30)
# plt.hist(off_df['재실밀도'], bins=30)
plt.figure(figsize=(10, 10))
plt.hist(off_df['열관류율()'], bins=30)
plt.xlabel('Value')
plt.ylabel('Frequency')
plt.title('Data Distribution')
plt.show()