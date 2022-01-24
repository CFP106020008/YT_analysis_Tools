import yt
import numpy as np
from yt.visualization.api import get_multi_plot
import matplotlib.colorbar as cb
import matplotlib
matplotlib.use('pdf')
from matplotlib.colors import LogNorm
#import My_Plugin as M
import My_Fields as M
import matplotlib.pyplot as plt
from matplotlib import rc_context
import matplotlib.ticker as ticker

Datas = M.Load_Simulation_Datas()
Datas_to_use = ['CReS_HighFPS']
DataSet = [Datas[i] for i in Datas_to_use]

rc_context({'mathtext.fontset': 'stix'})

width = (100, 'kpc')
res = [800, 800]

Fields_dict = { 
                'density':           0,
                'temperature':       1,
                'pressure':          1,
                'CR_energy_density': 0,
                'crht':              0,
                'csht':              0,
                'mag_strength':      0,
                'beta_th':           0,
                'beta_B':            0,
                'beta_CR':           0,
                'cooling_time':      0,
                'Sync':              0
                }
Fields = [key for key in Fields_dict if Fields_dict[key]==1]
orient = 'horizontal'
fig, ax = plt.subplots(figsize=(6, 6)) 

Frames = np.arange(301)
plots = []
cmaps = [
         'gist_heat',
         'inferno'
         ]

def One_Axis(i, j, DS, Field, Frame, width=width, res=res, fig=fig, ax=ax, plots=plots, CMAP="bds_highcontrast"):
    ds = DS[Frame]
    sli = ds.slice('x', 0.5)
    frb = sli.to_frb(width, res)
    Axis = ax
    Axis.xaxis.set_visible(False)
    Axis.yaxis.set_visible(False)
    Arr = np.array(frb[Field])
    #Arr[Arr==0] = 1e-99
    IMG = ax.imshow(Arr, norm=LogNorm())
    IMG.set_clim(1,2)
    IMG.set_clim(M.Zlim(Field)[0], M.Zlim(Field)[1])
    IMG.set_cmap(CMAP)
    #if j == 0:
    #    Axis.text(0.05, 0.95, Titles[i], c='w', horizontalalignment='left', verticalalignment='top', transform=Axis.transAxes, fontsize=15)

for i, ds in enumerate(DataSet):
    for j, Field in enumerate(Fields):
        for k, frame in enumerate(Frames):
            One_Axis(i, j, ds, Field, frame, CMAP=cmaps[j])
            fig.subplots_adjust(0,0,1,1)
            fig.savefig("{}_{}_{:04d}.jpg".format(Datas_to_use[i], Field, frame), dpi=300)
            ax.cla()
