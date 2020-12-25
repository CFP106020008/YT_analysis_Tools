import yt
import numpy as np
from yt import YTQuantity
from yt.utilities.physical_constants import kb

def Zlim(Field):
    ZLIMS = {'Heating/Cooling':[1e-1, 1e1],
             'CR_energy_density':[1e-15, 1e-5],
             'density':[1e-27, 1e-24],
             'temperature':[1e7, 1e9],
             'crht':[1e-40, 1e-26],
             'pressure':[1e-11, 1e-8]
            }
    return ZLIMS[Field]

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

# Cosmic Ray energy density
def ecr(field, data):
    return data["density"]*data["cray"]*yt.YTQuantity(1,"erg/g")
yt.add_field(function = ecr, 
             units = "erg/cm**3", 
             name = "CR_energy_density", 
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
    return (data["pres"]*1.5 - data["density"]*data["cray"]*yt.YTQuantity(1,"erg/g")*0.5)*data["cell_volume"]
yt.add_field(function = _eth_incell, 
             units = "erg", 
             name = "Thermal_Energy",
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
    return data["crht"]*yt.YTQuantity(1,"erg/s/cm**3")/data["cooling_rate"]
yt.add_field(   ("gas","Heating/Cooling"), 
                function=Heat_Cool, 
                units="",
                sampling_type = "cell")






