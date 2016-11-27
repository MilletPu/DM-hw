# -*- encoding: utf8 -*-
import numpy as np
import os
import pandas as pd


def get_major_content(url):
    if os.path.exists(url):
        file = open(url)
        line_split = [line.strip().split() for line in file.readlines()]
        file.close()
    else:
        return

    T1_name = []  #存放正极性标识[ [T1/T2/T3],... ]
    T2_name = []  #存放负极性标识[ [T1/T2/T3],... ]
    for line in line_split:
        if line[1]=="Positive": T1_name.append([line[2],1]);
        if line[1]=="Negative": T2_name.append([line[2],-1]);

    content = [] #存放极性内容与极性[ [Claim,-1/1] ,...]
    for line in line_split:
        for idx in range(len(T1_name)):
            if T1_name[idx][0] == line[0]:
                content.append([line[4],T1_name[idx][1]])
        for idx in range(len(T2_name)):
            if T2_name[idx][0] == line[0]:
                content.append([line[4],T2_name[idx][1]])

    data = pd.DataFrame(content, columns = ["content","jixing"])
    return data

if __name__ == "__main__":

    df = 0
    for i in range(1,10):
        url = '%d.ann'%i
        next = get_major_content(url)
        if df == 0: df = next
        if next is not None:
            merge = [next, df]
            print pd.concat(merge)