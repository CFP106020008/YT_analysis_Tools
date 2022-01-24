import yt
import numpy as np
from yt import YTQuantity
from yt.utilities.physical_constants import kb
from yt.fields.api import ValidateParameter
import os


Myr2s = 3.1556926e13


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

#=========================================================#

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

#=========================================================#

def Load_E_EVO_Data():
    path = "/data/yhlin/E_EVO/Final"
    files = [f for f in os.listdir(path) if (os.path.isfile(os.path.join(path, f)) and f.endswith(".npy"))]
    DataSet = [np.load(os.path.join(path, i), allow_pickle=True) for i in files]
    Names = ['_'.join(''.join(f.split('.')[:-1]).split('_')[1:]) for f in files]
    Datas = {}
    for i in range(len(DataSet)):
        Datas[Names[i]] = DataSet[i]
    #print(Datas)
    return Datas

#=========================================================#
def _mag_strength(field, data):
    return np.sqrt(data["magx"]**2 + data["magy"]**2 + data["magz"]**2)
yt.add_field(   ("gas","mag_strength"), 
                function=_mag_strength, 
                units="gauss",
                sampling_type = "cell")

#=========================================================#

def _coolingRate(field, data):
    return np.maximum(1.5*data["pressure"]/data["cooling_time"],1.e-30*YTQuantity(1.,"erg/s/cm**3")) #this includes setting a minimum value
yt.add_field(   ("gas","cooling_rate"), 
                function=_coolingRate, 
                units="erg/s/cm**3",
                sampling_type = "cell")

#=========================================================#

# Cooling timescale of the CR due to x ray emission
def _tCool(field, data):
    mu = 0.61 # assuming fully ionized gas
    mue = 1.18
    mp = 1.67e-24*YTQuantity(1.,"g")
    ne = data["density"]/mue/mp
    n = data["density"]/mu/mp
    T = data["temp"].in_units('K')
    return 1.5*n/ne**2.*kb*T**0.5/YTQuantity(3e-27, 'erg/s*cm**3/K**0.5')
yt.add_field(   ("gas", "cooling_time"), 
                function=_tCool, 
                units="s",
                sampling_type = "cell")

#=========================================================#

# Total Pressure / Magnetic Pressure
def beta_B(field, data):
    return data["pres"]/data["magp"]
yt.add_field(function = beta_B, 
             units = "", 
             name = "beta_B", 
             sampling_type = "cell")

#=========================================================#

# Cosmic Ray energy density
def ecr(field, data):
    return data["density"]*data["cray"]*yt.YTQuantity(1,"erg/g")
yt.add_field(function = ecr, 
             units = "erg/cm**3", 
             name = "CR_energy_density", 
             sampling_type = "cell")

#=========================================================#

# Total Pressure / CR Pressure
def beta_CR(field, data):
    return data["pres"]/(data["CR_energy_density"]/3)
yt.add_field(function = beta_CR, 
             units = "", 
             name = "beta_CR", 
             sampling_type = "cell")

#=========================================================#

# Cosmic Ray energy in cell
def _ecr_incell(field, data):
    return data["density"] * data["cray"] * yt.YTQuantity(1,"erg/g") * data["cell_volume"]
yt.add_field(function = _ecr_incell, 
             units = "erg", 
             name = "CR_energy_incell",
             sampling_type = "cell")

#=========================================================#

# Thermal Energy in cell
def _eth_incell(field, data):
    return (data["pres"]*1.5-data["density"]*data["cray"]*yt.YTQuantity(1,"erg/g")*0.5)*data["cell_volume"]
yt.add_field(function = _eth_incell, 
             units = "erg", 
             name = "Thermal_Energy",
             sampling_type = "cell")

#=========================================================#

# Total Pressure / Thermal pressure
def beta_th(field, data):
    mu = 0.61 # assuming fully ionized gas
    mp = 1.67e-24*YTQuantity(1.,"g")
    n = data["density"]/mu/mp
    T = data["temp"].in_units('K') 
    return data["pres"]/(n*kb*T)
yt.add_field(function = beta_th, 
             units = "", 
             name = "beta_th",
             sampling_type = "cell")

#=========================================================#
# Kinetic energy in cell
def _ek_incell(field, data):
    vx = data[('flash', 'velx')]#*yt.YTQuantity(1,"cm/s")
    vy = data[('flash', 'vely')]#*yt.YTQuantity(1,"cm/s")
    vz = data[('flash', 'velz')]#*yt.YTQuantity(1,"cm/s")
    return (vx**2 + vy**2 + vz**2)*data["density"]*data["cell_volume"]
yt.add_field(function = _ek_incell, 
             units = "erg", 
             name = "Kinetic_Energy",
             sampling_type = "cell")
#=========================================================#

# Kinetic energy in cell
def _PV_incell(field, data):
    return data["pres"]*data["cell_volume"]
yt.add_field(function = _PV_incell, 
             units = "erg", 
             name = "PV_incell",
             sampling_type = "cell")

#=========================================================#

