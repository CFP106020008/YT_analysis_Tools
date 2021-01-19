import numpy as np
import yt
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib import rc_context
from mpl_toolkits.axes_grid1 import AxesGrid
import My_Plugin as M

#Set the parameters
Folder_p = "./CRp_Streaming/crbub_hdf5_plt_cnt_*"
Folder_e = "./CRe_Streaming/crbub_hdf5_plt_cnt_*"
Fields = {  'crht': 0,
            'CR_energy_density': 1,
            'density': 0,
            'pressure': 0,
            'temperature': 0,
            'csht': 0,
            'mag_strength': 0}
CMAP = 'algae' #'dusk'
Frames = [10,30,50]
#Frames = [11]
Width = 100
#===========================#

ts_p = yt.load(Folder_p) #Proton Jet dataset
ts_e = yt.load(Folder_e) #Electron Jet dataset

fns = [ts_p, ts_e] # Total set of datas

def Plot(Frame, ts_p, ts_e, mag=False, vel=False):
    
    fig = plt.figure(figsize=(16,16))
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
    M.One_Plot(0, ts_p, Frame, Field=Field, fig=fig, grid=grid, mag=MAG)
    M.One_Plot(1, ts_e, Frame, Field=Field, fig=fig, grid=grid, mag=MAG)
    
    grid[0].axes.set_title("Proton Jet", fontsize=20)
    grid[1].axes.set_title("Electron Jet", fontsize=20)
    fig.suptitle("Time: {:03.0f} Myr".format(float(ts_p[i].current_time/31556926e6)),fontsize=24, y=0.80)

    plt.savefig("{}_Frame={}.png".format(Field,Frame), dpi=300, bbox='tight')
    plt.close()

for key in Fields:
    if Fields[key] ==1:
        Field = key
        if Field == 'mag_strength':
            MAG = True
        else:
            MAG = False
        for i in Frames:
            Plot(i, ts_p, ts_e, mag=MAG)

