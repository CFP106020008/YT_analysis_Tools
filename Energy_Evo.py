import numpy as np
import yt
import matplotlib.pyplot as plt
from matplotlib import rc_context
import My_Plugin as M

#Set the parameters
Folder_p = "./CRp_Streaming/crbub_hdf5_plt_cnt_*"
Folder_e = "./CRe_Streaming/crbub_hdf5_plt_cnt_*"
CMAP = 'algae' #'dusk'
ts_p = yt.load(Folder_p) #Proton Jet dataset
ts_e = yt.load(Folder_e) #Electron Jet dataset
Frame = len(ts_p)
BubbleOnly = True
BubbleDef = 1e-14

# Store data in an np array
# First axis: Time, Proton, Electron
# Second axis: Time series
# Third axis: CR, Kinetic, Thermal field
OUT = np.ones((3,len(ts_p),3)) 
for i in range(3):
    OUT[0,:,i] = np.linspace(ts_p[0].current_time/31556926e6,ts_p[-1].current_time/31556926e6,len(ts_p))

# Main Code
if BubbleOnly:
    for i in range(Frame):
        print("Making Plot: {}/{}".format(i+1,len(ts_p)))
        OUT[1,i,0] = M.ECR_InBub(ts_p[i], BubbleDef=BubbleDef)
        OUT[2,i,0] = M.ECR_InBub(ts_p[i], BubbleDef=BubbleDef)
        OUT[1,i,1] =  M.Ek_InBub(ts_p[i], BubbleDef=BubbleDef)
        OUT[2,i,1] =  M.Ek_InBub(ts_e[i], BubbleDef=BubbleDef)
        OUT[1,i,2] = M.Eth_InBub(ts_p[i], BubbleDef=BubbleDef)
        OUT[2,i,2] = M.Eth_InBub(ts_e[i], BubbleDef=BubbleDef)
    np.save("E_Evo_Streaming_Bubble.npy",OUT)
else:
    for i in range(Frame):
        print("Making Plot: {}/{}".format(i+1,len(ts_p)))
        OUT[1,i,0] = M.ECR_tot(ts_p[i])
        OUT[2,i,0] = M.ECR_tot(ts_e[i])
        OUT[1,i,1] =  M.Ek_tot(ts_p[i])
        OUT[2,i,1] =  M.Ek_tot(ts_e[i])
        OUT[1,i,2] = M.Eth_tot(ts_p[i])
        OUT[2,i,2] = M.Eth_tot(ts_e[i])
    np.save("E_Evo_Streaming_Total.npy",OUT)
#print(OUT)
