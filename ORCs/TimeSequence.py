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
from astropy.cosmology import FlatLambdaCDM

#yt.enable_parallelism()

Datas = Load_Simulation_Datas()
Datas_to_use = [#'CRpS', 
                #'CRpS_RefineTest',
                #'CReS_M13_P5_D5',
                #'CReS_M13_P5_D10',
                #'CReS_M12_P5_D5',
                #'CReS_M12_P5_D10',
                #'CReS_88',
                #'CReS_87',
                #'CReS_86',
                #'CReS_85',
                #'KIN_M13_P1_D5',
                #'MIX_M13_P1_D5',
                #'MIX_M13_P5_D5',
                #'CRpS_M14_P1_D5',
                #'CRpS_M14_P5_D1',
                #'CRpS_M14_P5_D5',
                #'CRpS_M14_P5_D5_lb23',
                #'CRpS_M13_P1_D5',
                #'CRpS_M13_P5_D1',
                #'CRpS_M13_P5_D5',
                #'CRpS_M13_P5_D5_lb23',
                #'CRpS_M12_P1_D5',
                #'CRpS_M12_P5_D1',
                'CRpS_M12_P5_D5',
                #'CReS_M13_P5_D5_OC',
                #'CReS_M12_P5_D5_OC',
                #'CRpS_M12_P5_D5_lb23',
                #'SelfRegCRp_M14',
                #'SelfRegCRe_M14',
                #'SelfRegCRp_M13',
                #'SelfRegCRp_M12',
                ]
DataSet = [Datas[i] for i in Datas_to_use]
Titles = Datas_to_use

plt.rcParams.update({"text.usetex": True})
plt.rcParams['font.family'] = 'STIXGeneral'

width = (1200, 'kpc')
res = [800, 800]
#FWHM = 1
BeamSize = 6 # arcsec

cosmo = FlatLambdaCDM(H0=70, Om0=0.3)
Distance1 = cosmo.angular_diameter_distance(z=0.551).value # ORC1
Distance5 = cosmo.angular_diameter_distance(z=0.27).value # ORC5
FWHM1 = 1#BeamSize/3600*np.pi/180*(Distance1*1000)*res[0]/width[0]
FWHM5 = 1#BeamSize/3600*np.pi/180*(Distance5*1000)*res[0]/width[0]

TYPE = 'proj'
#TYPE = 'slice'
N_frame = 4
#f_min = 12
f_min = 50
f_max = 100
Frames = np.linspace(f_min, f_max, N_frame).astype(int)
CMAP = 'inferno'
#CMAP = 'Spectral_r'
#CMAP = 'gray'

theta = 90
phi = 45
x = np.sin(theta*np.pi/180)*np.cos(phi*np.pi/180)
y = np.sin(theta*np.pi/180)*np.sin(phi*np.pi/180)
z = np.cos(theta*np.pi/180)
normal = np.array([x,y,z])

Fields_dict = { 
                'density':              0,
                'temperature':          0,
                'pressure':             0,
                'velocity_magnitude':   0,
                'CR_energy_density':    1,
                'crht':                 0,
                'csht':                 0,
                'mag_strength':         0,
                'beta_B':               0,
                'beta_CR':              0,
                'beta_th':              0,
                'cooling_time':         0,
                'Sync':                 0,
                'j_nu_Sync':            0,
                'Xray_Emissivity':      0,
                'Fake_gamma':           0,
                'Fake_gamma_electron':  0,
                'Heating_Cooling_Ratio':0
                }
Fields = [key for key in Fields_dict if Fields_dict[key]==1]
orient = 'vertical'

