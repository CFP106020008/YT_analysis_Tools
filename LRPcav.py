import numpy as np
import yt
import matplotlib
matplotlib.use('pdf')
import matplotlib.pyplot as plt
import My_Plugin as M
from matplotlib import rc_context
#from matplotlib.animation import FuncAnimation
from mpl_toolkits.axes_grid1 import AxesGrid
import multiprocessing as mp
import multiprocessing.managers as mpman
import time
import os

# Load datas
Datas = M.Load_Simulation_Datas()
Datas_to_use = ['CReS_SE', 'CRpS']
DataSet = [Datas[i] for i in Datas_to_use]
Titles = ['CReS_SE', 'CRpS']

# Set parameters
BubbleDef = 9.47e16
Myr2s = 3.1556952e13
E_jet = 5.e45*10*Myr2s

def E_cav(dataset, BubbleDef, radius=50):
    ds = dataset
    sp = ds.sphere(ds.domain_center, (radius, "kpc"))
    Bub = ds.cut_region(sp, ["obj['cooling_time'] > {}".format(BubbleDef)])
    E_CR = Bub.quantities.total_quantity("CR_energy_incell")
    E_th = Bub.quantities.total_quantity("Thermal_Energy")
    E_k  = Bub.quantities.total_quantity("Kinetic_Energy")
    return E_CR + E_th + E_k

def Total_Energy(Data):
    return np.sum(Data, axis=1) 

D1 = np.load("/data/yhlin/E_EVO/EEVO_CReS_SE.npy")
D2 = np.load("/data/yhlin/E_EVO/EEVO_CRpS.npy")

t = np.linspace(0, 100, 51, endpoint=True)
'''
for i, Datas in enumerate(DataSet):
    E_Bub = []
    for frame in range(len(Datas)):
        E_Bub.append(E_cav(Datas[frame], BubbleDef))
    plt.plot(t, E_Bub, label='{}'.format(Titles[i]))
    plt.hlines(E_jet, 0, 100*Myr2s, linestyle='dotted', label='Jet Energy')
'''
E_Bub1 = Total_Energy(D1[1,:,:])
E_Bub2 = Total_Energy(D2[1,:,:])

plt.semilogy(t, E_Bub1, label='{}'.format(Titles[0]))
plt.semilogy(t, E_Bub2, label='{}'.format(Titles[1]))
plt.hlines(E_jet, 0, 100, linestyle='dotted', label='Jet Energy')
plt.legend()
plt.xlabel("Time (Myr)")
plt.ylabel("Energy (erg)")
plt.savefig("Ecav.png")