def Heat_Cool(field, data):
    return (data["crht"]+data["csht"])*yt.YTQuantity(1,"erg/s/cm**3")/data["cooling_rate"]
yt.add_field(   ("gas","Heating/Cooling"), 
                function = Heat_Cool, 
                units="",
                sampling_type = "cell")

#=========================================================#

def CR_Heating(field, data):
    return (data["crht"]+data["csht"])*yt.YTQuantity(1,"erg/s/cm**3")
yt.add_field(   ("gas","CR_Heating"), 
                function = CR_Heating, 
                units="erg/s/cm**3",
                sampling_type = "cell")

#=========================================================#
def Xray_Emissivity(field, data):
    mu = 0.61 # assuming fully ionized gas
    mue = 1.18
    mp = 1.67e-24*YTQuantity(1.,"g")
    ne = data["density"]/mue/mp
    n = data["density"]/mu/mp
    T = data["temp"].in_units('K')
    return 3e-27*T**0.5*ne**2*yt.YTQuantity(1,"erg/s*cm**3/K**0.5")
yt.add_field(("gas","Xray_Emissivity"), 
             function = Xray_Emissivity, 
             units="erg/s/cm**3",
             sampling_type = "cell")
#yt.add_xray_emissivity_field(ds, 0.5, 2)

#=========================================================#

def ECR_tot(dataset):
    ds = dataset
    return ds.all_data().quantities.total_quantity(["CR_energy_incell"])

#=========================================================#

def Ek_tot(dataset):
    ds = dataset
    return ds.all_data().quantities.total_quantity(["Kinetic_Energy"])

#=========================================================#

def Eth_tot(dataset):
    ds = dataset
    return ds.all_data().quantities.total_quantity(["Thermal_Energy"])

#=========================================================#

def PV_tot(dataset):
    ds = dataset
    return ds.all_data().quantities.total_quantity(["PV_incell"])

#=========================================================#

def ECR_InBub(dataset, BubbleDef, radius=50):
    ds = dataset
    sp = ds.sphere(ds.domain_center, (radius, "kpc"))
    CR = ds.cut_region(sp, ["obj['cooling_time'] > {}".format(BubbleDef)])
    CR_InBub = CR.quantities.total_quantity("CR_energy_incell")
    return CR_InBub

#=========================================================#

def Ek_InBub(dataset, BubbleDef, radius=50):
    ds = dataset
    sp = ds.sphere(ds.domain_center, (radius, "kpc"))
    CR = ds.cut_region(sp, ["obj['cooling_time'] > {}".format(BubbleDef)])
    Ek_InBub = CR.quantities.total_quantity("Kinetic_Energy")
    return Ek_InBub

#=========================================================#

def Eth_InBub(dataset, BubbleDef, radius=50):
    ds = dataset
    sp = ds.sphere(ds.domain_center, (radius, "kpc"))
    CR = ds.cut_region(sp, ["obj['cooling_time'] > {}".format(BubbleDef)])
    Eth_InBub = CR.quantities.total_quantity("Thermal_Energy")
    return Eth_InBub

#=========================================================#

def PV_InBub(dataset, BubbleDef, radius=50):
    ds = dataset
    sp = ds.sphere(ds.domain_center, (radius, "kpc"))
    CR = ds.cut_region(sp, ["obj['cooling_time'] > {}".format(BubbleDef)])
    PV_InBub = CR.quantities.total_quantity("PV_incell")
    return PV_InBub

#=========================================================#

def Bub_Volume(dataset, BubbleDef, radius=50):
    ds  = dataset
    sp  = ds.sphere(ds.domain_center, (radius, "kpc"))
    Bub = ds.cut_region(sp, ["obj['cooling_time'] > {}".format(BubbleDef)])
    V   = Bub.quantities.total_quantity("cell_volume")
    return V

#=========================================================#

def Bub_Pressure(dataset, BubbleDef, radius=50):
    ds  = dataset
    sp  = ds.sphere(ds.domain_center, (radius, "kpc"))
    Bub = ds.cut_region(sp, ["obj['cooling_time'] > {}".format(BubbleDef)])
    P   = Bub.quantities.weighted_average_quantity("pressure", weight="cell_volume")
    return P

#=========================================================#

def Bub_PCR(dataset, BubbleDef, radius=50):
    ds  = dataset
    sp  = ds.sphere(ds.domain_center, (radius, "kpc"))
    Bub = ds.cut_region(sp, ["obj['cooling_time'] > {}".format(BubbleDef)])
    PCR = Bub.quantities.weighted_average_quantity("CR_energy_density", weight="cell_volume")/3
    return PCR

#=========================================================#

