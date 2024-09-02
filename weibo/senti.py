import pandas as pd
from matplotlib import pyplot as plt
from snownlp import SnowNLP

plt.rcParams['font.sans-serif'] = ['SimHei']

# 加载微博数据
data_path = '春晚新_hot02.csv'  # 请替换为您微博数据文件的实际路径
weibo_data = pd.read_csv(data_path)

# 定义一个函数，用于计算文本的情感得分
def get_sentiment_score(text):
    # 检查text是否为字符串类型
    if isinstance(text, str):
        return SnowNLP(text).sentiments
    else:
        # 如果text不是字符串，返回默认情感得分
        # 这里我们返回0.5，表示中性情绪
        return 0.5

# 假设您的微博数据中包含文本内容的列名为'text'，请根据实际情况调整列名
weibo_data['sentiment_score'] = weibo_data['_text'].apply(get_sentiment_score)

# 查看情感得分的前几行以确认
print(weibo_data[['_text', 'sentiment_score']].head())

# 保存含有情感得分的数据到新的CSV文件，以便进一步分析
# output_path = 'data_with_sentiment.csv'  # 请指定输出文件的路径
# weibo_data.to_csv(output_path, index=False)
# 计算平均情感得分
average_sentiment_score = weibo_data['sentiment_score'].mean()
print(f"平均情感得分: {average_sentiment_score}")

# 定义情感类别
weibo_data['sentiment_category'] = pd.cut(weibo_data['sentiment_score'],
                                          bins=[0, 0.4, 0.6, 1],
                                          labels=["负面", "中性", "正面"],
                                          include_lowest=True)

# 统计情感类别分布
sentiment_distribution = weibo_data['sentiment_category'].value_counts(normalize=True) * 100

# 打印情感分布
print(sentiment_distribution)

# 可视化情感分布
sentiment_distribution.plot(kind='bar', title='情感分布')
plt.xlabel('情感类别')
plt.ylabel('百分比')
plt.show()