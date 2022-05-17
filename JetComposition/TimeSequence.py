import yt
import numpy as np
from yt.visualization.api import get_multi_plot
import matplotlib.colorbar as cb
from matplotlib.colors import LogNorm, Normalize
import My_Plugin as M
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('pdf')
from matplotlib import rc_context

#yt.enable_parallelism()

Datas = M.Load_Simulation_Datas()
Datas_to_use = ['CRpS','CRpS_ORCHM', 'CRpS_ORCHMLJ']
#Datas_to_use = ['CRpS_ORCHMNJ', 'CRpS_ORCHMNJNC']
#Datas_to_use = ['CRp', 'CRpS']
#Datas_to_use = ['CRe', 'CReS']
DataSet = [Datas[i] for i in Datas_to_use]
Titles = Datas_to_use
#[r'$\mathrm{CRpS}$', r'$\mathrm{CReS}$']

rc_context({'mathtext.fontset': 'stix'})

width = (250, 'kpc')
res = [500, 500]
TYPE = 'proj'
#TYPE = 'slice'
theta = 20*np.pi/180 #deg
phi = 0*np.pi/180
Frames = [0,10,20,30,40,50]
#Frames = [5,10,15,20]

x = np.sin(theta)*np.cos(phi)
y = np.sin(theta)*np.sin(phi)
z = np.cos(theta)
normal = np.array([x,y,z])

Fields_dict = { 
                'density':           0,
                'temperature':       0,
                'pressure':          0,
                'velocity_magnitude':0,
                'CR_energy_density': 0,
                'crht':              0,
                'csht':              0,
                'mag_strength':      0,
                'beta_B':            0,
                'beta_CR':           0,
                'beta_th':           0,
                'cooling_time':      0,
                'Sync':              0,
                'Xray_Emissivity':   0,
                'Fake_gamma':        1
                }
Fields = [key for key in Fields_dict if Fields_dict[key]==1]
orient = 'vertical'
#Frames = [5,15,25,35]
#Frames = [3,6,9,12]

def One_Axis(i, j, DS, Field, Frame, plots, fig, axes, colorbars, width=width, res=res, Type='slice'):
    ds = DS[Frame]
    if Type == 'slice':
        Plot = yt.SlicePlot(ds, 'x', fields=Field, width=width)
    else:
        #Plot = yt.ProjectionPlot(ds, 'z', fields=Field, width=width)
        Plot = yt.OffAxisProjectionPlot(ds, normal, fields=Field, width=width)
        #Plot.annotate_scale()

    Fig = Plot.export_to_mpl_figure((1,1))
    #frb  = Plot.data_source.to_frb(width, res)
    Axis = axes[i][j]
    Axis.xaxis.set_visible(False)
    Axis.yaxis.set_visible(False)
    Arr = Fig.axes[0].get_images()[0].get_array()
    #Arr = np.array(frb[Field])
    Max = np.max(Arr)
    Min = np.max(Arr)/50
    #axes[i][j] = Fig.axes[0]
    if Type == 'slice':
        #Arr[Arr <= Min] = Min
        Arr[Arr <= M.Zlim(Field)[0]] = M.Zlim(Field)[0]
    else:
        #Arr[Arr <= Min] = Min
        Arr[Arr <= M.Zlim_Projection(Field)[0]] = M.Zlim_Projection(Field)[0]
    #plots.append(Fig.axes[0].get_images()[0])
    #plots.append(Axis.imshow(Arr, norm=LogNorm()))
    #plots.append(Axis.imshow(Arr, norm=LogNorm(np.max(Arr)/1e3, np.max(Arr))))
    plots.append(Axis.imshow(Arr, norm=Normalize(Min, Max)))
    '''
    if Type == 'slice':
        plots[-1].set_clim((M.Zlim(Field)[0], M.Zlim(Field)[1]))
    else:
        plots[-1].set_clim((M.Zlim_Projection(Field)[0], M.Zlim_Projection(Field)[1]))
    '''
    plots[-1].set_cmap("inferno")
    if j == 0:
        Axis.text(0.05, 0.95, Titles[i], c='w', horizontalalignment='left', verticalalignment='top', transform=Axis.transAxes, fontsize=15)
    Axis.text(0.95, 0.95, r'{:.0f} Myr'.format(M.Time(ds)), c='w', horizontalalignment='right', verticalalignment='top', transform=Axis.transAxes, fontsize=15)

def main():
    tot_num = len(Frames)*len(DataSet)
    for Field in Fields:
        fig, axes, colorbars = get_multi_plot(len(Frames), len(DataSet), colorbar=orient, bw = 3)
        plots = []
        for i, DS in enumerate(DataSet):
            for j, Frame in enumerate(Frames):
                print('Now working on {}/{} image'.format(i*len(DataSet)+j,tot_num))
                One_Axis(i, j, DS, Field, Frame, plots=plots, fig=fig, axes=axes, colorbars=colorbars, Type=TYPE)

        titles = ['{}'.format(Field)]*len(DataSet) 

        for p, cax, t in zip(plots, colorbars, titles):
            cbar = fig.colorbar(p, cax=cax, orientation=orient)
            cbar.set_label(t)
        fig.savefig("Time_Sequence_{}_{}.png".format(Field, TYPE))
        plt.close()

if __name__ == "__main__":
    main()
