import pandas as pd
import numpy as np
import random

def stochastique(A):
    for i in range(np.shape(A)[0]):
        somme = sum(A[i,:])
        for j in range(np.shape(A)[1]):
            if somme == 0:
                A[i][j] = 0
            else : 
                A[i][j] = A[i][j]/somme
    return np.transpose(A)

def PageRank(beta, A):
    P = stochastique(A) 
    n = np.shape(P)[0]
    v = np.transpose(np.full(shape = n, fill_value = 1/n))
    eT = np.ones(shape = n)
    Q = np.dot(v, eT)
    R = np.dot(beta, P) + np.dot((1-beta),Q)/n
    x = np.zeros(shape = n)
    x[random.randint(0,n-1)] = 1
    
    for i in range (10):
        x = np.dot(R, x)
    return x


def printTopValues(x):
    sorted_list = sorted(x, reverse=True)
    top_5 = sorted_list[:5] 

    finalPrint = []
    for elem in top_5:
        index = [i for i in range(len(x)) if x[i] == elem]
        key = [k for k,v in keyIndex.items() if v == index[0]]
        finalPrint.append([key[0],elem])
    
    print(finalPrint)


df = pd.read_csv("/home/anas/VS/C#/TP Big Data/TP Big Data/wikispeedia_paths-and-graph/paths_finished.tsv", sep="\t", skiprows=15)

paths = list(df['path'].values)

global_list = []
keyIndex = []

for string in paths:
    global_list.extend(string.split(';'))

global_list  = dict.fromkeys(global_list)
keyIndex = dict.fromkeys(global_list)
keys = list(global_list.keys())

global_list.pop('<')
keyIndex.pop('<')
keys.remove('<')
 
global_list = dict(sorted(global_list.items()))
keyIndex = dict(sorted(global_list.items()))
keys = list(global_list.keys())

index = 0
for key in keys:
    global_list[key] = []
    keyIndex[key] = index
    index = index+1


paths = [i.split(";") for i in paths]


for j in range(len(paths)):
    i = 0
    while(i < len(paths[j]) -1):
        while(paths[j][i] == '<'):
            paths[j].remove(paths[j][i])
            paths[j].remove(paths[j][i-1])
            i-=2

        if (paths[j][i] != '<' and paths[j][i+1] != '<' and i < len(paths[j]) - 1 and paths[j][i+1] not in global_list[paths[j][i]]):
            global_list[paths[j][i]].append(paths[j][i+1])
        i+=1
        

A = np.zeros(shape = (len(global_list),len(global_list)), dtype=float)

for i in range(len(global_list)):
    for elt in global_list[keys[i]]:
        A[i][keyIndex[elt]] = 1

x = PageRank(0.85, A)



printTopValues(x)












