import numpy as np
import yt
import matplotlib.pyplot as plt
from matplotlib import rc_context
import My_Plugin as M

#Set the parameters
Folder_p  = "/data/yhlin/CRp_NS/crbub_hdf5_plt_cnt_*"
Folder_e  = "/data/yhlin/CRe_NS/crbub_hdf5_plt_cnt_*"
Folder_pS = "/data/yhlin/CRp_Streaming/crbub_hdf5_plt_cnt_*"
Folder_eS = "/data/yhlin/CRe_Streaming/crbub_hdf5_plt_cnt_*"
CRp  = yt.load(Folder_p) #Proton Jet dataset
CRe  = yt.load(Folder_e) #Electron Jet dataset
CRpS = yt.load(Folder_pS) #Proton Jet dataset
CReS = yt.load(Folder_eS) #Electron Jet dataset
Frame = len(CRp)

def Set_Table():
    # Store data in an np array
    # [:,0] ==> Time
    # [:,1] ==> Cold gas mass of Ds1
    # [:,2] ==> Cold gas mass of Ds2
    OUT = np.ones((len(CRp),3)) 
    OUT[:,0] = np.linspace(M.Time(CRp[0]), M.Time(CRp[-1]), Frame)
    return OUT

def Write_Data(Ds1, Ds2, Name):
    OUT = Set_Table()
    for i in range(Frame):
        OUT[i,1] = M.ColdGas(Ds1[i], Tcut=5e5)
        OUT[i,2] = M.ColdGas(Ds2[i], Tcut=5e5)
    np.save("ColdGasMass_{}.npy".format(Name), OUT)

#Write_Data(CRpS, CReS, "Streaming")
#Write_Data(CRp, CRe, "No_Streaming")


