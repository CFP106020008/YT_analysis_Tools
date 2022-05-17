import numpy as np
import yt
import threading
import multiprocessing as mp
import multiprocessing.managers as mpman
import time
import matplotlib.pyplot as plt
from matplotlib import rc_context
import My_Plugin as M
import Mock_observe as MO
import matplotlib
import os
matplotlib.use('pdf')

s = time.time()
Datas = M.Load_Simulation_Datas()
Datas_to_use = ['CReS'] #, 'CReS_RC', 'CReS_SE', 'CReS_SE_Small', 'CRp', 'CRe', , 'CRpS''CReS_SE_CB_Small']
DataSet = [Datas[i] for i in Datas_to_use]

Myr2s = 86400*365*1e6

skip_factor = 2
tsim = np.linspace(2, 100, len(DataSet[0][1::skip_factor]) )
'''
for i in range(len(DataSet)):
    fig, ax = plt.subplots()
    tsound   = np.array(list(map(MO.t_sound,  DataSet[i][2::skip_factor])))/Myr2s
    tbouy    = np.array(list(map(MO.t_bouy,   DataSet[i][2::skip_factor])))/Myr2s
    trefill  = np.array(list(map(MO.t_refill, DataSet[i][2::skip_factor])))/Myr2s
    ax.plot(tsim, tsound, label='{}_sound'.format(Datas_to_use[i]))
    ax.plot(tsim, tbouy , label='{}_bouy'.format(Datas_to_use[i]))
    ax.plot(tsim, trefill,label='{}_refill'.format(Datas_to_use[i]))
    ax.plot(tsim, tsim, linestyle='--')
    ax.legend()
    fig.savefig("timescale_{}.png".format(Datas_to_use[i]), dpi=300)
    #os.system("MM Edge_{}".format(Datas_to_use[i]))
    #os.system("rm Edge*.png".format(Datas_to_use[i]))
for i in np.arange(1,50,5):
    print(MO.t_refill(DataSet[0][i],))
    #print(i, MO.bubble_center(DataSet[0][i], plot=True)[1]/3e21)
e = time.time()
print("The code took:", e-s)
'''
print(M.LR_Total(DataSet[0][25]))
