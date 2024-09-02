import re
import pandas as pd
import jieba
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from emoji import replace_emoji
from collections import Counter
import seaborn as sns
import numpy as np
from PIL import Image

plt.rcParams['font.sans-serif'] = ['SimHei']

# 加载停用词表
stopwords_file = 'stopwords.txt'
with open(stopwords_file, "r", encoding='utf-8') as words:
    stopwords = [i.strip() for i in words]

#中文文本预处理
def segment_text(texts):
    segmented_texts = []
    for text in texts:
        if len(text) == 0:
            continue
        seg_list = ' '.join(jieba.lcut(text, cut_all=True))
        segmented_texts.append(seg_list)
    return segmented_texts

def clean_text(text):
    text = str(text)
    text = re.sub(r"(回复)?(//)?\s*@\S*?\s*(:| |$)", " ", text)  # 去除正文中的@和回复/转发中的用户名
    text = re.sub(r"\[\S+\]", "", text)  # 去除表情符号
    text = replace_emoji(text)
    URL_REGEX = re.compile(
        r'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’]))',
        re.IGNORECASE)
    text = re.sub(URL_REGEX, "", text)  # 去除网址

    # 去除停用词
    for word in stopwords:
        text = text.replace(word, '')
    text = re.sub(r"\s+", " ", text)  # 合并正文中过多的空格
    text = text.strip().replace(' ', '')  # 去除空格
    return text.strip()

# 绘制词云图
def generate_wordcloud(text):
    wordcloud = WordCloud(font_path="simhei.ttf",
                          background_color='white',
                          width=800,  # 增加宽度
                          height=600  # 增加高度
                          ).generate(text)
    plt.figure(figsize=(10, 10))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()

# 词频统计
def plot_word_frequency(text):
    word_list = jieba.cut(text)
    word_list = [word for word in word_list if word.strip()]
    word_counter = Counter(word_list)
    word_freq = word_counter.most_common(20)  # 取出现频率最高的前20个词语及其频次
    words, freqs = zip(*word_freq)

    plt.figure(figsize=(10, 8))
    plt.bar(words, freqs)
    plt.xticks(rotation=45)
    plt.xlabel('词语')
    plt.ylabel('频次')
    plt.title('笔记内容词语频次图')
    plt.show()


data = pd.read_csv('春晚新_hot03.csv')

wb_content = data['_text']

# 数据清洗
wb_content = wb_content.apply(clean_text)

# 对微博内容进行分词
segment_content = segment_text(wb_content)

# 绘制词云图
content_text = ' '.join(segment_content)
generate_wordcloud(content_text)

ip_location = data['_region']
value_counts = ip_location.value_counts()[:10]

pie_labels = value_counts.index
colors = plt.cm.Pastel1(np.linspace(0, 1, len(value_counts)))  # 使用Pastel1颜色映射

plt.figure(figsize=(8, 8))  # 设置画布大小
plt.pie(value_counts.values,
        labels=pie_labels,
        autopct='%1.1f%%',  # 显示百分比
        colors=colors,  # 添加颜色
        startangle=140,  # 开始角度
        textprops={'fontsize': 12})  # 设置文本属性为适中的字体大小

plt.title("关键词中IP属地的占比", fontsize=14, fontweight='bold')  # 设置标题和字体大小
plt.show()
