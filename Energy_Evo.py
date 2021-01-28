import numpy as np
import yt
import threading
import time
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
BubbleOnly = True
BubbleDef = 9.47e16

Start_Time = time.time()

def Set_Table():
    # Store data in an np array
    # First axis: Time, Proton, Electron
    # Second axis: Time series
    # Third axis: CR, Kinetic, Thermal field
    OUT = np.ones((3,len(CRp),3)) 
    for i in range(3):
        OUT[0,:,i] = np.linspace(M.Time(CRp[0]), M.Time(CRp[-1]), len(CRp))
    return OUT

OUT = Set_Table()

def One_Frame(Ds1, Ds2, i, OUT, BubbleDef):
    print("Making Plot: {}/{}".format(i+1,len(CRp)))
    OUT[1,i,0] = M.ECR_InBub(Ds1[i], BubbleDef=BubbleDef)
    OUT[2,i,0] = M.ECR_InBub(Ds2[i], BubbleDef=BubbleDef)
    OUT[1,i,1] =  M.Ek_InBub(Ds1[i], BubbleDef=BubbleDef)
    OUT[2,i,1] =  M.Ek_InBub(Ds2[i], BubbleDef=BubbleDef)
    OUT[1,i,2] = M.Eth_InBub(Ds1[i], BubbleDef=BubbleDef)
    OUT[2,i,2] = M.Eth_InBub(Ds2[i], BubbleDef=BubbleDef)

def Frames_in_range(Frame1, Frame2, Ds1, Ds2, BubbleDef):
    for i in range(Frame1, Frame2):
        One_Frame(Ds1, Ds2, i, OUT, BubbleDef=BubbleDef)

def Write_Data(Ds1, Ds2, Name, n_thread, BubbleOnly=True, OUT=OUT):
    if BubbleOnly:
        Thread_List = []
        for i in range(n_thread):
            Thread_List.append(threading.Thread(target=Frames_in_range, args=(int(Frame/n_thread)*i, int(Frame/n_thread)*(i+1), Ds1, Ds2, BubbleDef)))
        for t in Thread_List:
            t.start()
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
#Write_Data(CRp, CRe, Name='No_Streaming', n_thread=2)
Write_Data(CRpS, CReS, Name="Streaming", n_thread=2)
#End_Time = time.time()
#print('The code takes {} s to finish'.format(End_Time-Start_Time))
