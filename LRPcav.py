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
import pandas as pd

# Load datas
Datas_to_use = ['CRe', 'CReS']
EEVODatas = [M.Load_E_EVO_Data()[i] for i in Datas_to_use]

# Set parameters
Myr2s = 3.1556952e13
E_jet = 5.e45*10*Myr2s
nu = 1.51e8 # Hz
def Total_Energy(Data):
    return np.sum(Data, axis=1) 

t = np.linspace(0, 100, 51, endpoint=True)
E_Bub_All = []
LR_All = []
for i in range(len(Datas_to_use)):
    print('Progress: {}'.format(i/len(Datas_to_use)))
    E_Bub = []
    LR_1DS = np.zeros(len(EEVODatas[0]))
    #for frame in range(40,41):#len(SimDatas[0])):
    #    LR_1DS[frame] = M.LR_Total(SimDatas[i][frame])
    #    print(LR_1DS[frame])
    #LR_All.append(LR_1DS)
    E_Bub_All.append(Total_Energy(EEVODatas[i][1,:,:4]))
    # Here we divide it by nu to make it d\epsilon/d\nu
    # Note that this is in erg/s/Hz
    LR_All.append(EEVODatas[i][2,:,4]/nu) 

fig, ax = plt.subplots(figsize=(6,6))

# We divide it by 1e7 to make erg to W, and 4*pi to make it sr^-1

ax.scatter(LR_All[0][1:]/1e7/4/np.pi, E_Bub_All[0][1:]/1e7/(Myr2s*t[1:]*2), c=t[1:], cmap='Reds' , label=Datas_to_use[0], marker='o')
ax.scatter(LR_All[1][1:]/1e7/4/np.pi, E_Bub_All[1][1:]/1e7/(Myr2s*t[1:]*2), c=t[1:], cmap='Blues', label=Datas_to_use[1], marker='^')

# Observation datas from Ineson2017.
'''
Ineson2017 = pd.read_csv('./Obs_Data/Ineson2017.csv')
ax.scatter(x = 10**Ineson2017['log10L151'], y = Ineson2017['Qjet']*1e44/1e7, marker='*')
ax.errorbar(x = 10**Ineson2017['log10L151'], 
            y = Ineson2017['Qjet']*1e44/1e7,
            yerr = Ineson2017['Qjet_Error']*1e44/1e7,
            ls = 'none')
'''
# Observation datas from Crotson2017.
Crotson2017 = pd.read_excel('./Obs_Data/Crotson2017.xlsx')
ax.scatter(x = Crotson2017['L151MHz(W/Hz/sr)'], y = Crotson2017['Qjet(W)'], marker = 'o')

ax.set_xlabel(r"$L_{151~MHz}~(W~Hz^{-1}~sr^{-1})$")
ax.set_ylabel(r"$Q_{jet}~(W)$")
ax.set_xscale('log')
ax.set_yscale('log')
Xlim = [1e20, 1e28]
ax.set_xlim(Xlim)
ax.set_ylim([5e33, 5e39])

# 
plt.hlines(5e38, Xlim[0], Xlim[1], colors='k', linestyle='dashed')
ax.set_aspect(1)
plt.legend()
plt.savefig("Ecav.png", dpi=300)
