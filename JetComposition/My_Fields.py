import yt
import numpy as np
from yt import YTQuantity
from yt.utilities.physical_constants import kb
from yt.fields.api import ValidateParameter
import os

# Loading all the file folders
def Load_Simulation_Datas():
    Folder_ps = "/data/yhlin/Final_Sims/CRp_Streaming/crbub_hdf5_plt_cnt_*"
    Folder_es = "/data/yhlin/Final_Sims/CReS_10MyrCool/crbub_hdf5_plt_cnt_*"
    Folder_p  = "/data/yhlin/Final_Sims/CRp_NS/crbub_hdf5_plt_cnt_*"
    Folder_e  = "/data/yhlin/Final_Sims/CRe/crbub_hdf5_plt_cnt_*"
    CRp = yt.load(Folder_p) #Proton Jet dataset
    CRe = yt.load(Folder_e) #Electron Jet dataset
    CRpS = yt.load(Folder_ps) #Proton Jet dataset
    CReS = yt.load(Folder_es) #Electron Jet dataset
    #CReS_RC = yt.load("/data/yhlin/CReS_RC/crbub_hdf5_plt_cnt_*")
    #CReS_SE = yt.load("/data/yhlin/CReS_SpectrumEvo/crbub_hdf5_plt_cnt_*")
    #CReS_SE_Small = yt.load("/data/yhlin/CReS_Emin=1e-2/crbub_hdf5_plt_cnt_*")
    #CReS_SE_CB_Emin100MeV = yt.load("/data/yhlin/CReS_SE_ConstantB/crbub_hdf5_plt_cnt_*") # Spectral evolution with constant B field
    #CReS_SE_CB_Emin1GeV = yt.load("/data/yhlin/Final_Sims/CReS_SE_CB_Emin1GeV/crbub_hdf5_plt_cnt_*") # Spectral evolution with constant B field
    #CRe_Expansion = yt.load("/data/yhlin/CRe_Expansion/crbub_hdf5_plt_cnt_*") # Detail process of bubble inflation
    CRe_1E21E0 = yt.load("/data/yhlin/CRe_EmaxEminConvergence/1E21E0/crbub_hdf5_plt_cnt_*") # Convergence test on Emax and Emin
    CRe_1E23E0 = yt.load("/data/yhlin/CRe_EmaxEminConvergence/1E23E0/crbub_hdf5_plt_cnt_*") # Convergence test on Emax and Emin
    CRe_3E11E0 = yt.load("/data/yhlin/CRe_EmaxEminConvergence/3E11E0/crbub_hdf5_plt_cnt_*") # Convergence test on Emax and Emin
    CRe_3E21E0 = yt.load("/data/yhlin/CRe_EmaxEminConvergence/3E21E0/crbub_hdf5_plt_cnt_*") # Convergence test on Emax and Emin
    CRe_1E23E_1 = yt.load("/data/yhlin/CRe_EmaxEminConvergence/1E23E-1/crbub_hdf5_plt_cnt_*") # Convergence test on Emax and Emin
    CReS_HighFPS = yt.load("/data/yhlin/CReS_HighFPS/crbub_hdf5_plt_cnt_*") # Convergence test on Emax and Emin
    Datas = {'CRp'          : CRp,
             'CRe'          : CRe,
             'CRpS'         : CRpS,
             'CReS'         : CReS,
             #'CReS_RC'      : CReS_RC,
             #'CReS_SE'      : CReS_SE,
             #'CReS_SE_Small': CReS_SE_Small,
             #'CReS_SE_CB_Small'   : CReS_SE_CB_Emin100MeV,
             #'CReS_SE_CB_Large'   : CReS_SE_CB_Emin1GeV,
             #'CRe_Expansion': CRe_Expansion,
             'CRe_1E21E0': CRe_1E21E0,
             'CRe_1E23E0': CRe_1E23E0,
             'CRe_3E11E0': CRe_3E11E0,
             'CRe_3E21E0': CRe_3E21E0,
             'CRe_1E23E-1': CRe_1E23E_1,
             'CReS_HighFPS': CReS_HighFPS
            }
    return Datas


def Zlim(Field):
    ZLIMS = {'Heating/Cooling':[1e-1, 1e1],
             'CR_energy_density':[1.e-10, 1.e-9],
             'density':[1e-27, 2e-25],
             'temperature':[2e7, 3e8],
             #'temperature':[5e4, 5e6],
             'crht':[1e-29, 1e-25],
             'pressure':[1.e-10, 1.e-9],
             'csht':[1e-29, 1e-25],
             'mag_strength':[1e-7, 1e-5],
             'beta_B':  [1, 1e3],
             'beta_CR': [1, 1e3],
             'beta_th': [1, 3],
             'cooling_time': [3.15e16, 3.17e16],
             'Sync': [1e-10, 1e-7],
             'Xray_Emissivity': [4e-24, 3e-23],
             'adiabatic_time': [-1e3, 1e3]
            }
    return ZLIMS[Field]

def Zlim_Projection(Field):
    ZLIMS = {'Heating/Cooling':[1e-1, 1e1],
             'CR_energy_density':[1e9, 1e17],
             'density':[2e-2, 6e-2],
             'temperature':[1e7, 1e9],
             'crht':[1e-29, 1e-25],
             'pressure':[1e-11, 1e-8],
             'csht':[1e-29, 1e-25],
             'mag_strength':[1e-7, 1e-5],
             'beta_B': [1, 1e3],
             'beta_CR': [1, 1e3],
             'beta_th': [1, 1e3],
             'cooling_time': [3.15e16, 3.17e16],
             'Sync': [1e-30, 1e-10],
             'Xray_Emissivity': [2e-3, 3e-2]
            }
    return ZLIMS[Field]

'''
# Cosmic Ray energy density
def ecr(field, data):
    return data["density"]*data["cray"]*yt.YTQuantity(1,"erg/g")
yt.add_field(function = ecr, 
             units = "erg/cm**3", 
             name = "CR_energy_density", 
             sampling_type = "cell")
'''
