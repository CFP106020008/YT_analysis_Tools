import numpy as np
import yt
import threading
import multiprocessing as mp
import multiprocessing.managers as mpman
import time
import matplotlib.pyplot as plt
from matplotlib import rc_context
import My_Plugin as M

#Set the parameters
CRp, CRe, CRpS, CReS = M.Load_Simulation_Datas()
Frame = len(CRp)
BubbleDef = 9.47e16
MultiProcess = True # Use multiprocress on CICA, procress <--> core on CICA
MultiThread = False

Start_Time = time.time()

# Setting some stuff to make multiple process use the same table
class MyManager(mpman.BaseManager):
    pass
MyManager.register('np_ones', np.ones, mpman.ArrayProxy)
m = MyManager()
m.start()

# Create the table to store the data
def Set_Table():
    # Store data in an np array
    # First axis: Time, Proton, Electron
    # Second axis: Time series
    # Third axis: CR, Kinetic, Thermal field
    OUT = m.np_ones((3,len(CRp),3)) 
    for i in range(3):
        OUT[0,:,i] = np.linspace(M.Time(CRp[0]), M.Time(CRp[-1]), len(CRp))
    return OUT

OUT = Set_Table()

def Frames_in_range(Frame1, Frame2, Ds1, Ds2, BubbleDef, OUT):
    for i in range(Frame1, Frame2):
        print("Making Plot: {}/{}".format(i+1,len(CRp)))
        OUT[1,i,0] = M.ECR_InBub(Ds1[i], BubbleDef=BubbleDef)
        OUT[2,i,0] = M.ECR_InBub(Ds2[i], BubbleDef=BubbleDef)
        OUT[1,i,1] =  M.Ek_InBub(Ds1[i], BubbleDef=BubbleDef)
        OUT[2,i,1] =  M.Ek_InBub(Ds2[i], BubbleDef=BubbleDef)
        OUT[1,i,2] = M.Eth_InBub(Ds1[i], BubbleDef=BubbleDef)
        OUT[2,i,2] = M.Eth_InBub(Ds2[i], BubbleDef=BubbleDef)

def Frames_in_range_Total(Frame1, Frame2, Ds1, Ds2, OUT):
    for i in range(Frame1, Frame2):
        print("Making Plot: {}/{}".format(i+1,len(CRp)))
        OUT[1,i,0] = M.ECR_tot(Ds1[i])
        OUT[2,i,0] = M.ECR_tot(Ds2[i])
        OUT[1,i,1] =  M.Ek_tot(Ds1[i])
        OUT[2,i,1] =  M.Ek_tot(Ds2[i])
        OUT[1,i,2] = M.Eth_tot(Ds1[i])
        OUT[2,i,2] = M.Eth_tot(Ds2[i])

def Write_Data(Ds1, Ds2, Name, n_thread, BubbleOnly=True):
    Lost = Frame%n_thread
    if BubbleOnly:
        if MultiProcess:
            Pro_List = []
            for i in range(n_thread):
                Pro_List.append(mp.Process(target=Frames_in_range, args=(int(Frame/n_thread)*i, int(Frame/n_thread)*(i+1), Ds1, Ds2, BubbleDef, OUT)))
            Pro_List.append(mp.Process(target=Frames_in_range, args=(int(Frame/n_thread)*(i+1), int(Frame/n_thread)*(i+1) + Lost, Ds1, Ds2, BubbleDef, OUT)))
            for p in Pro_List:
                p.start()
            for p in Pro_List:
                p.join() 
        if MultiThread:
            Thread_List = []
            for i in range(n_thread):
                Thread_List.append(threading.Thread(target=Frames_in_range, args=(int(Frame/n_thread)*i, int(Frame/n_thread)*(i+1), Ds1, Ds2, BubbleDef, OUT)))
            Thread_List.append(threading.Thread(target=Frames_in_range, args=(int(Frame/n_thread)*(i+1), int(Frame/n_thread)*(i+1) + Lost, Ds1, Ds2, BubbleDef, OUT)))
            for t in Thread_List:
                t.start()
            for t in Thread_List:
                t.join() 
        np.save("E_Evo_Bubble_{}.npy".format(Name),OUT)
    else:
        if MultiProcess:
            Pro_List = []
            for i in range(n_thread):
                Pro_List.append(mp.Process(target=Frames_in_range_Total, args=(int(Frame/n_thread)*i, int(Frame/n_thread)*(i+1), Ds1, Ds2, OUT)))
            Pro_List.append(mp.Process(target=Frames_in_range_Total, args=(int(Frame/n_thread)*(i+1), int(Frame/n_thread)*(i+1) + Lost, Ds1, Ds2, OUT)))
            for p in Pro_List:
                p.start()
            for p in Pro_List:
                p.join() 
        if MultiThread:
            Thread_List = []
            for i in range(n_thread):
                Thread_List.append(threading.Thread(target=Frames_in_range_Total, args=(int(Frame/n_thread)*i, int(Frame/n_thread)*(i+1), Ds1, Ds2, OUT)))
            Thread_List.append(threading.Thread(target=Frames_in_range_Total, args=(int(Frame/n_thread)*(i+1), int(Frame/n_thread)*(i+1) + Lost, Ds1, Ds2, OUT)))
            for t in Thread_List:
                t.start()
            for t in Thread_List:
                t.join() 
        np.save("E_Evo_Total_{}.npy".format(Name),OUT)

# Main Code
#Write_Data(CRp, CRe, Name='No_Streaming', n_thread=10)
#Write_Data(CRpS, CReS, Name='Streaming', n_thread=10)
#Write_Data(CRp, CRe, Name="No_Streaming", n_thread=10, BubbleOnly=False)
#Write_Data(CRpS, CReS, Name="Streaming",  n_thread=10, BubbleOnly=False)
Write_Data(CReS, CReS_RC, Name="SelfConsistentCooling",  n_thread=10)
#Write_Data(CReS, CReS_RC, Name="SelfConsistentCooling",  n_thread=10, BubbleOnly=False)
End_Time = time.time()
print('The code takes {} s to finish'.format(End_Time-Start_Time))
