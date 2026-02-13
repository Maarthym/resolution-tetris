import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit

lev = np.array([i for i in range(1,16)])
g = np.array([0.01667,0.021017,0.026977,0.035256,0.04693,0.06361,0.0879,0.1236,0.1775,0.2598,0.388,0.59,0.92,1.46,2.36])

def reso(x,a,b,c):
    return a*b**x + c

def func(x):
    return np.exp(x)

plt.figure()
plt.plot(lev,g, label='exp', marker='x', linestyle='none')

reg =  np.polyfit(func(lev), g, 1)
print(reg)
plt.plot(lev, reg[0]*func(lev) + reg[1], label='solution 1 ', marker='+', linestyle='none') # première approximation par visualisation de la courbe

params,_ = curve_fit(reso, lev, g)
print(params)
plt.plot(lev, reso(lev,params[0],params[1],params[2]), marker='o', label='solution finale', linestyle='none') # solution finale
plt.legend()

plt.show()