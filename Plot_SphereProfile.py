import numpy as np
import yt
import yt.units as u
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib import rc_context
from mpl_toolkits.axes_grid1 import AxesGrid
import My_Plugin as M
from matplotlib.animation import FuncAnimation

#Set the parameters
Folder_p = "./CRp/crbub_hdf5_plt_cnt_*"
#Folder_e = "./AGNCRe/crbub_hdf5_plt_cnt_*"
#Field = ['Heating/Cooling']
#Field = 'CR_energy_density'
#Field = 'density'
#Field = 'pressure'
#Field = 'temperature'
#CMAP = 'seismic'#'algae' #'dusk'
Frames = [1,10,20,30,40,50]
radius = 50
center = [0,0,0]
FPS = 10
ANIME = True
#===========================#

ts_p = yt.load(Folder_p) #Proton Jet dataset
#ts_e = yt.load(Folder_e) #Electron Jet dataset
start_frame = 1
end_frame = len(ts_p)

#fns = [ts_p, ts_e] # Total set of datas
fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(8,4.5), sharey=True)
c, = ax.semilogy([], [], label="Cooling Rate", color='b')
h, = ax.semilogy([], [], label="Heating Rate", color='r')
ax.set_xlabel("Radius (kpc)")
ax.set_ylabel(r'$(erg/s/cm^3)$')
ax.set_xlim([0,radius])
ax.set_ylim([1e-28,1e-20])
 
def Plot(frame):    
    ds = ts_p[frame]
    sphere = ds.sphere(center, (radius, "kpc"))
    P = yt.create_profile( sphere, 'radius', ['cooling_rate','crht'],
                           units = {'radius': 'kpc'},
                           logs = {'radius': False})
    
    if ANIME:
        #print("ANIEM!!")
        c.set_data(P.x.value, P['cooling_rate'].value)
        h.set_data(P.x.value, P['crht'].value)
        ax.set_title("Time: {:03.0f} Myr".format(float(ts_p[frame].current_time/31556926e6)))
    else:
        #fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(8,4.5), sharey=True)
        #plt.subplots_adjust(left=0.05, bottom=0.2, right=0.89, top=0.9, wspace=0.1, hspace=0.4) 
        #c = ax.semilogy(P.x.value, P['cooling_rate'].value, label="Cooling Rate", color='b')
        #h = ax.semilogy(P.x.value, P['crht'].value, label="Heating Rate", color='r')
        c.set_data(P.x.value, P['cooling_rate'].value)
        h.set_data(P.x.value, P['crht'].value)
        ax.set_title("Time: {:03.0f} Myr".format(float(ts_p[frame].current_time/31556926e6)))
        #plt.legend()
        #handles, labels = ax.get_legend_handles_labels()
        #fig.legend(handles, labels)#, loc='center right')
        #plt.suptitle("Time: {:03.0f} Myr".format(float(ts_p[Frame].current_time/31556926e6)))
        plt.savefig("HeatCool_Spherical_Profile_frame={}.png".format(frame), dpi=300)
        #plt.cla()
    return c, h

# Main Code
if ANIME:
    def animate(i):
        print("Making Video: {}/{}".format(i+1,len(ts_p)))
        Plot(i)

    animation = FuncAnimation(fig = fig,
                              func = animate,
                              frames = range(start_frame,end_frame),
                              interval = int(1000/FPS),
                              save_count = 0
                              )
    animation.save('HeatCoolProfile.mp4', dpi=300)
else:
    for frame in Frames:
        Plot(frame)
