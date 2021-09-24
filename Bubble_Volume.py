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
#matplotlib.use('pdf')

# yt related
import yt
from yt.visualization.api import get_multi_plot

# Costom plugins
import My_Plugin as M

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
Myr2s = 3.1556926e13 # s

def t_sync(E):
    # Synchrotron time scale in https://www.mpi-hd.mpg.de/personalhomes/frieger/HEA5.pdf
    # E is in unit of eV
    m_e = 9.11e-28 # g
    c = 29979245800 # cm/s
    gamma = E*1.6e-12/m_e/c**2
    B = 1e-6 # G
    tau = 7.8e8/B**2/gamma/Myr2s
    return tau # In Myr 

Frames = np.arange(1,51)
V = np.ones(len(Frames))
P = np.ones(len(Frames))
PCR = np.ones(len(Frames))
Syn = np.ones(len(Frames))
Fraction = np.ones(len(Frames))

for frame in tqdm(Frames):
    V[frame-1]   = M.Bub_Volume(    DataSet[0][frame-1], BubbleDef=BubbleDef)
    P[frame-1]   = M.Bub_Pressure(  DataSet[0][frame-1], BubbleDef=BubbleDef)
    PCR[frame-1] = M.Bub_PCR(       DataSet[0][frame-1], BubbleDef=BubbleDef)
    Syn[frame-1] = M.Sync_InBub(    DataSet[0][frame-1], BubbleDef=BubbleDef)
    #Fraction[frame-1] = M.CR_Ratio( DataSet[0][frame-1], BubbleDef=BubbleDef)

dVdt = np.gradient(V, Frames*2*Myr2s)
dPCRdt = np.gradient(PCR, Frames*2*Myr2s)
#print(P)
#print(V)
#print(dV)
PCRdVdt = PCR*dVdt
VdPCRdt = V*dPCRdt
dPV = PCRdVdt + VdPCRdt

ax.plot(Frames, PCRdVdt, color='k', label='$P_{cr}dV/dt (erg/s)$')
ax.plot(Frames, VdPCRdt, color='b', label='$VdP_{cr}/dt (erg/s)$')
ax.plot(Frames, dPV,     color='r', label='$d(PV) (erg/s)$')
ax.plot(Frames, Syn,     color='g', label='Synchrotron cooling (erg/s)')
plt.yscale("symlog")
plt.legend()
fig.savefig("Bubble_Volume.png", dpi=300)
#plt.show()
