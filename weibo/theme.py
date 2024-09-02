import pandas as pd
import jieba
import re
from emoji import replace_emoji
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from matplotlib import pyplot as plt
import time

# 确保 matplotlib 支持中文
plt.rcParams['font.sans-serif'] = ['SimHei']
jieba.add_word('马凡舒', freq=None, tag=None)
jieba.add_word('尼格买提', freq=None, tag=None)
jieba.add_word('迪丽热巴', freq=None, tag=None)
jieba.add_word('刘诗诗', freq=None, tag=None)

def load_stopwords(filepath):
    with open(filepath, "r", encoding='utf-8') as file:
        stopwords = set(file.read().splitlines())
    return stopwords

def clean_and_segment_text(text, stopwords):
    # 增强的文本清洗
    text = re.sub(r"(回复)?(//)?\s*@\S*?\s*(:| |$)", " ", text)
    text = re.sub(r"\[\S+\]", "", text)
    text = replace_emoji(text, "")
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"\d+", "", text)  # 去除数字
    text = re.sub(r"[^\u4e00-\u9fa5]", "", text)  # 仅保留中文字符
    seg_list = jieba.cut(text, cut_all=False)
    seg_result = ' '.join([w for w in seg_list if w not in stopwords and len(w) > 1])
    return seg_result

def display_topics(model, feature_names, no_top_words):
    for topic_idx, topic in enumerate(model.components_):
        print(f"Topic {topic_idx}:")
        print(" ".join([feature_names[i] for i in topic.argsort()[:-no_top_words - 1:-1]]))

def main():
    start_time = time.time()

    data = pd.read_csv('春晚新_hot03.csv')
    stopwords = load_stopwords('stopwords.txt')

    data.fillna('', inplace=True)
    data['_text'] = data['_text'].apply(lambda x: clean_and_segment_text(x, stopwords))

    vectorizer = CountVectorizer(max_df=0.85, min_df=2, max_features=1000)
    dtm = vectorizer.fit_transform(data['_text'])

    lda_model = LatentDirichletAllocation(n_components=6, learning_method='batch', max_iter=200, random_state=42)
    lda_model.fit(dtm)

    display_topics(lda_model, vectorizer.get_feature_names_out(), 12)

    end_time = time.time()
    print(f"Total time: {end_time - start_time} seconds")

if __name__ == "__main__":
    main()
