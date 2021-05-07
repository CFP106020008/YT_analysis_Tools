import yt
import numpy as np
from yt.visualization.api import get_multi_plot
import matplotlib.colorbar as cb
from matplotlib.colors import LogNorm
import My_Plugin as M
import matplotlib.pyplot as plt
from matplotlib import rc_context

Datas = M.Load_Simulation_Datas()
Datas_to_use = ['CRe', 'CReS']
DataSet = [Datas[i] for i in Datas_to_use]
Titles = [r'$\mathrm{CRpS}$', r'$\mathrm{CReS}$']

rc_context({'mathtext.fontset': 'stix'})

width = (100, 'kpc')
res = [500, 500]

Fields_dict = { 
                'density':           0,
                'temperature':       0,
                'pressure':          0,
                'CR_energy_density': 0,
                'crht':              0,
                'csht':              0,
                'mag_strength':      0,
                'beta_B':            0,
                'beta_CR':           0,
                'beta_th':           0,
                'cooling_time':      0,
                'Sync':              0,
                'Xray_Emissivity':   1
                }
Fields = [key for key in Fields_dict if Fields_dict[key]==1]
orient = 'vertical'
Frames = [1,10,20,30,40]

fig, axes, colorbars = get_multi_plot(len(Frames), len(DataSet), colorbar=orient, bw = 3)

plots = []

def One_Axis(i, j, DS, Field, Frame, width=width, res=res, fig=fig, axes=axes, colorbars=colorbars, plots=plots, Type='slice'):
    ds = DS[Frame]
    if Type == 'slice':
        Plot = yt.SlicePlot(ds, 'x', fields=Field)
    else:
        Plot = yt.ProjectionPlot(ds, 'x', fields=Field)

    frb  = Plot.data_source.to_frb(width, res)
    #frb = sli.to_frb(width, res)
    #frb = pro.to_frb(width, res)
    Axis = axes[i][j]
    Axis.xaxis.set_visible(False)
    Axis.yaxis.set_visible(False)
    Arr = np.array(frb[Field])
    Arr[Arr==0] = 1e-99
    print(Arr)
    plots.append(Axis.imshow(Arr, norm=LogNorm()))
    plots[-1].set_clim((M.Zlim(Field)[0], M.Zlim(Field)[1]))
    plots[-1].set_cmap("inferno")
    if j == 0:
        Axis.text(0.05, 0.95, Titles[i], c='k', horizontalalignment='left', verticalalignment='top', transform=Axis.transAxes, fontsize=15)
    Axis.text(0.95, 0.95, r'${} Myr$'.format(Frames[j]*2), c='k', horizontalalignment='right', verticalalignment='top', transform=Axis.transAxes, fontsize=15)

Field = Fields[0]
for i, DS in enumerate(DataSet):
    for j, Frame in enumerate(Frames):
        One_Axis(i, j, DS, Field, Frame, Type='proj')

titles = [  
            '{}'.format(Field), 
            '{}'.format(Field) 
            ]

for p, cax, t in zip(plots, colorbars, titles):
    cbar = fig.colorbar(p, cax=cax, orientation=orient)
    cbar.set_label(t)
# And now we're done!
plt.tight_layout()
fig.savefig("Time_Sequence.png")
