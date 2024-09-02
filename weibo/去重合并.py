import pandas as pd

# # 假设你的CSV文件路径是'春晚.csv'
# file_path = '春晚1.8k - 副本.csv'
#
# # 读取CSV文件
# df = pd.read_csv(file_path)
#
# # 去除重复行
# df_unique = df.drop_duplicates()
#
# # 保存去重后的数据到新的CSV文件，如果想覆盖原文件，直接用原文件名即可
# df_unique.to_csv('春晚1.8k_去重.csv', index=False)



# 设置CSV文件路径
file_path1 = '春晚overal.csv'
file_path2 = '春晚新_hot02.csv'

# 读取两个CSV文件
df1 = pd.read_csv(file_path1)
df2 = pd.read_csv(file_path2)

# 合并DataFrame，并去除重复项
df_combined = pd.concat([df1, df2]).drop_duplicates()

# 保存合并后的数据到新的CSV文件
df_combined.to_csv('春晚新_hot03.csv', index=False)
