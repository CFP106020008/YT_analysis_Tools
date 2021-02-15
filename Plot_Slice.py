import numpy as np
import yt
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib import rc_context
from mpl_toolkits.axes_grid1 import AxesGrid
import My_Plugin as M

#Set the parameters
Folder_ps = "/data/yhlin/CRp_Streaming/crbub_hdf5_plt_cnt_*"
Folder_es = "/data/yhlin/CRe_Streaming/crbub_hdf5_plt_cnt_*"
Folder_p  = "/data/yhlin/CRp_NS/crbub_hdf5_plt_cnt_*"
Folder_e  = "/data/yhlin/CRe_NS/crbub_hdf5_plt_cnt_*"
Folder_esrc = "/data/yhlin/CReS_RC/crbub_hdf5_plt_cnt_*"

Fields = {  'crht':              0,
            'CR_energy_density': 0,
            'density':           0,
            'pressure':          0,
            'temperature':       0,
            'csht':              1,
            'mag_strength':      0,
            'beta_B':            0,
            'beta_CR':           0,
            'beta_th':           0,
            'cooling_time':      0
            }

CMAP = 'algae' #'dusk'
#Frames = [10,30,50]
Frames = [22]
Width = 100
#===========================#

CRp = yt.load(Folder_p) #Proton Jet dataset
CRe = yt.load(Folder_e) #Electron Jet dataset
CRpS = yt.load(Folder_ps) #Proton Jet dataset
CReS = yt.load(Folder_es) #Electron Jet dataset
CReS_RC = yt.load(Folder_esrc)

def Plot(Frame, Ds1, Ds2, Titles, mag=False, vel=False):
    
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
    M.One_Plot(0, Ds1, Frame, Field=Field, fig=fig, grid=grid, mag=MAG)
    M.One_Plot(1, Ds2, Frame, Field=Field, fig=fig, grid=grid, mag=MAG)
    
    grid[0].axes.set_title(Titles[0], fontsize=20)
    grid[1].axes.set_title(Titles[1], fontsize=20)
    fig.suptitle("Time: {:03.0f} Myr".format(M.Time(Ds1[Frame])),fontsize=24, y=0.80)

    plt.savefig("{}_Frame={}.png".format(Field,Frame), dpi=300, bbox='tight')
    plt.close()

Titles = ["CReS", "CReS_RC"]

for key in Fields:
    if Fields[key] ==1:
        Field = key
        if Field == 'mag_strength':
            MAG = True
        else:
            MAG = False
        for i in Frames:
            Plot(i, CReS, CReS_RC, Titles, mag=MAG)

