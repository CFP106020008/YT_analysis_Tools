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

fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(8,4.5))
plt.subplots_adjust(left=0.125, bottom=0.1, right=0.9, top=0.9, wspace=0.4, hspace=0.4)

lines = []

for i, jet in enumerate(fns):
    ds = jet[Frame]
    disk = ds.disk(center, [0,0,1], radius, height)
    rp = yt.create_profile(disk, 'radius', Fields,
                           units = {'radius': 'kpc'},
                           logs = {'radius': False})
    for j, field in enumerate(Fields):
        if i == 0:
            l = axes[int(j/2),j%2].plot(rp.x.value, np.log10(rp[field].value), label="Proton Jet")
        else:
            l = axes[int(j/2),j%2].plot(rp.x.value, np.log10(rp[field].value), label="Electron Jet")
        axes[int(j/2),j%2].set_xlabel("Radius (kpc)")
        axes[int(j/2),j%2].set_ylabel("{}\n(log({}))".format(field, unit[j]))
        lines.append(l)

LABEL = ["Proton Jet", "Electron Jet"]
#handles, labels = axes.get_legend_handles_labels()
fig.legend(lines[:2], LABEL, loc='lower center')
#plt.tight_layout()
plt.suptitle("Time: {:03.0f} Myr".format(float(ts_p[Frame].current_time/31556926e6)))
plt.savefig("Profiles_{:03.0f}_Myr.png".format(float(ts_p[Frame].current_time/31556926e6)), dpi=300)
#plt.show()
