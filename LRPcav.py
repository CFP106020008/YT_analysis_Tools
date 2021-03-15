import numpy as np
import yt
import matplotlib
matplotlib.use('pdf')
import matplotlib.pyplot as plt
import My_Plugin as M
from matplotlib import rc_context
from mpl_toolkits.axes_grid1 import AxesGrid
import multiprocessing as mp
import multiprocessing.managers as mpman
import time
import os

# Load datas
Datas_to_use = ['CReS', 'CReS_SE']
EEVODatas = [M.Load_E_EVO_Data()[i] for i in Datas_to_use]
SimDatas  = [M.Load_Simulation_Datas()[i] for i in Datas_to_use]

# Set parameters
BubbleDef = 9.47e16
Myr2s = 3.1556952e13
E_jet = 5.e45*10*Myr2s

def Total_Energy(Data):
    return np.sum(Data, axis=1) 

t = np.linspace(0, 100, 51, endpoint=True)
E_Bub_All = []
LR_All = []
for i in range(len(Datas_to_use)):
    E_Bub = []
    LR_1DS = np.zeros(len(SimDatas[0]))
    for frame in range(len(SimDatas[0])):
        LR_1DS[frame] = M.LR_Total(SimDatas[i][frame])
    E_Bub_All.append(Total_Energy(EEVODatas[i][1,:,:]))
    LR_All.append(LR_1DS)

fig, ax = plt.subplots()

ax.scatter(LR_All[0][1:]*1e7, E_Bub_All[0][1:]*1e7/(Myr2s*t[1:]*2), c=t[1:], cmap='Reds' , label='CReS')
ax.scatter(LR_All[1][1:]*1e7, E_Bub_All[1][1:]*1e7/(Myr2s*t[1:]*2), c=t[1:], cmap='Blues', label='CReS_SE')
ax.set_xlabel(r"$L_{151~MHz}~(W/Hz)$")
ax.set_ylabel(r"$Q_{jet}~(W)$")
ax.set_xscale('log')
ax.set_yscale('log')
ax.set_xlim([1e20, 1e28])
ax.set_ylim([1e33, 1e40])
plt.legend()
plt.savefig("Ecav.png", dpi=300)
