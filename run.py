from BatAlgorithm import *


def fungsi(d):
    jum = 0
    for i in range(len(d)):
        jum = jum + (d[i]*d[i])
    return jum

ba = BatAlgorithm(2,1000,10000,0.1,0.95,0.95,0,1,-1,1,fungsi)
ba.proses_ba()
