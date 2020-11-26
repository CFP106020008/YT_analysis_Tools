import numpy as np
import yt
import matplotlib.pyplot as plt
from matplotlib import rc_context

#Set the parameters
Folder_p = "./AGNCRp/crbub_hdf5_plt_cnt_*"
Folder_e = "./AGNCRe/crbub_hdf5_plt_cnt_*"
CMAP = 'algae' #'dusk'

#===========================#

ts_p = yt.load(Folder_p) #Proton Jet dataset
ts_e = yt.load(Folder_e) #Electron Jet dataset

# Define a new field that is the CR energy in each cell
def _ecr_incell(field, data):
    return data["density"]*data["cray"]*yt.YTQuantity(1,"erg/g")*data["cell_volume"]

# Add field
yt.add_field(function = _ecr_incell, 
             units = "erg", 
             name = "CR_energy_incell",
             sampling_type = "cell")
#ts_p[0].add_field(function = _ecr_incell, 
#             units = "erg", 
#             name = "CR_energy_incell",
#             sampling_type = "cell")

#print(ts_p[0].field_list)

def ECR_tot(dataset):
    ds = dataset
    return ds.all_data().quantities.total_quantity(["CR_energy_incell"])

OUT = np.ones((3,len(ts_p))) # First row: Time, Second row: Proton, Third row: Electron
OUT[0,:] = np.linspace(ts_p[0].current_time/31556926e6,ts_p[-1].current_time/31556926e6,len(ts_p))

for i in range(len(ts_p)):
    print("Making Plot: {}/{}".format(i,len(ts_p)))
    OUT[1,i] = ECR_tot(ts_p[i])
    OUT[2,i] = ECR_tot(ts_e[i])

plt.plot(OUT[0,:], OUT[1,:], label="Proton Jet")
plt.plot(OUT[0,:], OUT[2,:], label="Electron Jet")
plt.legend()
plt.xlabel("Time (Myr)")
plt.ylabel("CR Energy (erg)")
plt.show()
