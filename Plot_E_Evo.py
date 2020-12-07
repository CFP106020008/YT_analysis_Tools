import numpy as np
import matplotlib.pyplot as plt

OUT = np.load('./E_Evo.npy')
plt.semilogy(OUT[0,1:,0], OUT[1,1:,0], linestyle='dashed', color='r', label=r"Proton Jet $E_{CR}$")
plt.semilogy(OUT[0,1:,0], OUT[2,1:,0], linestyle='dashed', color='b', label=r"Electron Jet $E_{CR}$")
plt.semilogy(OUT[0,1:,1], OUT[1,1:,1], linestyle='solid' , color='r', label=r"Proton Jet $E_k$")
plt.semilogy(OUT[0,1:,1], OUT[2,1:,1], linestyle='solid' , color='b', label=r"Electron Jet $E_k$")
plt.semilogy(OUT[0,1:,2], OUT[1,1:,2], linestyle=':' , color='r', label=r"Proton Jet $E_{th}$")
plt.semilogy(OUT[0,1:,2], OUT[2,1:,2], linestyle=':' , color='b', label=r"Electron Jet $E_{th}$")
plt.legend()
#plt.tight_layout()
plt.xlabel(r'Time (Myr)')
plt.ylabel('Energy ($erg$)')
plt.savefig("E_Evo.png", dpi=300)
