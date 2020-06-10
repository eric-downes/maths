import time
import numpy as np

N = 1000

def box(N=N,vec=False):
    if vec:
        k = int(N*2.5)
        ret = np.array([])
        while ret.shape[0]<N:
            a = 2*np.random.random([k,3])-1
            ok = (a**2).sum(axis=1) <= 1
            if ok.sum()>=N: 
                return a[ok]
            ret = np.r_[ ret, a[ok] ] if len(ret)>0 else a[ok]
            k = int( (N-ret.shape[0])*2.5 )
        return ret
    else:
        while True:
            a = 2*np.random.random(3)-1
            if (a**2).sum() <= 1:
                return a

            
def cyl(N=N,vec=False):
    if vec:
        k = int(N*1.7)
        R = np.array([])
        Z = np.array([])
        while len(R)<N:
            a = np.random.random([2,k])        
            z = 2*a[1]-1
            ok = z**2 <= 1 - a[0]
            R = np.append( R, np.sqrt(a[0,ok]) )
            Z = np.append( Z, z[ok] )
            k = int((N-len(R))*1.7)
        T = np.random.random(R.shape[0])
        X = R * np.sin(T)
        Y = R * np.cos(T)
        return np.c_[ X , Y , Z ].T
    else:
        while True:
            a = np.random.random(2)
            z = (2*a[0]-1)
            if z**2 <= 1 - a[1]:
                r = np.sqrt(a[1])
                break
        t = np.random.random()*2*np.pi
        x = r*np.cos(t)
        y = r*np.sin(t)
        return np.r_[x,y,z]


def mull(N=N,vec=False):
    if vec:
        n = np.random.randn(N,3)
        u = np.random.random([N,1])
        d = np.sqrt((n**2).sum(axis=1)).reshape([N,1])
        xyz = n * np.tile( np.cbrt(u)/d , (1,3) )
        return xyz
    else:
        n = np.random.random(3)
        return n * np.cbrt(np.random.random()) / np.sqrt( (n**2).sum() )


def timing():
    tdict = dict()
    funcs = [box,cyl,mull]
    dt1 = []
    dtv = []
    dtsd = []
    for f in funcs:
        t = time.time()
        [f() for i in range(N)]
        dt1.append( time.time() - t )
        tmp=[]
        for i in range(7):
            t = time.time()
            f(vec=True)
            tmp.append( time.time() - t )
        dtv.append( np.mean(tmp) )
        dtsd.append( np.std(tmp) )
        print(f.__name__,str(dt1[-1]),str(dtv[-1]),str(dtsd[-1]))
        tdict[f.__name__] = [str(dt1[-1]),str(dtv[-1]),str(dtsd[-1])]
    return tdict
