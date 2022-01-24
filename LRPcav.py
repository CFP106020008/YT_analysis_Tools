import numpy as np
import yt
import matplotlib
matplotlib.use('pdf')
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import My_Plugin as M
from matplotlib import rc_context
from mpl_toolkits.axes_grid1 import AxesGrid
import multiprocessing as mp
import multiprocessing.managers as mpman
import time
import os
import pandas as pd

# Load datas
Datas_to_use = ['CRe', 'CReS', 'CRp', 'CRpS']
EEVODatas = [M.Load_E_EVO_Data()[i] for i in Datas_to_use]

# Set parameters
Myr2s = 3.1556952e13
E_jet = 5.e45*10*Myr2s
nu = 1.51e8 # Hz
def Total_Energy(Data):
    return np.sum(Data, axis=1) 

# Here we simply want to use part of the colormap
def truncate_colormap(cmap, minval=0.0, maxval=1.0, n=100):
    new_cmap = colors.LinearSegmentedColormap.from_list(
        'trunc({n},{a:.2f},{b:.2f})'.format(n=cmap.name, a=minval, b=maxval),
        cmap(np.linspace(minval, maxval, n)))
    return new_cmap

NBlue = truncate_colormap(plt.get_cmap('Blues'), 0.2, 0.8)
NRed = truncate_colormap(plt.get_cmap('Reds'), 0.2, 0.8)


t = np.linspace(0, 100, 51, endpoint=True)
E_Bub_All = []
LR_All = []
for i in range(len(Datas_to_use)):
    print('Progress: {}'.format(i/len(Datas_to_use)))
    E_Bub = []
    LR_1DS = np.zeros(len(EEVODatas[0]))
    E_Bub_All.append(Total_Energy(EEVODatas[i][1,:,:4]))
    # Note that this is in erg/s/Hz
    if i < 2:
        LR_All.append(EEVODatas[i][2,:,4]) 

fig, ax = plt.subplots(figsize=(6,6))

# We divide it by 1e7 to make erg to W, and 4*pi to make it sr^-1
# These two are for CRe
ax.scatter(LR_All[0][::5]/1e7/4/np.pi, E_Bub_All[0][::5]/1e7/(Myr2s*t[::5]*2), c=t[::5], cmap=NBlue , label=Datas_to_use[0], marker='o')
ax.scatter(LR_All[1][::5]/1e7/4/np.pi, E_Bub_All[1][::5]/1e7/(Myr2s*t[::5]*2), c=t[::5], cmap=NBlue, label=Datas_to_use[1], marker='^')

# These are for CRp
Proton_LR = pd.read_excel('./Data/CRp_Radio_Revised0902.xlsx')
ax.scatter(Proton_LR.loc[::5,'CRp (W/Hz)']/4/np.pi,  E_Bub_All[2][::5]/1e7/(Myr2s*t[::5]*2), c=t[::5], cmap=NRed, label=Datas_to_use[2], marker='o')
ax.scatter(Proton_LR.loc[::5,'CRpS (W/Hz)']/4/np.pi, E_Bub_All[3][::5]/1e7/(Myr2s*t[::5]*2), c=t[::5], cmap=NRed, label=Datas_to_use[3], marker='^')


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
ax.scatter(x = Crotson2017['L151MHz(W/Hz/sr)'], y = Crotson2017['Qjet(W)'], marker = '+')

ax.set_xlabel(r"$L_{151~MHz}~(W~Hz^{-1}~sr^{-1})$")
ax.set_ylabel(r"$Q_{jet}~(W)$")
ax.set_xscale('log')
ax.set_yscale('log')
Xlim = [1e20, 1e28]
ax.set_xlim(Xlim)
ax.set_ylim([5e33, 5e39])

plt.hlines(5e38, Xlim[0], Xlim[1], colors='k', linestyle='dashed')
ax.set_aspect(1)
plt.legend(markerscale=1, scatterpoints=1, loc=4)
legend = ax.get_legend()
legend.legendHandles[0].set_color(plt.cm.Blues(.8))
legend.legendHandles[1].set_color(plt.cm.Blues(.8))
legend.legendHandles[2].set_color(plt.cm.Reds(.8))
legend.legendHandles[3].set_color(plt.cm.Reds(.8))
legend.get_frame().set_alpha(0.5)
plt.savefig("Ecav_10.png", dpi=300)
