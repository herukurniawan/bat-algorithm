from BatAlgorithm import *


def fungsi(d):
    jum = 0
    for i in range(len(d)):
        jum = jum + d[i]
    return jum

ba = BatAlgorithm(2,10,1,0.1,0.95,0.95,0,1,0,100,fungsi)
ba.proses_ba()
