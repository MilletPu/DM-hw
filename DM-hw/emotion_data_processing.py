# -*- encoding: utf8 -*-
import numpy as np
import pandas as pd


def get_major_content(url = '1.ann'):
    file = open(url)
    line_split = [ line.strip().split() for line in file.readlines()]
    T1_name = []  #存放正极性标识[ [T1/T2/T3],... ]
    T2_name = []  #存放负极性标识[ [T1/T2/T3],... ]

    for line in line_split:
        if line[1]=="Positive": T1_name.append([line[2],1]);
        if line[1]=="Negative": T2_name.append([line[2],-1]);
    print T1_name

    content = [] #存放极性内容与极性[ [Claim,-1/1] ,...]
    for line in line_split:
        for idx in range(len(T1_name)):
            if T1_name[idx][0] == line[0]:
                content.append([line[4],T1_name[idx][1]])
        for idx in range(len(T2_name)):
            if T1_name[idx][0] == line[0]:
                content.append([line[4],T2_name[idx][1]])
    data = pd.DataFrame(content,columns = ["content","jixing"])

    file.close()
    return data

if __name__ == "__main___":
    print get_major_content('1.ann')