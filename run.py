from BatAlgorithm import *


def fungsi(d):
    jum = 0
    for i in range(len(d)):
        jum = jum + (d[i]*d[i])
    return jum

### Added Michalewicz Function

def Michalewicz(pos):
    result = 0.0
    for i in range(0 , len(pos)):
        a = math.sin(pos[i])
        b = math.sin(((i+1) * pos[i] * pos[i] ) / math.pi)
        c = math.pow(b , 20)
        result += a*c
    return -1.0 * result


ba = BatAlgorithm(2,1000,10000,0.1,0.95,0.95,0,1,-1,1,fungsi)
#ba = BatAlgorithm(5,50,1000,0.10,0.95,0.95,0,1,0,np.pi,Michalewicz) ## Michalewicz

ba.proses_ba()
