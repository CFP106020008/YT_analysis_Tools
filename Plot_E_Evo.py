import numpy as np
import matplotlib.pyplot as plt

OUT = np.load('./E_Evo.npy')


fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(10,4))
plt.subplots_adjust(left=0.125, bottom=0.15, right=0.9, top=0.85, wspace=0.4, hspace=0.2)

y_lim = [1e57,3e60]

axes[0].semilogy(OUT[0,1:,0], OUT[1,1:,0]-np.ones(np.shape(OUT)[1]-1)*OUT[1,0,0], linestyle='--', color='r', label=r"Proton Jet $E_{CR}$")
axes[0].semilogy(OUT[0,1:,1], OUT[1,1:,1]-np.ones(np.shape(OUT)[1]-1)*OUT[1,0,1], linestyle='-.' , color='r', label=r"Proton Jet $E_k$")
axes[0].semilogy(OUT[0,1:,2], OUT[1,1:,2]-np.ones(np.shape(OUT)[1]-1)*OUT[1,0,2], linestyle=':' , color='r', label=r"Proton Jet $E_{th}$")
axes[0].semilogy(OUT[0,1:,2], np.sum(OUT[1,1:,:],axis=1)-np.ones(np.shape(OUT)[1]-1)*np.sum(OUT[1,0,:]), linestyle='-' , color='r', label=r"Proton Jet $E_{tot}$")
axes[0].set_title("Proton Jet")
axes[0].set_xlabel(r'Time (Myr)')
axes[0].set_ylabel('$E-E_{0}$ ($erg$)')
axes[0].set_ylim(y_lim)
axes[0].legend()

axes[1].semilogy(OUT[0,1:,0], OUT[2,1:,0]-np.ones(np.shape(OUT)[1]-1)*OUT[2,0,0], linestyle='--', color='b', label=r"Electron Jet $E_{CR}$")
axes[1].semilogy(OUT[0,1:,1], OUT[2,1:,1]-np.ones(np.shape(OUT)[1]-1)*OUT[2,0,1], linestyle='-.' , color='b', label=r"Electron Jet $E_k$")
axes[1].semilogy(OUT[0,1:,2], OUT[2,1:,2]-np.ones(np.shape(OUT)[1]-1)*OUT[2,0,2], linestyle=':' , color='b', label=r"Electron Jet $E_{th}$")
axes[1].semilogy(OUT[0,1:,2], np.sum(OUT[2,1:,:],axis=1)-np.ones(np.shape(OUT)[1]-1)*np.sum(OUT[2,0,:]), linestyle='-' , color='b', label=r"Proton Jet $E_{tot}$")
axes[1].set_title("Electron Jet")
axes[1].set_xlabel(r'Time (Myr)')
axes[1].set_ylabel('$E-E_{0}$ ($erg$)')
axes[1].set_ylim(y_lim)
axes[1].legend()
#plt.legend()
plt.savefig("E_Evo.png", dpi=300, bbox='tight')
