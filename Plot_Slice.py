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

#CMAP = 'B-W LINEAR'#'algae' #'dusk'
CMAP = 'inferno'#'algae' #'dusk'
#Frames = [10,20,30,40,50]
Frames = [30]
Width = 100
#===========================#

Datas = M.Load_Simulation_Datas()
Datas_to_use = ['CRe', 'CReS']
DataSet = [Datas[i] for i in Datas_to_use]
Titles = ['CRe', 'CReS']

def Plot(Frame, Ds1, Ds2, Titles, mag=False, vel=False):
    
    # Set up the figures
    fig = plt.figure(figsize=(16,8))
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

    M.One_Plot(0, Ds1, Frame, Field=Field, fig=fig, grid=grid, mag=MAG, CMAP=CMAP)
    M.One_Plot(1, Ds2, Frame, Field=Field, fig=fig, grid=grid, mag=MAG, CMAP=CMAP)
    
    grid[0].axes.set_title(Titles[0], fontsize=20)
    grid[1].axes.set_title(Titles[1], fontsize=20)
    fig.suptitle("Time: {:03.0f} Myr".format(M.Time(Ds1[Frame])),fontsize=24, y=0.80)

    plt.savefig("{}_Frame={}.png".format(Field,Frame), dpi=300, bbox='tight')
    plt.close()

def Big_Plot(DS, Titles, Epochs):
    fig = plt.figure(figsize=(10,10))
    rc_context({'mathtext.fontset': 'stix'})
    grid = AxesGrid(fig, 
                    (0.05,0.05,0.8,0.9),
                    nrows_ncols = (len(DS), len(Epochs)),
                    axes_pad = 0.,
                    label_mode = "L",
                    share_all = True,
                    cbar_location = "right",
                    cbar_mode = "single",
                    cbar_size = "3%",
                    cbar_pad = "0%")
    for i, ds in enumerate(DS):
        for j, frame in enumerate(Epochs):
            ID = i*len(Epochs) + j
            M.One_Plot(ID, ds, frame, Field=Field, fig=fig, grid=grid, mag=MAG, CMAP=CMAP)
            grid[ID].axes.xaxis.set_visible(False)
            grid[ID].axes.yaxis.set_visible(False)
    fig.savefig("Multi_Compare.png", dpi=300)
    plt.close()

for key in Fields:
    if Fields[key] ==1:
        Field = key
        if Field == 'mag_strength':
            MAG = True
        else:
            MAG = False
        for i in Frames:
            #Big_Plot(DataSet, Titles, [1,10,20,30,40,50])
            Plot(i, DataSet[0], DataSet[1], Titles, mag=MAG)
