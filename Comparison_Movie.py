import numpy as np
import yt
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib import rc_context
from mpl_toolkits.axes_grid1 import AxesGrid

#Set the parameters
Folder_p = "./AGNCRp/crbub_hdf5_plt_cnt_*"
Folder_e = "./AGNCRe/crbub_hdf5_plt_cnt_*"
Fields = ['density']#, 'CR_energy_density', 'pressure', 'temperature']
CMAP = 'algae' #'dusk'
FPS = 20
SAVE_IMAGE = False

#===========================#
fig = plt.figure(figsize=(16,9))

ts_p = yt.load(Folder_p) #Proton Jet dataset
ts_e = yt.load(Folder_e) #Electron Jet dataset

fns = [ts_p, ts_e] # Total set of datas
def ecr(field, data):
    return data["density"]*data["cray"]*yt.YTQuantity(1,"erg/g")

yt.add_field(function = ecr, 
             units = "erg/cm**3", 
             name = "CR_energy_density", 
             sampling_type = "cell")

def One_frame(j):
    
    #fig = plt.figure(figsize=(16,9))
    rc_context({'mathtext.fontset': 'stix'})
    grid = AxesGrid(fig, (0.090,0.075,0.80,0.85),
                    nrows_ncols = (1, 2),
                    axes_pad = 0.5,
                    label_mode = "L",
                    share_all = True,
                    cbar_location = "right",
                    cbar_mode = "single",
                    cbar_size = "3%",
                    cbar_pad = "0%")
    
    for i, fn in enumerate(fns):
    
        # Load the data and create a single plot        
        p = yt.SlicePlot(fn[j], 
                         'x', 
                         Field, 
                         width=(200, 'kpc')
                         ).set_cmap(field = Field, cmap=CMAP
                         )#.annotate_velocity(factor = 16,normalize=True)

        # Ensure the colorbar limits match for all plots
        #p.set_zlim(Field, 1e-40, 1e0) # For ecr
        p.set_zlim(Field, 1e-27, 1e-24) # For den

        plot = p.plots[Field]        
        plot.figure = fig
        plot.axes = grid[i].axes
        plot.cax = grid.cbar_axes[i]
        p._setup_plots()
        
        if i == 0:
            Name = "Proton Jet"
        else:
            Name = "Electron Jet"
        grid[i].axes.set_title(Name, fontsize=20)
    
    if SAVE_IMAGE:
        plt.savefig("./temp-store/{}_frame={:04d}.png".format(Field,j),dpi=300)

    return fig

def animate(i):
    print("Making Video: {}/{}".format(i+1,len(ts_p)))
    p.
    
    
    One_frame(i)
    #plt.close()

animation = FuncAnimation(fig = fig, 
                          func = animate, 
                          frames = 3,#min(len(ts_p),len(ts_e)),
                          interval = int(1000/FPS), 
                          save_count = 0
                          )

for Field in Fields:
    #One_frame(30)
    animation.save('Comparison_{}.mp4'.format(Field), dpi=300)
    #for i in range(min(len(ts_p),len(ts_e))):
    #    One_frame(i)
    #    plt.close()
    #    print("Making Video: {}/{}".format(i+1,len(ts_p)))