def One_Plot(i, ts, frame, Field, fig, grid, mag=False, vel=False, CMAP='inferno', Type='Slice'):
    ds = ts[frame]
    if Type == 'Projection':
        p = yt.ProjectionPlot(ds, 
                              'x', 
                              Field, 
                              width=(100, 'kpc')
                              ).set_cmap(field = Field, cmap=CMAP)
        #p.set_zlim(Field, Zlim_Projection(Field)[0], Zlim_Projection(Field)[1])
    else:
        p = yt.SlicePlot(ds, 
                         'x', 
                         Field, 
                         width=((100, 'kpc'), (100, 'kpc'))
                         ).set_cmap(field = Field, cmap=CMAP)
        p.set_zlim(Field, Zlim(Field)[0], Zlim(Field)[1])
    
    if mag:
        p.annotate_magnetic_field(normalize=True)

    if vel:
        p.annotate_velocity(factor = 16, normalize=True)
    
    plot = p.plots[Field]  
    plot.figure = fig
    plot.axes = grid[i].axes
    plot.cax = grid.cbar_axes[i]#.set_bad(color='black')
    p._setup_plots()

#=========================================================#

def Time(ds):
    return float(ds.current_time/31556926e6)

#=========================================================#

def ColdGas(dataset, Tcut=5e5):
    ds = dataset
    T = ds.r["temp"]
    MassInCell = ds.r["dens"]*ds.r["cell_volume"]
    ColdGasMass = np.sum(MassInCell[T <= Tcut])
    return ColdGasMass

#=========================================================#
def Sync_Emissivity(field, data, p=2.5):
    
    # Constants
    Myr2s = 3.1556926e13
    q_e   = 4.80e-10 # Fr (e.s.u)
    m_e   = 9.11e-28 # g
    sigma_T = 6.65e-25 # Thomson Cross Section
    c     = 29979245800. # cm/s
    MeV2erg = 1.6e-6 # Coverting factor
    
    # Parameters
    nu    = 1.51e8 # Hz, frequency of the observation
    B     = 1e-6 # G
    Urad  = 4.2e-13 # erg/cm**3 energy density of CMB photon at z=0
    
    # Derived quantities
    Ub    = B**2/(8*np.pi) # erg/cm**3
    Utot  = Ub + Urad
    beta  = 4/3*sigma_T/(m_e**2*c**3)*Utot
    nu_L  = q_e*B/(2*np.pi*m_e*c) # Larmor frequency
    
    # Evolution of the energy range
    E_max = 1e5*MeV2erg / (1 + beta*Time(data.ds)*Myr2s*1e5*MeV2erg)
    E_min = 1e3*MeV2erg / (1 + beta*Time(data.ds)*Myr2s*1e3*MeV2erg)
    #print(beta)
    #print(Time(data.ds))
    #print(E_max, E_min)

    # Number density
    n0    = data["CR_energy_density"].v*(2-p)/(E_max**(2-p)-E_min**(2-p))
    K     = n0*(m_e*c**2)**(1-p)
    Constants = (3*sigma_T*c*Ub*K)/(16*np.pi**1.5*nu_L)
    Frequency = (nu/nu_L)**((1-p)/2)
    Angle = 3**(p/2)*(2.25/p**2.2+0.105)
    epsilon_nu  = Constants*Frequency*Angle*YTQuantity(1.,"erg/s/cm**3")
    return epsilon_nu

yt.add_field(("gas", "Sync"),
             function = Sync_Emissivity, 
             units = "erg/s/cm**3", 
             sampling_type = "cell")

#=========================================================#

def Sync_incell(field, data):
    return data["Sync"]*data["cell_volume"]
yt.add_field(("gas", "Sync_incell"),
             function = Sync_incell, 
             units = "erg/s", 
             sampling_type = "cell")

#=========================================================#

def Sync_InBub(dataset, BubbleDef, radius=50):
    ds = dataset
    sp = ds.sphere(ds.domain_center, (radius, "kpc"))
    Bub = ds.cut_region(sp, ["obj['cooling_time'] > {}".format(BubbleDef)])
    #Syn = Bub.quantities.weighted_average_quantity("Sync", weight="cell_volume")
    Syn = Bub.quantities.total_quantity("Sync_incell")
    print(Syn)
    return Syn

#=========================================================#

def Sync_timescale(field, data):
    return data["CR_energy_density"]/data["Sync"]
yt.add_field(("gas", "Sync_timescale"),
             function = Sync_timescale, 
             units = "Myr", 
             sampling_type = "cell")

#=========================================================#

def LR_Total(ds):
    return ds.all_data().quantities.total_quantity(["Sync_incell"])

#=========================================================#

def adiabatic_time(field, data):
    return 1/data["velocity_divergence"]
yt.add_field(("gas", "adiabatic_time"),
             function = adiabatic_time, 
             units = "Myr", 
             sampling_type = "local")


def CR_Ratio(dataset, BubbleDef, radius=50):
    ds  = dataset
    sp  = ds.sphere(ds.domain_center, (radius, "kpc"))
    Bub = ds.cut_region(sp, ["obj['cooling_time'] > {}".format(BubbleDef)])
    P   = Bub.quantities.weighted_average_quantity("pressure", weight="cell_volume")
    PCR = Bub.quantities.weighted_average_quantity("CR_energy_density", weight="cell_volume")/3
    return PCR/P
    
