# This code is used to identify when to switch the 
# Emax and Emin evolution method from adiabatic expansion to 
# Synchrotron cooling.

# General stuff
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

# For drawing
import matplotlib.colorbar as cb
import matplotlib.ticker as ticker
import matplotlib
from matplotlib import rc_context
from matplotlib.colors import LogNorm, SymLogNorm
matplotlib.use('pdf')

# yt related
import yt
from yt.visualization.api import get_multi_plot

# Costom plugins
import My_Plugin as M

# Multiprocessing
import multiprocessing as mp
import multiprocessing.managers as mpman

# Loading data
Datas = M.Load_Simulation_Datas()
Datas_to_use = ['CRe','CReS']
DataSet = [Datas[i] for i in Datas_to_use]
Titles = [r'$\mathrm{CRe}$',r'$\mathrm{CReS}$']

# Some setting
fig, ax = plt.subplots()
width = (50, 'kpc')
res = [500, 500]
BubbleDef = 9.47e16

# For multiprocessing
n_process = 10
class MyManager(mpman.BaseManager):
    pass
MyManager.register('np_ones', np.ones, mpman.ArrayProxy)
m = MyManager()
m.start()


def t_sync(E):
    # Synchrotron time scale in https://www.mpi-hd.mpg.de/personalhomes/frieger/HEA5.pdf
    # E is in unit of eV
    m_e = 9.11e-28 # g
    c = 29979245800 # cm/s
    Myr2s = 31556926e6 # s
    gamma = E*1.6e-12/m_e/c**2
    B = 1e-6 # G
    tau = 7.8e8/B**2/gamma/Myr2s
    return tau # In Myr 


def t_a_mean(ds):
    sp = ds.sphere(ds.domain_center, width)
    slc = ds.slice('x', 0.5, data_source=sp)
    frb = slc.to_frb(width, res)
    Adia_Map = frb["adiabatic_time"].d
    #print('Original mean:', np.mean(Adia_Map))
    #Adia_Map = np.array(yt.SlicePlot(ds, 'x', fields = ["adiabatic_time"], data_source=sp).data_source.to_frb(width, res)["adiabatic_time"])
    #Bubble = np.array(yt.SlicePlot(ds, 'x', fields = ["cooling_time"], data_source=sp).data_source.to_frb(width, res)["cooling_time"])
    Bubble = frb["cooling_time"].d
    Bubble = Bubble<BubbleDef
    Adia_Mean = np.ma.array(Adia_Map, mask=Bubble).mean()
    #print('Masked mean:', Adia_Mean)
    return Adia_Mean

#Frames = [5]
#Frames = [10,20,30,40,50]
Frames = np.arange(1,51)
T_a = m.np_ones(len(Frames))

def assign_frame(start, end):
    for i in range(start, end):
        #print('Frame: ', i)
        T_a[i] = t_a_mean(DataSet[1][Frames[i]])
        print(M.Time(DataSet[1][Frames[i]]))
    return

Pro_List = [] # The list that contains all the processes.
framePP = int((len(Frames) - len(Frames)%(n_process-1))/(n_process-1))
print('framePP', framePP)

for i in range(n_process-1): # Append the processes into the list
    print('Core:', i)
    Pro_List.append(mp.Process(target=assign_frame, args=(i*framePP, (i+1)*framePP)))
Pro_List.append(mp.Process(target=assign_frame, args=((n_process-1)*framePP, len(Frames))))

for p in Pro_List: # Start running
    p.start()

for p in Pro_List: # Wait for all the processes to finish before moving on
    p.join()

ax.plot(Frames, T_a, label='Mean Adiabatic Time scale', color='b')
ax.hlines(t_sync(1e11), 0, 50, label='100 GeV', color='r')
ax.hlines(t_sync(1e12), 0, 50, label='1 TeV'  , color='g')
plt.legend()
plt.savefig("Mean_Adiabatic_Timescale.png", dpi=300)
