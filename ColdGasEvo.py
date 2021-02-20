import numpy as np
import yt
import matplotlib.pyplot as plt
from matplotlib import rc_context
import My_Plugin as M

#Set the parameters
CRp, CRe, CRpS, CReS = M.Load_Simulation_Datas()
Frame = len(CRp)
TCUT = 5e5 # The temperature to define "cold" gas

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
        OUT[i,1] = M.ColdGas(Ds1[i], Tcut=TCUT)
        OUT[i,2] = M.ColdGas(Ds2[i], Tcut=TCUT)
    np.save("ColdGasMass_{}.npy".format(Name), OUT)

#Write_Data(CRpS, CReS, "Streaming")
#Write_Data(CRp, CRe, "No_Streaming")


