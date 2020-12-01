import numpy as np
import yt
import matplotlib.pyplot as plt
from matplotlib import rc_context

#Set the parameters
Folder_p = "./AGNCRp/crbub_hdf5_plt_cnt_*"
Folder_e = "./AGNCRe/crbub_hdf5_plt_cnt_*"
CMAP = 'algae' #'dusk'

#========================================#

ts_p = yt.load(Folder_p) #Proton Jet dataset
ts_e = yt.load(Folder_e) #Electron Jet dataset

#========================================#

# Define a new field that is the CR energy in each cell
def _ecr_incell(field, data):
    return data["density"] * data["cray"] * yt.YTQuantity(1,"erg/g") * data["cell_volume"]
yt.add_field(function = _ecr_incell, 
             units = "erg", 
             name = "CR_energy_incell",
             sampling_type = "cell")

#========================================#

def _ek_incell(field, data):
    vx = data[('flash', 'velx')]#*yt.YTQuantity(1,"cm/s")
    vy = data[('flash', 'vely')]#*yt.YTQuantity(1,"cm/s")
    vz = data[('flash', 'velz')]#*yt.YTQuantity(1,"cm/s")
    return (vx**2 + vy**2 + vz**2)*data["density"]*data["cell_volume"]
yt.add_field(function = _ek_incell, 
             units = "erg", 
             name = "Kinetic_Energy",
             sampling_type = "cell")

#========================================#

def _eth_incell(field, data):
    return data["density"] * data["cell_volume"] * data["temp"] * yt.YTQuantity(1.38e-16,"erg/K")
yt.add_field(function = _eth_incell, 
             units = "erg", 
             name = "Thermal_Energy",
             sampling_type = "cell")

#========================================#

def ECR_tot(dataset):
    ds = dataset
    return ds.all_data().quantities.total_quantity(["CR_energy_incell"])

def Ek_tot(dataset):
    ds = dataset
    return ds.all_data().quantities.total_quantity(["Kinetic_Energy"])

def Eth_tot(dataset):
    ds = dataset
    return ds.all_data().quantities.total_quantity(["Thermal_Energy"])

# Store data in an np array
# First axis: Time, Proton, Electron
# Second axis: Time series
# Third axis: CR, Kinetic, Thermal field
OUT = np.ones((3,len(ts_p),3)) 
OUT[0,:,0] = np.linspace(ts_p[0].current_time/31556926e6,ts_p[-1].current_time/31556926e6,len(ts_p))
#OUT[0,:,1] = np.linspace(ts_p[0].current_time/31556926e6,ts_p[-1].current_time/31556926e6,len(ts_p))

# Main Code
for i in range(len(ts_p)):
    print("Making Plot: {}/{}".format(i+1,len(ts_p)))
    #OUT[1,i,0] = ECR_tot(ts_p[i])
    #OUT[2,i,0] = ECR_tot(ts_e[i])
    OUT[1,i,1] = Ek_tot(ts_p[i])
    OUT[2,i,1] = Ek_tot(ts_e[i])
    #OUT[1,i,2] = Eth_tot(ts_p[i])
    #OUT[2,i,2] = Eth_tot(ts_e[i])

np.save("E_Evo.npy",OUT)
