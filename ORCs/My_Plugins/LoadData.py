# This file stores the path to the datasets 

import yt
import numpy as np



def Load_Simulation_Datas():
    CRpS = yt.load('/data/yhlin/Final_Sims/CRp_Streaming/crbub_hdf5_plt_cnt_*') #Proton Jet dataset
    ORC_M12_P1_D1 = yt.load('/data/yhlin/ORCs/ORC_LowResTest/ORC_M12_P1_D1/crbub_hdf5_plt_cnt_*') 
    ORC_M12_P1_D5 = yt.load('/data/yhlin/ORCs/ORC_LowResTest/ORC_M12_P1_D5/crbub_hdf5_plt_cnt_*') 
    ORC_M13_P1_D1 = yt.load('/data/yhlin/ORCs/ORC_LowResTest/ORC_M13_P1_D1/crbub_hdf5_plt_cnt_*') 
    ORC_M13_P1_D5 = yt.load('/data/yhlin/ORCs/ORC_LowResTest/ORC_M13_P1_D5/crbub_hdf5_plt_cnt_*') 
    ORC_M12_P1_D5_200 = yt.load('/data/yhlin/ORCs/ORC_LowResTest/ORC_M12_P1_D5_200Myr/crbub_hdf5_plt_cnt_*') 
    ORC_M12_P1_D10 = yt.load('/data/yhlin/ORCs/ORC_LowResTest/ORC_M12_P1_D10/crbub_hdf5_plt_cnt_*') 
    ORC_M12_P0_D5 = yt.load('/data/yhlin/ORCs/ORC_LowResTest/ORC_M12_P0_D5/crbub_hdf5_plt_cnt_*') 
    ORC_M12_P0_D10 = yt.load('/data/yhlin/ORCs/ORC_LowResTest/ORC_M12_P0_D10/crbub_hdf5_plt_cnt_*') 
    Datas = {
             'CRpS': CRpS,
             'ORC_M13_P1_D1': ORC_M13_P1_D1,
             'ORC_M13_P1_D5': ORC_M13_P1_D5,
             'ORC_M12_P1_D1': ORC_M12_P1_D1,
             'ORC_M12_P1_D5': ORC_M12_P1_D5,
             'ORC_M12_P1_D10': ORC_M12_P1_D10,
             'ORC_M12_P1_D5_200': ORC_M12_P1_D5_200,
             'ORC_M12_P0_D5': ORC_M12_P0_D5,
             'ORC_M12_P0_D10': ORC_M12_P0_D10,
            }
    return Datas

if __name__ == '__main__':
    print("Do not run me!")
