import numpy as np
import matplotlib.pyplot as plt
import My_Plugin as M
from os import listdir
from os.path import isfile, join
from matplotlib import rc_context
import tqdm as T

path = "/data/yhlin/E_EVO"
files = [f for f in listdir(path) if isfile(join(path, f))]
DataSet = [np.load(join(path, i)) for i in files]
Names = ['_'.join(''.join(f.split('.')[:-1]).split('_')[1:]) for f in files]

TO_PLOT = ['CRp', 'CRe', 'CRpS', 'CReS']
indexs = [Names.index(item) for item in TO_PLOT]
DataSet = [DataSet[i] for i in indexs]

#Plot_dE = True
PlotDE = True #False
fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(9,9), sharey=True, sharex=True)
plt.subplots_adjust(left=0.125, bottom=0.15, right=0.9, top=0.85, wspace=0.1, hspace=0.2)
y_lim = [1e57,1e62]
Time = np.linspace(0,100,51)
Myr2s = 1e6*86400*365

def Delta_Energy(E): #The input E should be a 1D array that is the sequence of Energy with time
    #deltaE = E-np.ones(np.shape(E)[0])*E[0]
    deltaE = E-np.ones(np.shape(E)[0])*np.min(E)
    return deltaE 

def Total_Energy(Data):
    return np.sum(Data, axis=1) 

def Plot_dE(i, j, k, Datas, Name, Color, Type): #Note that k=1 is for bubble, k=2 is for total field    
    axes[i,j].semilogy(Time[1:], Delta_Energy(Datas[k,:,0])[1:], linestyle='--', color=Color, label=r"$E_{CR}$")
    axes[i,j].semilogy(Time[1:], Delta_Energy(Datas[k,:,1])[1:], linestyle='-.', color=Color, label=r"$E_k$"   )
    axes[i,j].semilogy(Time[1:], Delta_Energy(Datas[k,:,2])[1:], linestyle=':' , color=Color, label=r"$E_{th}$")
    axes[i,j].semilogy(Time[1:], Delta_Energy(Total_Energy(Datas[k,:,:]))[1:], linestyle='-' , color=Color, label=r"$E_{tot}$")
    axes[i,j].set_title("{} Jet ({})".format(Name, Type))
    axes[i,j].set_ylim(y_lim)
    axes[i,j].legend()

def Plot_E(i, j, k, Datas, Name, Color, Type): #Note that k=1 is for bubble, k=2 is for total field
    axes[i, j].semilogy(Time[1:], Datas[k,1:,0], linestyle='--', color=Color, label=r"$E_{CR}$")
    axes[i, j].semilogy(Time[1:], Datas[k,1:,1], linestyle='-.', color=Color, label=r"$E_k$"   )
    axes[i, j].semilogy(Time[1:], Datas[k,1:,2], linestyle=':' , color=Color, label=r"$E_{th}$")
    axes[i, j].semilogy(Time[1:], Total_Energy(Datas[k,:,:])[1:], linestyle='-' , color=Color, label=r"$E_{tot}$")
    axes[i, j].semilogy(Time[1:], np.concatenate((np.linspace(0, 5e45*Myr2s*10, 6), np.ones(45)*5e45*Myr2s*10))[1:], linestyle='-' , color='gray', label="Inject jet energy")
    axes[i, j].set_title("{} Jet ({})".format(Name, Type))
    if j==0:
        axes[i, j].set_ylabel('Energy (erg)')
    if i==1:
        axes[i, j].set_xlabel('Time (Myr)')
    axes[i, j].set_xlim([Time[0], Time[-1]])
    axes[i, j].set_ylim(y_lim)
    axes[i, j].legend(ncol=2)

#for i, Data in enumerate(T.tqdm(DataSet)):
Plot_E(0, 0, 1, DataSet[0], TO_PLOT[0], 'r', 'Bubble')
Plot_E(0, 1, 1, DataSet[1], TO_PLOT[1], 'b', 'Bubble')
Plot_E(1, 0, 1, DataSet[2], TO_PLOT[2], 'r', 'Bubble')
Plot_E(1, 1, 1, DataSet[3], TO_PLOT[3], 'b', 'Bubble')

plt.savefig("E_Evo.png", dpi=300, bbox='tight')
