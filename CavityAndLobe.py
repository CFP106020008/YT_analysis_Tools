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
Datas_to_use = ['CRe','CReS']#,'CReS_SE_CB_Small']
DataSet = [Datas[i] for i in Datas_to_use]
Titles = [r'$\mathrm{CRpS}$',r'$\mathrm{CReS}$']#,r'$\mathrm{CReS~0.01GeV}$']

rc_context({'mathtext.fontset': 'stix'})

width = (100, 'kpc')
res = [500, 500]

Frames = [10,25,40,50]
orient = 'vertical'
size = 3 # inch
#fig, axes = plt.subplots(figsize=(len(Frames)*size, len(DataSet)*size), ncols=len(Frames), nrows=len(DataSet))
#fig.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0)

fig, axes, colorbars = get_multi_plot(len(Frames), len(DataSet), colorbar=orient, bw = 3)
plots = []

def One_Axis(i, j, DS, Frame, width=width, res=res, fig=fig, axes=axes, colorbars=colorbars, plots=plots, CMAP="bds_highcontrast"):
    ds = DS[Frame]
    sli = ds.slice(1, 0)
    proj = yt.ProjectionPlot(ds, 'x','Xray_Emissivity')
    proj_frb = proj.data_source.to_frb(width, res)
    frb = sli.to_frb(width, res)
    Axis = axes[i][j]
    Axis.xaxis.set_visible(False)
    Axis.yaxis.set_visible(False)
    Cavity = np.array(proj_frb['Xray_Emissivity'])
    Lobe = np.array(proj_frb['Sync'])
    Axis.imshow(Cavity)
    Axis.contour(Lobe, linewidths=0.5, colors='w')
    plots.append(Axis.imshow(Cavity, norm=LogNorm()))
    plots[-1].set_clim((M.Zlim('Xray_Emissivity')[0], M.Zlim('Xray_Emissivity')[1]))
    CMAP = 'inferno'
    plots[-1].set_cmap(CMAP)
    return fig, axes

for i, frame in enumerate(Frames):
    One_Axis(0 ,i, DataSet[0], frame)
    One_Axis(1 ,i, DataSet[1], frame)

titles = [  
            '{}'.format('Xray_Emissivity'), 
            '{}'.format('Xray_Emissivity') 
            ]

for p, cax, t in zip(plots, colorbars, titles):
    cbar = fig.colorbar(p, 
                        cax=cax, 
                        orientation=orient, 
                        format=ticker.LogFormatterMathtext())#, ticks=M.Zlim(Field))
    cbar.set_label(t)


fig.savefig('test.png', dpi=300)
