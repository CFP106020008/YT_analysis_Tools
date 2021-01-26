import yt
import numpy as np
from yt import YTQuantity
from yt.utilities.physical_constants import kb

def Zlim(Field):
    ZLIMS = {'Heating/Cooling':[1e-1, 1e1],
             'CR_energy_density':[1e-15, 1e-5],
             'density':[1e-27, 1e-24],
             'temperature':[1e7, 1e9],
             'crht':[1e-29, 1e-25],
             'pressure':[1e-11, 1e-8],
             'csht':[1e-29, 1e-25],
             'mag_strength':[1e-7, 1e-5],
             'beta_B': [1, 1e3],
             'beta_CR': [1, 1e3],
             'beta_th': [1, 1e3]
            }
    return ZLIMS[Field]

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

def ECR_InBub(dataset, BubbleDef):
    ds = dataset
    F_CR = ds.r["CR_energy_density"]
    CRIC = ds.r["CR_energy_incell"]
    CR_InBub = np.sum(CRIC[F_CR >= BubbleDef])
    return CR_InBub

#=========================================================#

def Ek_InBub(dataset, BubbleDef):
    ds = dataset
    F_CR = ds.r["CR_energy_density"]
    Ek = ds.r["Kinetic_Energy"]
    Ek_InBub = np.sum(Ek[F_CR >= BubbleDef])
    return Ek_InBub

#=========================================================#

def Eth_InBub(dataset, BubbleDef):
    ds = dataset
    F_CR = ds.r["CR_energy_density"]
    Eth = ds.r["Thermal_Energy"]
    Eth_InBub = np.sum(Eth[F_CR >= BubbleDef])
    return Eth_InBub

#=========================================================#

def One_Plot(i, ts, frame, Field, fig, grid, mag=False, vel=False, CMAP='algae'):
    ds = ts[frame]
    p = yt.SlicePlot(ds, 
                     'x', 
                     Field, 
                     width=(200, 'kpc')
                     ).set_cmap(field = Field, cmap=CMAP)
    if mag:
        p.annotate_magnetic_field(normalize=True)

    if vel:
        p.annotate_velocity(factor = 16,normalize=True)
    
    p.set_zlim(Field, Zlim(Field)[0], Zlim(Field)[1])
    plot = p.plots[Field]        
    plot.figure = fig
    plot.axes = grid[i].axes
    plot.cax = grid.cbar_axes[i]
    p._setup_plots()

#=========================================================#

def Time(ds):
    return float(ds.current_time/31556926e6)
