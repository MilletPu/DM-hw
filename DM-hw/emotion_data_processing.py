# -*- encoding: utf8 -*-
import numpy as np
import os
import pandas as pd
import jieba
import re

from sklearn import naive_bayes
from sklearn.feature_extraction.text import CountVectorizer


def get_major_content(url):
    if os.path.exists(url):
        file = open(url)
        line_split = [line.strip().split() for line in file.readlines()]
        file.close()
    else:
        return

    T1_name = []  # 存放正极性标识 [ ['T1' , 1], ['T2', 1],... ]
    T2_name = []  # 存放负极性标识 [ ['T1' , -1], ['T2', -1],... ]
    for line in line_split:
        if len(line) > 1:  # 注意某些行因为数据很脏，所以只有一列（上一列的comment内容换行而来）
            if line[1] == "Positive": T1_name.append([line[2], 1]);
            if line[1] == "Negative": T2_name.append([line[2], -1]);

    content = []  # 存放极性内容与极性 [ ['ClaimContent', -1/1] ,...]
    for line in line_split:
        for idx in range(len(T1_name)):
            if T1_name[idx][0] == line[0]:
                content.append([line[4], T1_name[idx][1]])
        for idx in range(len(T2_name)):
            if T2_name[idx][0] == line[0]:
                content.append([line[4], T2_name[idx][1]])

    return content


def get_all_comments():
    cur = []
    for comment in range(1, 301):
        for i in range(1, 6):
            url = os.getcwd() + '/data/comment_%d/%d.ann' % (comment, i)
            next = get_major_content(url)
            if next is not None:
                cur.extend(next)

    data = pd.DataFrame(cur, columns=["content", "jixing"])
    return data


def cut_all_comments(all_comments):
    segs = []
    for i in range(len(all_comments)):
        a = all_comments.values[i][0].decode('utf-8')
        s = re.sub("[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）]+".decode("utf8"), "".decode("utf8"), a)
        comments_seg = jieba.cut(s)
        segs.extend([" ".join(comments_seg).encode('utf-8')])
    all_comments_seg = pd.DataFrame(segs)

    return all_comments_seg


def get_all_comments_seg_vector(all_comments):
    all_comments_seg = cut_all_comments(all_comments)
    all_comments_seg_vector = []
    for comments_seg in range(len(all_comments_seg)):
        texts = all_comments_seg.values[comments_seg][0]
        all_comments_seg_vector.append(texts)

    return all_comments_seg_vector


def get_all_jixings_vector(all_comments):
    all_jixing = []
    for i in range(len(all_comments)):
        all_jixing.append(all_comments.values[i][1])
    return all_jixing


def predict_jixing(test_comment):
    global pre_jixing
    all_comments = get_all_comments()
    texts = get_all_comments_seg_vector(all_comments)
    jixings = get_all_jixings_vector(all_comments)

    cv = CountVectorizer()
    X_train = cv.fit_transform(texts)
    y_train = jixings
    nb = naive_bayes.MultinomialNB()
    nb.fit(X_train, y_train)

    X_test = cv.fit_transform(texts + [test_comment]) # 训练数据没有'垃圾'这词
    y_predicted = nb.predict(X_test)[-1]

    if y_predicted == 1: pre_jixing = 'Positive'
    if y_predicted == -1: pre_jixing = 'Negative'

    return pre_jixing


if __name__ == "__main__":
    print predict_jixing('酒店 不好')

    # texts = ["dog cat fish", "dog cat cat", "fish bird", 'bird']
    # cv = CountVectorizer()
    # X_train = cv.fit_transform(texts)
    # print X_train
    #
    # y_train = [1,2,3,4]
    # nb = naive_bayes.MultinomialNB()
    #
    # nb.fit(X_train, y_train)
    # y_pre = nb.predict(cv.fit_transform(texts + ["cat fish bird"])) # 必须要有所有的词才可以预测，所以必须平滑
    # print y_pre