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
Datas = M.Load_Simulation_Datas()
Datas_to_use = ['CReS_SE_CB_Large']#['CReS', 'CReS_RC', 'CReS_SE', 'CReS_SE_Small', 'CRp', 'CRe', 'CRpS']
DataSet = [Datas[i] for i in Datas_to_use]

Frame = 51
BubbleDef = 9.47e16
MultiProcess = True # Use multiprocress on CICA, procress <--> core on CICA

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
    OUT = m.np_ones((3,len(DataSet[0]),4)) 
    for i in range(3):
        OUT[0,:,i] = np.linspace(M.Time(DataSet[0][0]), M.Time(DataSet[0][-1]), len(DataSet[0]))
    return OUT

OUT = Set_Table()

def Frames_in_range(Frame1, Frame2, Ds, BubbleDef, OUT):
    for i in range(Frame1, Frame2):
        print("Making Plot: {}/{}".format(i+1,len(DataSet[0])))
        OUT[1,i,0] = M.ECR_InBub(Ds[i], BubbleDef=BubbleDef)
        OUT[2,i,0] = M.ECR_tot(Ds[i])
        OUT[1,i,1] = M.Ek_InBub(Ds[i], BubbleDef=BubbleDef)
        OUT[2,i,1] = M.Ek_tot(Ds[i])
        OUT[1,i,2] = M.Eth_InBub(Ds[i], BubbleDef=BubbleDef)
        OUT[2,i,2] = M.Eth_tot(Ds[i])
        OUT[1,i,3] = M.PV_InBub(Ds[i], BubbleDef=BubbleDef)
        OUT[2,i,3] = M.PV_tot(Ds[i])


def Write_Data(Ds, Name, n_process, BubbleOnly=True):
    Lost = Frame%n_process
    Pro_List = []
    for i in range(n_process):
        Pro_List.append(mp.Process(target=Frames_in_range, args=(int(Frame/n_process)*i, int(Frame/n_process)*(i+1), Ds, BubbleDef, OUT)))
    Pro_List.append(mp.Process(target=Frames_in_range, args=(int(Frame/n_process)*(i+1), int(Frame/n_process)*(i+1) + Lost, Ds, BubbleDef, OUT)))
    for p in Pro_List:
        p.start()
    for p in Pro_List:
        p.join()
    np.save("./EEVO_{}.npy".format(Name),OUT)

# Main Code
for i in range(len(DataSet)):
    Write_Data(DataSet[i], Name=Datas_to_use[i],  n_process=10)
End_Time = time.time()
print('The code takes {} s to finish'.format(End_Time-Start_Time))
