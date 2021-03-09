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
path = "/data/yhlin/E_EVO"
files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
DataSet = [np.load(os.path.join(path, i), allow_pickle=True) for i in files]
Names = ['_'.join(''.join(f.split('.')[:-1]).split('_')[1:]) for f in files]

# Set parameters
BubbleDef = 9.47e16
Myr2s = 3.1556952e13
E_jet = 5.e45*10*Myr2s
'''
def E_cav(dataset, BubbleDef, radius=50):
    ds = dataset
    sp = ds.sphere(ds.domain_center, (radius, "kpc"))
    Bub = ds.cut_region(sp, ["obj['cooling_time'] > {}".format(BubbleDef)])
    #E_CR = Bub.quantities.total_quantity("CR_energy_incell")
    #E_th = Bub.quantities.total_quantity("Thermal_Energy")
    #E_k  = Bub.quantities.total_quantity("Kinetic_Energy")
    PV =   Bub.quantities.total_quantity("Work_By_Bubble")
    return PV# + E_CR + E_th + E_k
'''
def Total_Energy(Data):
    return np.sum(Data, axis=1) 

#D1 = np.load("/data/yhlin/E_EVO/EEVO_CReS_SE.npy")
#D2 = np.load("/data/yhlin/E_EVO/EEVO_CRpS.npy")

t = np.linspace(0, 100, 51, endpoint=True)
for i, Datas in enumerate(DataSet):
    E_Bub = []
    for frame in range(np.shape(Datas)[1]):
        E_Bub.append(Total_Energy(Datas[1,:,:])[frame])
    plt.semilogy(t, E_Bub, label='{}'.format(Names[i]))
    #plt.hlines(E_jet, 0, 100*Myr2s, linestyle='dotted', label='Jet Energy')

#plt.semilogy(t, E_Bub1, label='{}'.format(Titles[0]))
#plt.semilogy(t, E_Bub2, label='{}'.format(Titles[1]))
plt.hlines(E_jet, 0, 100, linestyle='dotted', label='Jet Energy')
plt.legend()
plt.xlabel("Time (Myr)")
plt.ylabel("Energy (erg)")
plt.ylim([1e58, 1e61])
plt.savefig("Ecav.png", dpi=300)



