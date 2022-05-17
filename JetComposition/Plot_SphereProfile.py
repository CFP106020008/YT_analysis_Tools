import numpy as np
import yt
import yt.units as u
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib import rc_context
import matplotlib
matplotlib.use('pdf')
from mpl_toolkits.axes_grid1 import AxesGrid
import My_Plugin as M
from matplotlib.animation import FuncAnimation

#Set the parameters
#Frames = [1,3,5,7,9,11,13,15] #This is for eariler epoc
#Frames = [1,10,20,30,40,50] #This is for the whole simulation time
Frames = [0] #This is for the whole simulation time
radius = 500
center = [0,0,0]
FPS = 10
#===========================#
Datas = M.Load_Simulation_Datas()
#Datas_to_use = ['CRp', 'CRe', 'CRpS', 'CReS']
Datas_to_use = ['CRpS_ORC']
DataSet = [Datas[i] for i in Datas_to_use]
start_frame = 1
end_frame = len(DataSet[0])

n = len(Frames)
colors = plt.cm.PuBu(np.linspace(0.3,1,n))

# Set the plots
'''
fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(9,8), sharey=True, sharex=True)
plt.subplots_adjust(left=0.125, bottom=0.15, right=0.8, top=0.85, wspace=0.1, hspace=0.2)
'''
fig, ax = plt.subplots()

def set_lim(ax): # Set the limit of the plots
    ax.set_xlim([0,radius])
    ax.set_ylim([1e-28,1e-24])

def Profile(Ds, frame, Field): # Calculating the profiles
    ds = Ds[frame]
    sphere = ds.sphere(center, (radius, "kpc"))
    P = yt.create_profile( sphere, 'radius', ['beta_B','cooling_rate','crht','csht','CR_Heating'],
                           units = {'radius': 'kpc'},
                           logs = {'radius': False})
    return [P.x.value, P[Field].value]
#================================================#
def ALLINONE(i, Ds, Name, ax, fig=fig): # Overplot all the profiles in one plot
    #set_lim(ax)
    [x, y] = Profile(Ds, 0, 'cooling_rate')
    ax.semilogy(x, y, linestyle='dashed',label='Cooling Rate at t = {:03.0f} Myr'.format(M.Time(Ds[0])))
    for j, frame in enumerate(Frames):
        [x, y] = Profile(Ds, frame, 'CR_Heating')
        ax.semilogy(x, y, color=colors[j], label='t = {:03.0f} Myr'.format(M.Time(Ds[frame])))
    if i/2 >= 1:
        ax.set_xlabel("Radius (kpc)")
    if i%2 == 0:
        ax.set_ylabel(r'$H_\mathrm{cr}~(\mathrm{erg~s^{-1}~cm^{-3}})$')
    ax.set_title(Name)
    ax.set_xlim([0,radius])
    ax.set_ylim([1e-28,1e-24])
    #plt.savefig("Heat_Cool_Spherical_Profile_{}.png".format(Name), dpi=300)
    #ax.clear()
#================================================#
def ANIME(Ds, ax, fig=fig): # Making animation
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
def SEQUENCE(Ds, ax, fig=fig): # Making sequence of plots
    #c, = ax.semilogy([], [], label="Cooling Rate", color='b')
    #h, = ax.semilogy([], [], label="Heating Rate", color='r')
    h, = ax.plot([], [], label="Heating Rate", color='r')
    for frame in Frames:
        [hx, hy] = Profile(Ds, frame, 'beta_B')
        print(hx, hy)
        #[cx, cy] = Profile(Ds, frame, 'cooling_rate')
        #c.set_data(cx, cy)
        h.set_data(hx, hy)
        ax.plot(hx, hy)
        ax.set_title("Time: {:03.0f} Myr".format(M.Time(Ds[frame])))
        plt.savefig("Spherical_beta_B.png".format(frame), dpi=300)

#================================================#
# Main Code

for i, Data in enumerate(DataSet):
    #ALLINONE(i, Data, Datas_to_use[i], ax=axes[int(i/2), i%2])
    SEQUENCE(Data, ax)
#handles, labels = axes[0,0].get_legend_handles_labels()
#fig.legend(handles[1:], labels[1:], loc='center right')
#plt.tight_layout()
#plt.savefig("Heat_Cool_Spherical_Profile.png", dpi=300)
plt.savefig("T=0_Profile.png", dpi=300)
