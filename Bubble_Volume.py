# This code is used to identify when to switch the 
# Emax and Emin evolution method from adiabatic expansion to 
# Synchrotron cooling.

# General stuff
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
from scipy.integrate import solve_ivp

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
Datas_to_use = ['CRe_Expansion','CReS']
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

Frames = np.arange(0,len(DataSet[0]))
V = np.ones(len(Frames))
P = np.ones(len(Frames))
PCR = np.ones(len(Frames))
Syn = np.ones(len(Frames))
Fraction = np.ones(len(Frames))

for frame in tqdm(Frames):
    V[frame]   = M.Bub_Volume(DataSet[0][frame], BubbleDef=BubbleDef)
    #P[frame-1]   = M.Bub_Pressure(  DataSet[0][frame-1], BubbleDef=BubbleDef)
    #PCR[frame-1] = M.Bub_PCR(       DataSet[0][frame-1], BubbleDef=BubbleDef)
    #Syn[frame-1] = M.Sync_InBub(    DataSet[0][frame-1], BubbleDef=BubbleDef)
    #Fraction[frame-1] = M.CR_Ratio( DataSet[0][frame-1], BubbleDef=BubbleDef)

Time = np.linspace(0,10,len(Frames))
dVdt = np.gradient(V, Time)
ER = dVdt/3/V # Expansion rate 
#ax.plot(Time, V)
ax.plot(Time, ER)
print(V)
#dPCRdt = np.gradient(PCR, Frames*2*Myr2s)
#PCRdVdt = PCR*dVdt
#VdPCRdt = V*dPCRdt
#dPV = PCRdVdt + VdPCRdt

#ax.plot(Frames, PCRdVdt, color='k', label='$P_{cr}dV/dt (erg/s)$')
#ax.plot(Frames, VdPCRdt, color='b', label='$VdP_{cr}/dt (erg/s)$')
#ax.plot(Frames, dPV,     color='r', label='$d(PV) (erg/s)$')
#ax.plot(Frames, Syn,     color='g', label='Synchrotron cooling (erg/s)')
#plt.yscale("symlog")
#plt.legend()
#plt.plot(Frames, V)
#fig.savefig("Bubble_Volume.png", dpi=300)

#=============================================#

# This code use CGS!

sigma_T = 6.65e-25 # cm^2
m_e = 9.11e-28 # g
c = 29979245800. # cm/s
Myr = 3.16e13 # s/yr
GeV = 0.00160217662 # erg/GeV
B = 1 # micro gauss, simple assumption
gamma = 2.5 # cp/cv
z = 0 # redshift?

# From the OOO_unsplitUpdate.F90 
Urad = 4.2e-13*(1.+z)**4.
Ub = 4.e-14*B**2.
Utot = Urad + Ub

# From Yang & Ruszkowski (2018)
beta = 4/3*sigma_T/(m_e**2*c**3)*Utot

def EEVO(E0): 
    E = np.zeros(len(Frames)-1)
    for i, frame in enumerate(Frames[:-1]):
        #print(frame)
        if i == 0:
            E[i] = E0
        elif (i > 0 and i < 5):
            E[i] = E[i-1] - E[i-1]*dEdt[i]*1e9/GeV*2*Myr2s
            print(E[i-1]*dEdt[i]*1e9/GeV*2*Myr2s )
        else:
            t = Time[i] - Time[4]
            E[i] = E[4]/(1+beta*t*E[4])
    print(E)
    return E

#ax.plot(Time[1:], EEVO(100*GeV))
#ax.plot(Time[1:], EEVO(1*GeV))
plt.show()
