import numpy as np
import matplotlib.pyplot as plt

Bubble = np.load('./E_Evo_Streaming_Bubble.npy')
Total = np.load('./E_Evo_Streaming_Total.npy')

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
    #axes[i,j].set_xlabel(r'Time (Myr)')
    #axes[i,j].set_ylabel('$E-E_{0} (erg)$')
    axes[i,j].set_ylim(y_lim)
    axes[i,j].legend()

Time = Bubble[0,:,0]

if Plot_dE:
    Plot(0, 0, 1, Bubble, 'CRpS', 'r', 'Bubble')
    Plot(0, 1, 2, Bubble, 'CReS', 'b', 'Bubble')
    Plot(1, 0, 1, Total,  'CRpS', 'r', 'Total')
    Plot(1, 1, 2, Total,  'CReS', 'b', 'Total')
    #plt.tick_params(labelcolor="none", bottom=False, left=False)
    #plt.xlabel(r'Time (Myr)')
    #plt.ylabel('$E-E_{0} (erg)$')
    fig.text(0.5, 0.08, r'Time (Myr)', ha='center')
    fig.text(0.04, 0.5, '$E-E_{0} (erg)$', va='center', rotation='vertical')

'''
else:
    #axes[0].semilogy(OUT[0,1:,0], OUT[1,1:,0], linestyle='--', color='r', label=r"Proton Jet $E_{CR}$")
    #axes[0].semilogy(OUT[0,1:,1], OUT[1,1:,1], linestyle='-.', color='r', label=r"Proton Jet $E_k$")
    axes[0].semilogy(OUT[0,1:,2], OUT[1,1:,2], linestyle=':' , color='r', label=r"Proton Jet $E_{th}$")
    #axes[0].semilogy(OUT[0,1:,2], np.sum(OUT[1,1:,:],axis=1), linestyle='-' , color='r', label=r"Proton Jet $E_{tot}$")
    axes[0].set_title("Proton Jet")
    axes[0].set_xlabel(r'Time (Myr)')
    axes[0].set_ylabel('$E$ ($erg$)')
    #axes[0].set_ylim(y_lim)
    axes[0].legend()

    #axes[1].semilogy(OUT[0,1:,0], OUT[2,1:,0], linestyle='--', color='b', label=r"Electron Jet $E_{CR}$")
    #axes[1].semilogy(OUT[0,1:,1], OUT[2,1:,1], linestyle='-.', color='b', label=r"Electron Jet $E_k$")
    axes[1].semilogy(OUT[0,1:,2], OUT[2,1:,2], linestyle=':' , color='b', label=r"Electron Jet $E_{th}$")
    #axes[1].semilogy(OUT[0,1:,2], np.sum(OUT[2,1:,:],axis=1), linestyle='-' , color='b', label=r"Proton Jet $E_{tot}$")
    axes[1].set_title("Electron Jet")
    axes[1].set_xlabel(r'Time (Myr)')
    axes[1].set_ylabel('$E$ ($erg$)')
    #axes[1].set_ylim(y_lim)
    axes[1].legend()
'''
plt.savefig("E_Evo_Streaming.png", dpi=300, bbox='tight')
