import yt
import numpy as np
from yt.visualization.api import get_multi_plot
import matplotlib.colorbar as cb
from matplotlib.colors import LogNorm
import My_Plugin as M
import matplotlib.pyplot as plt
from matplotlib import rc_context

Datas = M.Load_Simulation_Datas()
Datas_to_use = ['CRp', 'CRe']
#Datas_to_use = ['CRe', 'CReS']
DataSet = [Datas[i] for i in Datas_to_use]
Titles = Datas_to_use
#[r'$\mathrm{CRpS}$', r'$\mathrm{CReS}$']

rc_context({'mathtext.fontset': 'stix'})

width = (100, 'kpc')
res = [500, 500]
#TYPE = 'proj'
TYPE = 'slice'

Fields_dict = { 
                'density':           1,
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
                'Xray_Emissivity':   0
                }
Fields = [key for key in Fields_dict if Fields_dict[key]==1]
orient = 'vertical'
Frames = [10,20,30,40,50]

fig, axes, colorbars = get_multi_plot(len(Frames), len(DataSet), colorbar=orient, bw = 3)

plots = []

def One_Axis(i, j, DS, Field, Frame, width=width, res=res, fig=fig, axes=axes, colorbars=colorbars, plots=plots, Type='slice'):
    ds = DS[Frame]
    if Type == 'slice':
        Plot = yt.SlicePlot(ds, 'x', fields=Field)
    else:
        Plot = yt.ProjectionPlot(ds, 'x', fields=Field)

    frb  = Plot.data_source.to_frb(width, res)
    Axis = axes[i][j]
    Axis.xaxis.set_visible(False)
    Axis.yaxis.set_visible(False)
    Arr = np.array(frb[Field])
    if Type == 'slice':
        Arr[Arr < M.Zlim(Field)[0]] = M.Zlim(Field)[0]
    else:
        Arr[Arr < M.Zlim_Projection(Field)[0]] = M.Zlim_Projection(Field)[0]
    plots.append(Axis.imshow(Arr, norm=LogNorm()))
    if Type == 'slice':
        plots[-1].set_clim((M.Zlim(Field)[0], M.Zlim(Field)[1]))
    else:
        plots[-1].set_clim((M.Zlim_Projection(Field)[0], M.Zlim_Projection(Field)[1]))
    plots[-1].set_cmap("inferno")
    if j == 0:
        Axis.text(0.05, 0.95, Titles[i], c='w', horizontalalignment='left', verticalalignment='top', transform=Axis.transAxes, fontsize=15)
    Axis.text(0.95, 0.95, r'${} Myr$'.format(Frames[j]*2), c='w', horizontalalignment='right', verticalalignment='top', transform=Axis.transAxes, fontsize=15)

def main():
    Field = Fields[0]
    for i, DS in enumerate(DataSet):
        for j, Frame in enumerate(Frames):
            One_Axis(i, j, DS, Field, Frame, Type=TYPE)

    titles = [  
                '{}'.format(Field), 
                '{}'.format(Field) 
                ]

    for p, cax, t in zip(plots, colorbars, titles):
        cbar = fig.colorbar(p, cax=cax, orientation=orient)
        cbar.set_label(t)
    #plt.tight_layout()
    fig.savefig("Time_Sequence_{}_{}.png".format(Field, TYPE))

if __name__ == "__main__":
    main()
