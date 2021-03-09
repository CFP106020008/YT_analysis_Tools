import numpy as np
import yt
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib import rc_context
from mpl_toolkits.axes_grid1 import AxesGrid
import My_Plugin as M

#Set the parameters
Fields = {  'crht':              0,
            'CR_energy_density': 0,
            'density':           0,
            'pressure':          0,
            'temperature':       0,
            'csht':              0,
            'mag_strength':      0,
            'beta_B':            0,
            'beta_CR':           0,
            'beta_th':           0,
            'cooling_time':      0,
            'Sync':              1
            }

CMAP = 'algae' #'dusk'
#Frames = [10,20,30,40,50]
Frames = [30]
Width = 100
#===========================#

#Folder_esrc = "/data/yhlin/CReS_RC/crbub_hdf5_plt_cnt_*"
#Folder_SpecEvo = "/data/yhlin/CReS_SpectrumEvo/crbub_hdf5_plt_cnt_*"
#CReS_RC = yt.load(Folder_esrc)
#CReS_SpecEvo = yt.load(Folder_SpecEvo)
#CRp, CRe, CRpS, CReS = M.Load_Simulation_Datas()
Datas = M.Load_Simulation_Datas()
Datas_to_use = ['CRpS', 'CReS_RC', 'CReS_SE', 'CReS_SE_Small']
DataSet = [Datas[i] for i in Datas_to_use]
Titles = ['CRpS', 'CReS_RC', 'CReS_SE', 'CReS_SE_Small']

def Plot(Frame, Ds1, Ds2, Titles, mag=False, vel=False):
    
    # Set up the figures
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

    M.One_Plot(0, Ds1, Frame, Field=Field, fig=fig, grid=grid, mag=MAG)
    M.One_Plot(1, Ds2, Frame, Field=Field, fig=fig, grid=grid, mag=MAG)
    
    grid[0].axes.set_title(Titles[0], fontsize=20)
    grid[1].axes.set_title(Titles[1], fontsize=20)
    fig.suptitle("Time: {:03.0f} Myr".format(M.Time(Ds1[Frame])),fontsize=24, y=0.80)

    plt.savefig("{}_Frame={}.png".format(Field,Frame), dpi=300, bbox='tight')
    plt.close()

Titles = ["CRpS_RC", "CReS_SpecEvo"] # The title of each figure in the plot

for key in Fields:
    if Fields[key] ==1:
        Field = key
        if Field == 'mag_strength':
            MAG = True
        else:
            MAG = False
        for i in Frames:
            Plot(i, DataSet[2], DataSet[3], Titles, mag=MAG)
