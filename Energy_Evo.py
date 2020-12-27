import numpy as np
import yt
import matplotlib.pyplot as plt
from matplotlib import rc_context
import My_Plugin as M
#Set the parameters
Folder_p = "./AGNCRp/crbub_hdf5_plt_cnt_*"
Folder_e = "./AGNCRe/crbub_hdf5_plt_cnt_*"
CMAP = 'algae' #'dusk'
mH = 1.6733e-24 #g
mu = 0.6
ts_p = yt.load(Folder_p) #Proton Jet dataset
ts_e = yt.load(Folder_e) #Electron Jet dataset
Frame = len(ts_p)

# Store data in an np array
# First axis: Time, Proton, Electron
# Second axis: Time series
# Third axis: CR, Kinetic, Thermal field
OUT = np.ones((3,len(ts_p),3)) 
for i in range(3):
    OUT[0,:,i] = np.linspace(ts_p[0].current_time/31556926e6,ts_p[-1].current_time/31556926e6,len(ts_p))

# Main Code
for i in range(Frame):
    print("Making Plot: {}/{}".format(i+1,len(ts_p)))
    OUT[1,i,0] = M.ECR_tot(ts_p[i])
    OUT[2,i,0] = M.ECR_tot(ts_e[i])
    OUT[1,i,1] = M.Ek_tot(ts_p[i])
    OUT[2,i,1] = M.Ek_tot(ts_e[i])
    OUT[1,i,2] = M.Eth_tot(ts_p[i])
    OUT[2,i,2] = M.Eth_tot(ts_e[i])

np.save("E_Evo.npy",OUT)
print(OUT)
