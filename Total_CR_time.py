import numpy as np
import yt
import matplotlib.pyplot as plt
from matplotlib import rc_context
import My_Plugin as M

#Set the parameters
Folder_p = "./AGNCRp/crbub_hdf5_plt_cnt_*"
Folder_e = "./AGNCRe/crbub_hdf5_plt_cnt_*"
CMAP = 'algae' #'dusk'

#===========================#

ts_p = yt.load(Folder_p) #Proton Jet dataset
ts_e = yt.load(Folder_e) #Electron Jet dataset

# Store data in an np array
# First row: Time, Second row: Proton, Third row: Electron
OUT = np.ones((3,len(ts_p))) 
OUT[0,:] = np.linspace(ts_p[0].current_time/31556926e6,ts_p[-1].current_time/31556926e6,len(ts_p))

# Main Code
for i in range(len(ts_p)):
    print("Making Plot: {}/{}".format(i+1,len(ts_p)))
    OUT[1,i] = M.ECR_tot(ts_p[i])
    OUT[2,i] = M.ECR_tot(ts_e[i])

np.save("CREtot.npy",OUT)

# Plotting setting
plt.plot(OUT[0,:], OUT[1,:], label="Proton Jet")
plt.plot(OUT[0,:], OUT[2,:], label="Electron Jet")
plt.legend()
plt.xlabel("Time (Myr)")
plt.ylabel("CR Energy (erg)")
plt.savefig("CREtot.png")
#plt.show()
