# This file stores the path to the datasets 

import yt
import numpy as np

def Load_Simulation_Datas():
    CRpS = yt.load('/data/yhlin/Final_Sims/CRp_Streaming/crbub_hdf5_plt_cnt_*') #Proton Jet dataset
    
    #CRpS_RefineTest = yt.load("/data/yhlin/ORCs/CRpS_RefineTest/crbub_hdf5_plt_cnt_*") 
    #CReS_M13_P5_D5 = yt.load("/data/yhlin/ORCs/ORC_LowResTest/CReS_M13_P5_D5_refdens/crbub_hdf5_plt_cnt_*") 
    #CReS_M13_P5_D10 = yt.load("/data/yhlin/ORCs/ORC_LowResTest/CReS_M13_P5_D10_refdens/crbub_hdf5_plt_cnt_*") 
    #CReS_M12_P5_D5 = yt.load("/data/yhlin/ORCs/ORC_LowResTest/CReS_M12_P5_D5_refdens/crbub_hdf5_plt_cnt_*") 
    #CReS_M12_P5_D10 = yt.load("/data/yhlin/ORCs/ORC_LowResTest/CReS_M12_P5_D10_highres/crbub_hdf5_plt_cnt_*") 
    
    CReS_88 = yt.load("/data/yhlin/ORCs/RefineVerify/CReS_M13_P5_D5_88/crbub_hdf5_plt_cnt_*")
    CReS_87 = yt.load("/data/yhlin/ORCs/RefineVerify/CReS_M13_P5_D5_87/crbub_hdf5_plt_cnt_*")
    CReS_86 = yt.load("/data/yhlin/ORCs/RefineVerify/CReS_M13_P5_D5_86/crbub_hdf5_plt_cnt_*")
    CReS_85 = yt.load("/data/yhlin/ORCs/RefineVerify/CReS_M13_P5_D5_85/crbub_hdf5_plt_cnt_*")

    KIN_M13_P1_D5 = yt.load("/data/yhlin/ORCs/ORC_LowResTest/KIN_M13_P1_D5/crbub_hdf5_plt_cnt_*")
    MIX_M13_P1_D5 = yt.load("/data/yhlin/ORCs/ORC_LowResTest/MIX_M13_P1_D5/crbub_hdf5_plt_cnt_*")
    MIX_M13_P5_D5 = yt.load("/data/yhlin/ORCs/ORC_LowResTest/MIX_M13_P5_D5/crbub_hdf5_plt_cnt_*")
    CRpS_M14_P1_D5 = yt.load("/data/yhlin/ORCs/ORC_LowResTest/CRpS_M14_P1_D5/crbub_hdf5_plt_cnt_*")
    CRpS_M14_P5_D1 = yt.load("/data/yhlin/ORCs/ORC_LowResTest/CRpS_M14_P5_D1/crbub_hdf5_plt_cnt_*")
    CRpS_M14_P5_D5 = yt.load("/data/yhlin/ORCs/ORC_LowResTest/CRpS_M14_P5_D5/crbub_hdf5_plt_cnt_*")
    CRpS_M14_P5_D5_lb23 = yt.load("/data/yhlin/ORCs/ORC_LowResTest/CRpS_M14_P5_D5_lb23/crbub_hdf5_plt_cnt_*")
    CRpS_M13_P1_D5 = yt.load("/data/yhlin/ORCs/ORC_LowResTest/CRpS_M13_P1_D5/crbub_hdf5_plt_cnt_*")
    CRpS_M13_P5_D1 = yt.load("/data/yhlin/ORCs/ORC_LowResTest/CRpS_M13_P5_D1/crbub_hdf5_plt_cnt_*")
    CRpS_M13_P5_D5 = yt.load("/data/yhlin/ORCs/ORC_LowResTest/CRpS_M13_P5_D5/crbub_hdf5_plt_cnt_*")
    CRpS_M13_P5_D5_lb23 = yt.load("/data/yhlin/ORCs/ORC_LowResTest/CRpS_M13_P5_D5_lb23/crbub_hdf5_plt_cnt_*")
    CRpS_M12_P1_D5 = yt.load("/data/yhlin/ORCs/ORC_LowResTest/CRpS_M12_P1_D5/crbub_hdf5_plt_cnt_*")
    CRpS_M12_P5_D1 = yt.load("/data/yhlin/ORCs/ORC_LowResTest/CRpS_M12_P5_D1/crbub_hdf5_plt_cnt_*")
    CRpS_M12_P5_D5 = yt.load("/data/yhlin/ORCs/ORC_LowResTest/CRpS_M12_P5_D5/crbub_hdf5_plt_cnt_*")
    CRpS_M12_P5_D5_lb23 = yt.load("/data/yhlin/ORCs/ORC_LowResTest/CRpS_M12_P5_D5_lb23/crbub_hdf5_plt_cnt_*")
    CReS_M13_P5_D5_OC = yt.load("/data/yhlin/ORCs/ORC_LowResTest/CReS_M13_P5_D5_OverCool/crbub_hdf5_plt_cnt_*")
    CReS_M12_P5_D5_OC = yt.load("/data/yhlin/ORCs/ORC_LowResTest/CReS_M12_P5_D5_OverCool/crbub_hdf5_plt_cnt_*")

    SelfRegCRp_M14 = yt.load("/data/yhlin/ORCs/SelfRegTest/CRpS_M14_P1_D1/crbub_hdf5_plt_cnt_*")
    SelfRegCRe_M14 = yt.load("/data/yhlin/ORCs/SelfRegTest/CReS_M14_P1_D1/crbub_hdf5_plt_cnt_*")
    SelfRegCRp_M13 = yt.load("/data/yhlin/ORCs/SelfRegTest/CRpS_M13_P1_D1/crbub_hdf5_plt_cnt_*")
    SelfRegCRp_M12 = yt.load("/data/yhlin/ORCs/SelfRegTest/CRpS_M12_P1_D1/crbub_hdf5_plt_cnt_*")
    
    Datas = {
             'CRpS' : CRpS,
             'CReS_88' : CReS_88,
             'CReS_87' : CReS_87,
             'CReS_86' : CReS_86,
             'CReS_85' : CReS_85,
             'KIN_M13_P1_D5' : KIN_M13_P1_D5,
             'MIX_M13_P1_D5' : MIX_M13_P1_D5,
             'MIX_M13_P5_D5' : MIX_M13_P5_D5,
             'CRpS_M14_P1_D5':CRpS_M14_P1_D5,
             'CRpS_M14_P5_D1':CRpS_M14_P5_D1,
             'CRpS_M14_P5_D5':CRpS_M14_P5_D5,
             'CRpS_M14_P5_D5_lb23':CRpS_M14_P5_D5_lb23,
             'CRpS_M13_P1_D5':CRpS_M13_P1_D5,
             'CRpS_M13_P5_D1':CRpS_M13_P5_D1,
             'CRpS_M13_P5_D5':CRpS_M13_P5_D5,
             'CRpS_M13_P5_D5_lb23':CRpS_M13_P5_D5_lb23,
             'CRpS_M12_P1_D5':CRpS_M12_P1_D5,
             'CRpS_M12_P5_D1':CRpS_M12_P5_D1,
             'CRpS_M12_P5_D5':CRpS_M12_P5_D5,
             'CRpS_M12_P5_D5_lb23':CRpS_M12_P5_D5_lb23,
             'CReS_M13_P5_D5_OC':CReS_M13_P5_D5_OC,
             'CReS_M12_P5_D5_OC':CReS_M12_P5_D5_OC,
             'SelfRegCRp_M14':SelfRegCRp_M14,
             'SelfRegCRe_M14':SelfRegCRe_M14,
             'SelfRegCRp_M13':SelfRegCRp_M13,
             'SelfRegCRp_M12':SelfRegCRp_M12,
            }
    return Datas

if __name__ == '__main__':
    print("Do not run me!")
