import numpy as np
import yt
import yt.units as u
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import AxesGrid
from matplotlib import rc_context
import My_Plugin as M

#Set the parameters
Folder_p = "./AGNCRp/crbub_hdf5_plt_cnt_*"
Folder_e = "./AGNCRe/crbub_hdf5_plt_cnt_*"
Frames = [1,10,20,30,40,50] #The frame to plot the profiles
Fields = ['density','CR_energy_density','pressure', 'temperature']
unit = [r'$erg/cm^3$',r'$erg/cm^3$',r'$erg/cm^3$',r'$K$']
radius = 50*u.kpc
height = 20*u.kpc
heights = [1*u.kpc, 20*u.kpc, 25*u.kpc, 30*u.kpc, 40*u.kpc, 45*u.kpc]
center = [0,0,0]
#===========================#

ts_p = yt.load(Folder_p) #Proton Jet dataset
ts_e = yt.load(Folder_e) #Electron Jet dataset

fns = [ts_p, ts_e]

def FourFig(Frame, height):
    fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(8,4.5))
    plt.subplots_adjust(left=0.125, bottom=0.2, right=0.9, top=0.9, wspace=0.4, hspace=0.4)
    for i, jet in enumerate(fns):
        ds = jet[Frame]
        disk = ds.disk(center, [0,0,1], radius, height)
        rp = yt.create_profile(disk, 'radius', Fields,
                               units = {'radius': 'kpc'},
                               logs = {'radius': False})
        for j, field in enumerate(Fields):
            if i == 0:
                l = axes[int(j/2),j%2].plot(rp.x.value, np.log10(rp[field].value), label="Proton Jet", color='r')
            else:
                l = axes[int(j/2),j%2].plot(rp.x.value, np.log10(rp[field].value), label="Electron Jet", color='b')
            axes[int(j/2),j%2].set_xlabel("Radius (kpc)")
            axes[int(j/2),j%2].set_ylabel("{}\n(log({}))".format(field, unit[j]))

    LABEL = ["Proton Jet", "Electron Jet"]
    handles, labels = axes[0,0].get_legend_handles_labels()
    fig.legend(handles, labels, loc='lower center')
    plt.suptitle("Time: {:03.0f} Myr, Height: {}".format(float(ts_p[Frame].current_time/31556926e6),height))
    plt.savefig("Profiles_{:03.0f}_Myr.png".format(float(ts_p[Frame].current_time/31556926e6)), dpi=300)
    plt.close()

def TimeSequence(Fields, Frames):
    for k, field in enumerate(Fields):
        fig, axes = plt.subplots(nrows=1, ncols=len(Frames), figsize=(4*len(Frames),4), sharey=True)
        plt.subplots_adjust(left=0.05, bottom=0.2, right=0.89, top=0.9, wspace=0.1, hspace=0.4)
        for i, jet in enumerate(fns):
            for j, frame in enumerate(Frames):
                ds = jet[frame]
                disk = ds.disk(center, [0,0,1], radius, height)
                rp = yt.create_profile(disk, 'radius', Fields,
                                       units = {'radius': 'kpc'},
                                       logs = {'radius': False})
                if i == 0:
                    l = axes[j].plot(rp.x.value, np.log10(rp[field].value), label="Proton Jet")
                else:
                    l = axes[j].plot(rp.x.value, np.log10(rp[field].value), label="Electron Jet")
                axes[j].set_xlabel("Radius (kpc)")
                axes[j].set_title("Time: {:03.0f} Myr".format(float(ts_p[frame].current_time/31556926e6)))

        axes[0].set_ylabel("{}\n(log({}))".format(field, unit[k]))
        LABEL = ["Proton Jet", "Electron Jet"]
        handles, labels = axes[0].get_legend_handles_labels()
        fig.legend(handles, labels, loc='center right')
        #plt.suptitle("Time: {:03.0f} Myr".format(float(ts_p[Frame].current_time/31556926e6)))
        plt.savefig("Profile_Sequence_{}.png".format(field), dpi=300)
        plt.close()

#TimeSequence(Fields, Frames)
for i in range(len(Frames)):
    FourFig(Frames[i],heights[i])
