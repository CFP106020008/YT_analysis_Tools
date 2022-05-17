import numpy as np
import yt
import matplotlib.pyplot as plt
from matplotlib import rc_context
import My_Plugin as M

#Set the parameters
Datas = M.Load_Simulation_Datas()
Datas_to_use = ['CRp', 'CRe', 'CRpS', 'CReS']
DataSet = [Datas[i] for i in Datas_to_use]
Titles = ['CRp', 'CRe', 'CRpS', 'CReS']

Frame = len(DataSet[0])
T_Start = M.Time(DataSet[0][0])
T_End   = M.Time(DataSet[0][-1])
TCUT = 5e5 # The temperature to define "cold" gas

def Set_Table():
    # Store data in an np array
    # [:,0] ==> Time
    # [:,1] ==> Cold gas mass
    OUT = np.ones((Frame,2)) 
    OUT[:,0] = np.linspace(T_Start, T_End, Frame)
    return OUT

def Write_Data(Ds, Name):
    OUT = Set_Table()
    for i in range(Frame):
        OUT[i,1] = M.ColdGas(Ds[i], Tcut=TCUT)
    np.save("/data/yhlin/ColdGasData/ColdGasMass_{}.npy".format(Name), OUT)

# Main
def run():
    for i, Data in enumerate(DataSet):
        Write_Data(Data, Titles[i])

if __name__ == '__main__':
    run()
