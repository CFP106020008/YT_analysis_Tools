import yt
import numpy as np
from yt.visualization.api import get_multi_plot
import matplotlib.colorbar as cb
from matplotlib.colors import LogNorm, SymLogNorm
import My_Plugin as M
import matplotlib.pyplot as plt
from matplotlib import rc_context
import matplotlib.ticker as ticker

Datas = M.Load_Simulation_Datas()
Datas_to_use = ['CRpS','CReS']
DataSet = [Datas[i] for i in Datas_to_use]
Titles = [r'$\mathrm{CRpS}$',r'$\mathrm{CReS}$']#,r'$\mathrm{CReS~0.01GeV}$']

kpc2cm = 3e21
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
                'beta_th':           0,
                'beta_B':            0,
                'beta_CR':           0,
                'cooling_time':      0,
                'adiabatic_time':    1,
                'Sync':              0
                }
Fields = [key for key in Fields_dict if Fields_dict[key]==1]
Field  = Fields[0]
Frames = [5,10,30]
orient = 'vertical'
fig, axes, colorbars = get_multi_plot(len(Frames)*2, len(DataSet), colorbar=orient, bw = 3)

Myr2s = 31556952000000
cmaps = [
         'inferno',
         'inferno',
         'inferno', 
         'Blues',
         'Blues'
         ]


plots = []

def One_Axis(i, j, DS, Field, Frame, width=width, res=res, fig=fig, axes=axes, colorbars=colorbars, plots=plots, CMAP="bds_highcontrast"):
    ds = DS[Frame]
    sp = ds.sphere(ds.domain_center, (100, "kpc"))
    slc = yt.SlicePlot(ds, 'x', fields = [Field, "Sync_timescale"],data_source=sp)
    print("i: ",i)
    print("j: ",j)
    Axis = axes[i][j*2]
    Axis.xaxis.set_visible(False)
    Axis.yaxis.set_visible(False)
    Arr1 = np.array(slc.data_source.to_frb(width, res)[Field])
    plots.append(Axis.imshow(Arr1, 
                             norm=SymLogNorm(linthresh=1,
                                             vmin=M.Zlim(Field)[0],
                                             vmax=M.Zlim(Field)[1]),
                             cmap=CMAP))
    Axis.text(0.95, 0.95, '{} Myr'.format(2*Frames[j]), c='w', horizontalalignment='right', verticalalignment='top', transform=Axis.transAxes, fontsize=15)
    Axis.vlines(250,0,500)
    # Plot profile
    Arr2 = np.array(slc.data_source.to_frb(width, res)["Sync_timescale"])
    Axis2 = axes[i][j*2+1]
    #Axis2.xaxis.set_visible(False)
    #Axis2.yaxis.set_visible(False)
    Axis2.plot(Arr1[:,250],np.linspace(-50, 50, 500), label="Adiabatic_timescale", color='b')
    Axis2.vlines(0,-50,50, color='k')
    Axis2.set_ylim([-50, 50])
    Axis2.set_xlim([-10, 10])
    Axis2.plot(Arr2[:,250],np.linspace(-50, 50, 500), label="Sync_timescale", color='r')
    Axis2.legend()
    if j == 0:
        Axis.text(0.05, 0.95, Titles[i], c='w', horizontalalignment='left', verticalalignment='top', transform=Axis.transAxes, fontsize=15)

#Field = 'density'
for i, DS in enumerate(DataSet):
    for j, Frame in enumerate(Frames):
        One_Axis(i, j, DS, Field, Frame, CMAP='RdBu_r')
        #One_Axis(i, j, DS, Field, Frame, Type='proj')

#titles = ['{} Myr'.format(frame*2) for frame in Frames]
titles = [
          'Adiabatic cooling timescale (Myr)',
          'Adiabatic cooling timescale (Myr)'
          ]

for p, cax, t in zip(plots, colorbars, titles):
    cbar = fig.colorbar(p, cax=cax, orientation=orient)
    cbar.set_label(t)

plt.show()
fig.savefig("Time_Sequence_{}.png".format(Field), dpi=300)
