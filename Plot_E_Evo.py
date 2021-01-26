import numpy as np
import matplotlib.pyplot as plt

DS1 = np.load('./E_EVO/E_Evo_Streaming_Bubble.npy')
#DS2 = np.load('./E_EVO/E_Evo_Streaming_Total.npy')
DS2 = np.load('./E_Evo_Bubble.npy')

Plot_dE = True
fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(8,8), sharey=True, sharex=True)
plt.subplots_adjust(left=0.125, bottom=0.15, right=0.9, top=0.85, wspace=0.1, hspace=0.2)

y_lim = [1e57,1e62]

def Delta_Energy(E): #The input E should be a 1D array that is the sequence of Energy with time
    return E-np.ones(np.shape(E)[0])*E[0]

def Total_Energy(Data):
    return np.sum(Data, axis=1) 

def Plot(i, j, k, Datas, Name, Color, Type): #Note that k=1 is for CRp, k=2 is for CRe.
    axes[i,j].semilogy(Time[1:], Delta_Energy(Datas[k,:,0])[1:], linestyle='--', color=Color, label=r"$E_{CR}$")
    axes[i,j].semilogy(Time[1:], Delta_Energy(Datas[k,:,1])[1:], linestyle='-.', color=Color, label=r"$E_k$"   )
    axes[i,j].semilogy(Time[1:], Delta_Energy(Datas[k,:,2])[1:], linestyle=':' , color=Color, label=r"$E_{th}$")
    axes[i,j].semilogy(Time[1:], Total_Energy(Datas[k,:,:])[1:], linestyle='-' , color=Color, label=r"$E_{tot}$")
    axes[i,j].set_title("{} Jet ({})".format(Name, Type))
    axes[i,j].set_ylim(y_lim)
    axes[i,j].legend()

Time = DS1[0,:,0]

if Plot_dE:
    Plot(0, 0, 1, DS1, 'CRpS', 'r', 'Bubble')
    Plot(0, 1, 2, DS1, 'CReS', 'b', 'Bubble')
    Plot(1, 0, 1, DS2, 'CRp', 'r', 'Bubble')
    Plot(1, 1, 2, DS2, 'CRe', 'b', 'Bubble')
    fig.text(0.5, 0.08, r'Time (Myr)', ha='center')
    fig.text(0.04, 0.5, '$E-E_{0} (erg)$', va='center', rotation='vertical')

plt.savefig("E_Evo.png", dpi=300, bbox='tight')
