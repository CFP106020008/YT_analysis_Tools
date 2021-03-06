import numpy as np
import matplotlib.pyplot as plt

DS1 = np.load("/data/yhlin/E_EVO/EEVO_CReS.npy")
DS2 = np.load("/data/yhlin/E_EVO/EEVO_CReS_RC.npy")
DS3 = np.load("/data/yhlin/E_EVO/EEVO_CReS_SE.npy")
DS4 = np.load("/data/yhlin/E_EVO/EEVO_CReS_SE_Small.npy")

#Plot_dE = True
PlotDE = True #False
fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(8,8), sharey=True, sharex=True)
plt.subplots_adjust(left=0.125, bottom=0.15, right=0.9, top=0.85, wspace=0.1, hspace=0.2)

y_lim = [1e57,1e62]

def Delta_Energy(E): #The input E should be a 1D array that is the sequence of Energy with time
    #deltaE = E-np.ones(np.shape(E)[0])*E[0]
    deltaE = E-np.ones(np.shape(E)[0])*np.min(E)
    return deltaE 

def Total_Energy(Data):
    return np.sum(Data, axis=1) 

def Plot_dE(i, j, k, Datas, Name, Color, Type): #Note that k=1 is for bubble, k=2 is for total field    
    axes[i,j].semilogy(Time[1:], Delta_Energy(Datas[k,:,0])[1:], linestyle='--', color=Color, label=r"$E_{CR}$")
    axes[i,j].semilogy(Time[1:], Delta_Energy(Datas[k,:,1])[1:], linestyle='-.', color=Color, label=r"$E_k$"   )
    axes[i,j].semilogy(Time[1:], Delta_Energy(Datas[k,:,2])[1:b], linestyle=':' , color=Color, label=r"$E_{th}$")
    axes[i,j].semilogy(Time[1:], Delta_Energy(Total_Energy(Datas[k,:,:]))[1:], linestyle='-' , color=Color, label=r"$E_{tot}$")
    axes[i,j].set_title("{} Jet ({})".format(Name, Type))
    axes[i,j].set_ylim(y_lim)
    axes[i,j].legend()

def Plot_E(i, j, k, Datas, Name, Color, Type): #Note that k=1 is for bubble, k=2 is for total field
    axes[i,j].semilogy(Time[1:], Datas[k,1:,0], linestyle='--', color=Color, label=r"$E_{CR}$")
    axes[i,j].semilogy(Time[1:], Datas[k,1:,1], linestyle='-.', color=Color, label=r"$E_k$"   )
    axes[i,j].semilogy(Time[1:], Datas[k,1:,2], linestyle=':' , color=Color, label=r"$E_{th}$")
    axes[i,j].semilogy(Time[1:], Total_Energy(Datas[k,:,:])[1:], linestyle='-' , color=Color, label=r"$E_{tot}$")
    axes[i,j].set_title("{} Jet ({})".format(Name, Type))
    axes[i,j].set_ylim(y_lim)
    axes[i,j].legend()


Time = np.linspace(0,100,51)

if PlotDE:
    Plot_dE(0, 0, 1, DS1, 'CReS', 'b', 'Bubble')
    Plot_dE(0, 1, 1, DS2, 'CReS_RC', 'b', 'Bubble')
    Plot_dE(1, 0, 1, DS3, 'CReS_SE', 'b', 'Bubble')
    Plot_dE(1, 1, 1, DS4, 'CReS_SE_Small', 'b', 'Bubble')
    fig.text(0.5, 0.08, r'Time (Myr)', ha='center')
    fig.text(0.04, 0.5, '$E-E_{0} (erg)$', va='center', rotation='vertical')
else:
    Plot_E(0, 0, 1, DS1, 'CReS', 'b', 'Bubble')
    Plot_E(0, 1, 1, DS2, 'CReS_RC', 'b', 'Bubble')
    Plot_E(1, 0, 1, DS3, 'CReS_SE', 'b', 'Bubble')
    Plot_E(1, 1, 1, DS4, 'CReS_SE_Small', 'b', 'Bubble')
    fig.text(0.5, 0.08, r'Time (Myr)', ha='center')
    fig.text(0.04, 0.5, '$E(erg)$', va='center', rotation='vertical')

plt.savefig("E_Evo.png", dpi=300, bbox='tight')
