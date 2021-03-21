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
Datas_to_use = ['CReS_SE_CB_Large', 'CReS_SE_CB_Small']
EEVODatas = [M.Load_E_EVO_Data()[i] for i in Datas_to_use]
SimDatas  = [M.Load_Simulation_Datas()[i] for i in Datas_to_use]

#Ref = plt.imread('./Ref.png')

# Set parameters
Myr2s = 3.1556952e13
E_jet = 5.e45*10*Myr2s

def Total_Energy(Data):
    return np.sum(Data, axis=1) 

t = np.linspace(0, 100, 51, endpoint=True)
E_Bub_All = []
LR_All = []
for i in range(len(Datas_to_use)):
    print('Progress: {}'.format(i/len(Datas_to_use)))
    E_Bub = []
    LR_1DS = np.zeros(len(SimDatas[0]))
    for frame in range(len(SimDatas[0])):
        LR_1DS[frame] = M.LR_Total(SimDatas[i][frame])
        print('Sync: {:.2e} erg/s'.format(LR_1DS[frame]))
    E_Bub_All.append(Total_Energy(EEVODatas[i][1,:,:]))
    LR_All.append(LR_1DS)

fig, ax = plt.subplots()

ax.scatter(LR_All[0][1:]/1e7/4/np.pi, E_Bub_All[0][1:]/1e7/(Myr2s*t[1:]*2), c=t[1:], cmap='Reds' , label=Datas_to_use[0], marker='o')
ax.scatter(LR_All[1][1:]/1e7/4/np.pi, E_Bub_All[1][1:]/1e7/(Myr2s*t[1:]*2), c=t[1:], cmap='Blues', label=Datas_to_use[1], marker='^')
ax.set_xlabel(r"$L_{151~MHz}~(W/Hz)$")
ax.set_ylabel(r"$Q_{jet}~(W)$")
ax.set_xscale('log')
ax.set_yscale('log')
ax.set_xlim([1e20, 1e33])
ax.set_ylim([1e33, 1e40])
plt.hlines(5e38, 1e20, 1e32, colors='k', linestyle='dashed')
#ax.imshow(Ref, zorder=1)
plt.legend()
plt.savefig("Ecav.png", dpi=300, transparent=True)
