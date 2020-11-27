import numpy as np
import yt
import yt.units as u
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import AxesGrid
from matplotlib import rc_context

#Set the parameters
Folder_p = "./AGNCRp/crbub_hdf5_plt_cnt_*"
Folder_e = "./AGNCRe/crbub_hdf5_plt_cnt_*"
Frame = 30 #The frame to plot the profiles
Fields = ['density','CR_energy_density','pressure', 'temperature']
unit = [r'$erg/cm^3$',r'$erg/cm^3$',r'$erg/cm^3$',r'$K$']
radius = 50*u.kpc
height = 20*u.kpc
center = [0,0,0]
#===========================#

ts_p = yt.load(Folder_p) #Proton Jet dataset
ts_e = yt.load(Folder_e) #Electron Jet dataset

fns = [ts_p, ts_e]

# Define a new field that is the CR energy in each cell
def ecr(field, data):
    return data["density"]*data["cray"]*yt.YTQuantity(1,"erg/g")

# Add field
yt.add_field(function = ecr, 
             units = "erg/cm**3", 
             name = "CR_energy_density",
             sampling_type = "cell")

fig, axes = plt.subplots(nrows=len(Fields), ncols=2, figsize=(8,8))
'''
fig = plt.figure()
grid = AxesGrid(fig, (0.075,0.075,0.85,0.85),
                nrows_ncols = (len(Fields), 2),
                axes_pad = 1.0,
                label_mode = "1",
                share_all = True,
                cbar_location="right",
                cbar_mode="each",
                cbar_size="3%",
                cbar_pad="0%")
'''

for i, jet in enumerate(fns):
    ds = jet[Frame]
    disk = ds.disk(center, [0,0,1], radius, height)
    rp = yt.create_profile(disk, 'radius', Fields,
                           units = {'radius': 'kpc'},
                           logs = {'radius': False})
    for j, field in enumerate(Fields):
        #grid[i+2*j].plot(rp.x.value, np.log10(rp[field].value))
        axes[j,i].plot(rp.x.value, np.log10(rp[field].value))
        axes[j,i].set_xlabel("Radius (kpc)")
        axes[j,i].set_ylabel("{}\n(log({}))".format(field, unit[j]))
        #if i == 0:
        #    #grid[i+2*j].set_title("Proton Jet: {}".format(field))
        #    axes[j,i].set_title("Proton Jet: {}".format(field))
        #else:
        #    axes[j,i].set_title("Electron Jet: {}".format(field))
plt.tight_layout()
plt.savefig("Profiles_{:03.0f}_Myr.png".format(float(ts_p[Frame].current_time/31556926e6)), dpi=300)
#plt.show()




