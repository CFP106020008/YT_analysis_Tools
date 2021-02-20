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
#Frames = [1,3,5,7,9,11,13,15] #This is for eariler epoc
Frames = [1,10,20,30,40,50] #This is for the whole simulation time
radius = 100
center = [0,0,0]
FPS = 10
#===========================#
CRp, CRe, CRpS, CReS = M.Load_Simulation_Datas()
start_frame = 1
end_frame = len(CRpS)

n = len(Frames)
colors = plt.cm.PuBu(np.linspace(0.3,1,n))

# Set the plots
fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(8,4.5), sharey=True)
ax.set_xlabel("Radius (kpc)")
ax.set_ylabel(r'$(erg/s/cm^3)$')

def set_lim(ax): # Set the limit of the plots
    ax.set_xlim([0,radius])
    ax.set_ylim([1e-28,1e-24])

def Profile(Ds, frame, Field): # Calculating the profiles
    ds = Ds[frame]
    sphere = ds.sphere(center, (radius, "kpc"))
    P = yt.create_profile( sphere, 'radius', ['cooling_rate','crht','csht','CR_Heating'],
                           units = {'radius': 'kpc'},
                           logs = {'radius': False})
    return [P.x.value, P[Field].value]
#================================================#
def ALLINONE(Ds, Name, fig=fig, ax=ax): # Overplot all the profiles in one plot
    set_lim(ax)
    [x, y] = Profile(Ds, 0, 'cooling_rate')
    ax.semilogy(x, y, linestyle='dashed',label='Cooling Rate at t = {:03.0f} Myr'.format(M.Time(Ds[0])))
    for i, frame in enumerate(Frames):
        [x, y] = Profile(Ds, frame, 'CR_Heating')
        ax.semilogy(x, y, color=colors[i], label='CR Heating Rate at t = {:03.0f} Myr'.format(M.Time(Ds[frame])))
    plt.legend()
    plt.savefig("Heat_Cool_Spherical_Profile_{}.png".format(Name), dpi=300)
    ax.clear()
#================================================#
def ANIME(Ds, fig=fig, ax=ax): # Making animation
    c, = ax.semilogy([], [], label="Cooling Rate", color='b')
    h, = ax.semilogy([], [], label="Heating Rate", color='r')
    def animate(i):
        print("Making Video: {}/{}".format(i+1,end_frame))
        [hx, hy] = Profile(Ds, i, 'CR_Heating')
        [cx, cy] = Profile(Ds, i, 'cooling_rate')
        c.set_data(cx, cy)
        h.set_data(hx, hy)
        ax.set_title("Time: {:03.0f} Myr".format(M.Time(Ds[i])))
    animation = FuncAnimation(fig = fig,
                              func = animate,
                              frames = range(start_frame, end_frame),
                              interval = int(1000/FPS),
                              save_count = 0
                              )
    animation.save('HeatCoolProfile.mp4', dpi=300)
#================================================#
def SEQUENCE(Ds, fig=fig, ax=ax): # Making sequence of plots
    c, = ax.semilogy([], [], label="Cooling Rate", color='b')
    h, = ax.semilogy([], [], label="Heating Rate", color='r')
    for frame in Frames:
        [hx, hy] = Profile(Ds, frame, 'CR_Heating')
        [cx, cy] = Profile(Ds, frame, 'cooling_rate')
        c.set_data(cx, cy)
        h.set_data(hx, hy)
        ax.set_title("Time: {:03.0f} Myr".format(M.Time(Ds[frame])))
        plt.savefig("HeatCool_Spherical_Profile_frame={}.png".format(frame), dpi=300)

#================================================#
# Main Code
ALLINONE(CRpS, 'CRpS')
ALLINONE(CReS, 'CReS')
ALLINONE(CRp, 'CRp')
ALLINONE(CRe, 'CRe')

