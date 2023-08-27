import yt
import numpy as np
from yt.visualization.api import get_multi_plot
import matplotlib.colorbar as cb
from matplotlib.colors import LogNorm, Normalize
from My_Plugins.Zlims import Zlim, Zlim_Projection
from My_Plugins.LoadData import Load_Simulation_Datas
import My_Plugins.Fields as M
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('pdf')
from matplotlib import rc_context
from scipy.ndimage import gaussian_filter
import matplotlib.ticker as ticker

Datas = Load_Simulation_Datas()
Datas_to_use = [
                #'CRpS_M14_P1_D5',
                #'CRpS_M14_P5_D1',
                #'CRpS_M14_P5_D5',
                #'CRpS_M14_P5_D5_lb23',
                #'CRpS_M13_P1_D5',
                #'CRpS_M13_P5_D1',
                'CRpS_M13_P5_D5',
                #'CRpS_M13_P5_D5_lb23',
                #'CRpS_M12_P1_D5',
                #'CRpS_M12_P5_D1',
                'CRpS_M12_P5_D5',
                #'CRpS_M12_P5_D5_lb23',
                ]
DataSet = [Datas[i] for i in Datas_to_use]
Titles = Datas_to_use#[r'$\mathrm{CRpS}$',r'$\mathrm{CReS}$']#,r'$\mathrm{CReS~0.01GeV}$']

rc_context({'mathtext.fontset': 'stix'})

width = (1000, 'kpc')
res = [500, 500]

Fields_dict = { 
                'density':           1,
                'temperature':       1,
                'pressure':          0,
                'velocity_magnitude':0,
                'CR_energy_density': 1,
                'crht':              0,
                'csht':              0,
                'mag_strength':      1,
                'beta_B':            0,
                'beta_CR':           0,
                'beta_th':           0,
                'cooling_time':      0,
                'Sync':              0,
                'Xray_Emissivity':   0,
                'Fake_gamma':        1
                }
Fields = [key for key in Fields_dict if Fields_dict[key]==1]
orient = 'horizontal'
fig, axes, colorbars = get_multi_plot(len(Fields), len(DataSet), colorbar=orient, bw = 3)

cmaps = [
         'Spectral_r',
         'Spectral_r',
         'Spectral_r',
         'Spectral_r',
         'Spectral_r'
         ]

Frame = 100

plots = []

def One_Axis(i, j, DS, Field, Frame, width=width, res=res, fig=fig, axes=axes, colorbars=colorbars, plots=plots, CMAP="bds_highcontrast", Type='slice'):
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
        Arr[Arr < Zlim(Field)[0]] = Zlim(Field)[0]
    else:
        Arr[Arr < Zlim_Projection(Field)[0]] = Zlim_Projection(Field)[0]
    plots.append(Axis.imshow(Arr, norm=LogNorm(), cmap=CMAP))
    if Type == 'slice':
        plots[-1].set_clim((Zlim(Field)[0], Zlim(Field)[1]))
    else:
        plots[-1].set_clim((Zlim_Projection(Field)[0], Zlim_Projection(Field)[1]))
    if j == 0:
        Axis.text(0.05, 0.95, Titles[i], c='w', horizontalalignment='left', verticalalignment='top', transform=Axis.transAxes, fontsize=15)

for i, ds in enumerate(DataSet):
    for j, Field in enumerate(Fields):
        if Field == 'Xray_Emissivity':
            One_Axis(i, j, ds, Field, Frame, CMAP=cmaps[j], Type='proj')
        else:
            One_Axis(i, j, ds, Field, Frame, CMAP=cmaps[j])

titles = [  
            r'$\mathrm{Density}\ (\mathrm{g~cm^{-3}})$',
            #r'$\mathrm{Pressure}\ (\mathrm{dyne\ cm^{-2}})$',
            r'$\mathrm{Temperature}\ (\mathrm{K})$',
            r'$\mathrm{CR~Energy~Density}\ (\mathrm{erg~cm^{-3}})$',
            r'$\mathrm{B (\mathrm{G})}$', 
            r'$\mathrm{\mathrm{Hadronic~emissivity~(erg~s~cm^{-3})}}$',
            r'$\mathrm{Proj.~\epsilon_{ff}}\ (\mathrm{erg~ s^{-1} cm^{-2}})$',
            ]

for p, cax, t, Field in zip(plots, colorbars, titles, Fields):
    cbar = fig.colorbar(p, 
                        cax=cax, 
                        orientation=orient, 
                        format=ticker.LogFormatterMathtext()
                        #format=ticker.LogFormatterSciNotation()
                        )#, ticks=Zlim(Field))
    cbar.set_label(t)

# And now we're done!
fig.savefig("Field_Sequence_ORC.png", dpi=300)
