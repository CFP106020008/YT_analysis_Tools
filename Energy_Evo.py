import numpy as np
import yt
import matplotlib.pyplot as plt
from matplotlib import rc_context
import My_Plugin as M

#Set the parameters
Folder_p  = "/data/yhlin/CRp/crbub_hdf5_plt_cnt_*"
Folder_e  = "/data/yhlin/CRe/crbub_hdf5_plt_cnt_*"
Folder_pS = "/data/yhlin/CRp_Streaming/crbub_hdf5_plt_cnt_*"
Folder_eS = "/data/yhlin/CRe_Streaming/crbub_hdf5_plt_cnt_*"
CRp  = yt.load(Folder_p) #Proton Jet dataset
CRe  = yt.load(Folder_e) #Electron Jet dataset
CRpS = yt.load(Folder_pS) #Proton Jet dataset
CReS = yt.load(Folder_eS) #Electron Jet dataset
Frame = len(CRp)
BubbleOnly = True
BubbleDef = 1e-11

def Set_Table():
    # Store data in an np array
    # First axis: Time, Proton, Electron
    # Second axis: Time series
    # Third axis: CR, Kinetic, Thermal field
    OUT = np.ones((3,len(CRp),3)) 
    for i in range(3):
        OUT[0,:,i] = np.linspace(CRp[0].current_time/31556926e6,CRp[-1].current_time/31556926e6,len(CRp))
    return OUT

def Write_Data(Ds1, Ds2, Name, BubbleOnly=True):
    OUT = Set_Table()
    if BubbleOnly:
        for i in range(Frame):
            print("Making Plot: {}/{}".format(i+1,len(CRp)))
            OUT[1,i,0] = M.ECR_InBub(Ds1[i], BubbleDef=BubbleDef)
            OUT[2,i,0] = M.ECR_InBub(Ds2[i], BubbleDef=BubbleDef)
            OUT[1,i,1] =  M.Ek_InBub(Ds1[i], BubbleDef=BubbleDef)
            OUT[2,i,1] =  M.Ek_InBub(Ds2[i], BubbleDef=BubbleDef)
            OUT[1,i,2] = M.Eth_InBub(Ds1[i], BubbleDef=BubbleDef)
            OUT[2,i,2] = M.Eth_InBub(Ds2[i], BubbleDef=BubbleDef)
        np.save("E_Evo_Bubble_{}.npy".format(Name),OUT)
    else:
        for i in range(Frame):
            print("Making Plot: {}/{}".format(i+1,len(CRp)))
            OUT[1,i,0] = M.ECR_tot(Ds1[i])
            OUT[2,i,0] = M.ECR_tot(Ds2[i])
            OUT[1,i,1] =  M.Ek_tot(Ds1[i])
            OUT[2,i,1] =  M.Ek_tot(Ds2[i])
            OUT[1,i,2] = M.Eth_tot(Ds1[i])
            OUT[2,i,2] = M.Eth_tot(Ds2[i])
        np.save("E_Evo_Total_{}.npy".format(Name),OUT)

# Main Code
Write_Data(CRp, CRe, Name='No_Streaming')
Write_Data(CRpS, CReS, Name="Streaming")