def One_Axis(i, j, DS, Field, Frame, plots, fig, axes, colorbars, width=width, res=res, FWHM=1, Type='slice'):
    ds = DS[Frame]
    if Type == 'slice':
        Plot = yt.SlicePlot(ds, 'z', fields=Field, width=width)
    else:
        #Plot = yt.ProjectionPlot(ds, 'x', fields=Field, width=width)
        Plot = yt.OffAxisProjectionPlot(ds, normal, fields=Field, width=width, north_vector=[0,0,1])

    Fig = Plot.export_to_mpl_figure((1,1))
    #frb  = Plot.data_source.to_frb(width, res)
    Axis = axes[i][j]
    Axis.xaxis.set_visible(False)
    Axis.yaxis.set_visible(False)
    Arr = Fig.axes[0].get_images()[0].get_array()
    Arr = gaussian_filter(Arr, FWHM)
    Arr[380:420,380:420] = 0
    #Arr = np.array(frb[Field])
    Max = np.max(Arr)
    Min = 0
    #Min = np.max(Arr)/50
    #axes[i][j] = Fig.axes[0]
    #if j == 0:
    #    global Max, Min
    #    Max = np.max(Arr)
    #    Min = np.min(Arr)
    if Type == 'slice':
        pass
        #Arr[Arr <= Min] = Min
        #Arr[Arr <= Zlim(Field)[0]] = Zlim(Field)[0]
        #print('pass')
    else:
        pass
        #Arr[Arr <= Min] = Min
        #Arr[Arr <= Zlim_Projection(Field)[0]] = Zlim_Projection(Field)[0]
    #plots.append(Fig.axes[0].get_images()[0])
    #plots.append(Axis.imshow(Arr, norm=LogNorm(np.max(Arr)/1e3, np.max(Arr))))
    if (Field == 'Fake_gamma') or (Field == 'Fake_gamma_electron') or (Field == 'j_nu_Sync'):
        #plots.append(Axis.imshow(Arr, norm=Normalize(Min, Max)))
        plots.append(Axis.imshow(Arr, norm=Normalize()))
        #plots.append(Axis.imshow(Arr, norm=LogNorm()))
        #plots.append(Axis.imshow(Arr, norm=LogNorm(Zlim_Projection(Field)[0], Zlim_Projection(Field)[1])))
        #plots.append(Axis.imshow(Arr, norm=Normalize(Zlim_Projection(Field)[0], Zlim_Projection(Field)[1])))
    else: 
        #plots.append(Axis.imshow(Arr, norm=LogNorm()))
        plots.append(Axis.imshow(Arr, norm=Normalize()))
        if Type == 'slice':
            pass
            #print('pass')
            #plots[-1].set_clim((Zlim(Field)[0], Zlim(Field)[1]))
        else:
            pass
            #plots[-1].set_clim((Zlim_Projection(Field)[0], Zlim_Projection(Field)[1]))
            #plots[-1].set_clim((Min, Max))
    plots[-1].set_cmap(CMAP)
    if j == 0:
        print('pass')
        #Axis.text(0.05, 0.95, Titles[i], c='w', horizontalalignment='left', verticalalignment='top', transform=Axis.transAxes, fontsize=15)
    if (i == len(DataSet)-1) and j == 0:
        Axis.text(0.05, 0.05, 'Box size: ' + str(width[0]) + ' kpc', c='w', horizontalalignment='left', verticalalignment='bottom', transform=Axis.transAxes, fontsize=10)
    Axis.text(0.95, 0.95, r'{:.0f} Myr'.format(M.Time(ds)), c='w', horizontalalignment='right', verticalalignment='top', transform=Axis.transAxes, fontsize=15)

def main():
    tot_num = len(Frames)*len(DataSet)
    for Field in Fields:
        fig, axes, colorbars = get_multi_plot(len(Frames), len(DataSet), colorbar=orient, bw = 3)
        plots = []
        for i, DS in enumerate(DataSet):
            for j, Frame in enumerate(Frames):
                print('Now working on {}/{} image of {} field'.format(i*len(Frames)+j+1, tot_num, Field))
                if i < 3:
                    One_Axis(i, j, DS, Field, Frame, plots=plots, fig=fig, axes=axes, colorbars=colorbars, FWHM=FWHM5, Type=TYPE)
                if i >= 3:
                    One_Axis(i, j, DS, Field, Frame, plots=plots, fig=fig, axes=axes, colorbars=colorbars, FWHM=FWHM1, Type=TYPE)

        titles = ['{}'.format(Field)]*len(DataSet) 

        for p, cax, t in zip(plots, colorbars, titles):
            cbar = fig.colorbar(p, cax=cax, orientation=orient)
            cbar.set_label(t)
            cbar.ax.yaxis.set_offset_position('left')
        fig.savefig("time_sequence_{}_{}.png".format(Field, TYPE))
        plt.close()

if __name__ == "__main__":
    main()
