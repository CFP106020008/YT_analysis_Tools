import yt
import numpy as np
from yt.visualization.api import get_multi_plot
import matplotlib.colorbar as cb
from matplotlib.colors import LogNorm
import My_Plugin as M
import matplotlib.pyplot as plt
from matplotlib import rc_context
import matplotlib.ticker as ticker

Datas = M.Load_Simulation_Datas()
Datas_to_use = ['CRpS','CReS']
DataSet = [Datas[i] for i in Datas_to_use]
Titles = [r'$\mathrm{CRpS}$',r'$\mathrm{CReS}$']#,r'$\mathrm{CReS~0.01GeV}$']

rc_context({'mathtext.fontset': 'stix'})

width = (100, 'kpc')
res = [500, 500]

Fields_dict = { 
                'density':           0,
                'temperature':       1,
                'pressure':          1,
                'CR_energy_density': 1,
                'crht':              0,
                'csht':              0,
                'mag_strength':      0,
                'beta_th':           1,
                'beta_B':            0,
                'beta_CR':           1,
                'cooling_time':      0,
                'Sync':              0
                }
Fields = [key for key in Fields_dict if Fields_dict[key]==1]
orient = 'horizontal'
fig, axes, colorbars = get_multi_plot(len(Fields), len(DataSet), colorbar=orient, bw = 3)

cmaps = [
         'gist_heat',
         'inferno',
         'inferno', 
         'Blues',
         'Blues'
         ]

Frame = 35

plots = []

def One_Axis(i, j, DS, Field, Frame, width=width, res=res, fig=fig, axes=axes, colorbars=colorbars, plots=plots, CMAP="bds_highcontrast"):
    ds = DS[Frame]
    sli = ds.slice(1, 0)
    frb = sli.to_frb(width, res)
    Axis = axes[i][j]
    Axis.xaxis.set_visible(False)
    Axis.yaxis.set_visible(False)
    Arr = np.transpose(np.array(frb[Field]))
    Arr[Arr<1e-20] = 1e-20
    plots.append(Axis.imshow(Arr, 
                             norm=LogNorm(),
                             vmin=M.Zlim(Field)[0], 
                             vmax=M.Zlim(Field)[1], 
                             cmap=CMAP))
    if j == 0:
        Axis.text(0.05, 0.95, Titles[i], c='w', horizontalalignment='left', verticalalignment='top', transform=Axis.transAxes, fontsize=15)

for i, ds in enumerate(DataSet):
    for j, Field in enumerate(Fields):
        One_Axis(i, j, ds, Field, Frame, CMAP=cmaps[j])

titles = [  
            r'$\mathrm{Temperature}\ (\mathrm{K})$',
            r'$\mathrm{Pressure}\ (\mathrm{dyne\ cm^{-2}})$',
            r'$\mathrm{CR~energy~density}\ (\mathrm{erg\ cm^{-3}})$',
            r'$\mathrm{\beta_{th}}$', 
            r'$\mathrm{\beta_{CR}}$',
            ]

for p, cax, t, Field in zip(plots, colorbars, titles, Fields):
    #print(p, cax, t, Field)
    cbar = fig.colorbar(p, 
                        cax=cax, 
                        orientation=orient, 
                        format=ticker.LogFormatterMathtext()
                        #format=ticker.LogFormatterSciNotation()
                        )#, ticks=M.Zlim(Field))
    cbar.set_label(t)
    #cbar.ax.set_xticklabels(cbar.ax.get_xticklabels(), rotation=45)
    #cbar.ax.xaxis.set_major_locator(ticker.LogLocator(base=10, numticks=15))
    #cbar.update_normal(p)
    #cbar.ax.set_xticklabels([])

# And now we're done!
fig.savefig("Field_Sequence.png", dpi=300)
