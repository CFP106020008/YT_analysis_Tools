import numpy as np
import yt
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib import rc_context
from mpl_toolkits.axes_grid1 import AxesGrid

#Set the parameters
Folder_p = "./AGNCRp/crbub_hdf5_plt_cnt_*"
Folder_e = "./AGNCRe/crbub_hdf5_plt_cnt_*"
Field = 'CR_energy_density'
#Field = 'density'
#Field = 'pressure'
#Field = 'temperature'
CMAP = 'algae' #'dusk'
Frames = [1,10,20,30,40,50]
#===========================#

ts_p = yt.load(Folder_p) #Proton Jet dataset
ts_e = yt.load(Folder_e) #Electron Jet dataset

fns = [ts_p, ts_e] # Total set of datas
def ecr(field, data):
    return data["density"]*data["cray"]*yt.YTQuantity(1,"erg/g")

yt.add_field(function = ecr, 
             units = "erg/cm**3", 
             name = "CR_energy_density", 
             sampling_type = "cell")

def Plot(Frame,ts_p,ts_e):
    
    fig = plt.figure(figsize=(64,16))
    rc_context({'mathtext.fontset': 'stix'})
    grid = AxesGrid(fig, 
                    (0.090,0.015,0.80,0.9),
                    nrows_ncols = (1, 2),
                    axes_pad = 0.5,
                    label_mode = "L",
                    share_all = True,
                    cbar_location = "right",
                    cbar_mode = "single",
                    cbar_size = "3%",
                    cbar_pad = "0%")

    # Proton Jet        
    pp = yt.SlicePlot(ts_p[Frame], 
                     'x', 
                     Field, 
                     width=(200, 'kpc')
                     ).set_cmap(field = Field, cmap=CMAP
                     )#.annotate_velocity(factor = 16,normalize=True)

    pp.set_zlim(Field, 1e-15, 1e-5) # For ecr
    #pp.set_zlim(Field, 1e-27, 1e-24) # For den
    #pp.set_zlim(Field, 1e-11, 1e-8) # For pressure
    #pp.set_zlim(Field, 1e7, 1e9) # For temp
    plotp = pp.plots[Field]        
    plotp.figure = fig
    plotp.axes = grid[0].axes
    plotp.cax = grid.cbar_axes[0]
    pp._setup_plots()

    # Electron Jet

    pe = yt.SlicePlot(ts_e[Frame], 
                     'x', 
                     Field, 
                     width=(200, 'kpc')
                     ).set_cmap(field = Field, cmap=CMAP
                     )#.annotate_velocity(factor = 16,normalize=True)

    pe.set_zlim(Field, 1e-15, 1e-5) # For ecr
    #pe.set_zlim(Field, 1e-27, 1e-24) # For den
    #pe.set_zlim(Field, 1e-11, 1e-8) # For pressure
    #pe.set_zlim(Field, 1e7, 1e9) # For temp
    plote = pe.plots[Field]        
    plote.figure = fig
    plote.axes = grid[1].axes
    plote.cax = grid.cbar_axes[1]
    pe._setup_plots()

    grid[0].axes.set_title("Proton Jet", fontsize=20)
    grid[1].axes.set_title("Electron Jet", fontsize=20)
    fig.suptitle("Time: {:03.0f} Myr".format(float(ts_p[i].current_time/31556926e6)),fontsize=24, y=0.80)

    plt.savefig("Frame={}.png".format(Frame), dpi=300, bbox='tight')
    plt.close()

for i in Frames:
    Plot(i,ts_p,ts_e)
