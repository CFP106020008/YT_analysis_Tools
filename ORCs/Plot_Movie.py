# This code is created by Lin Yen-Hsing (NTHU, 2022) on CICA cluster
import numpy as np
import os

import yt
import matplotlib
import matplotlib.colorbar as cb
import matplotlib.pyplot as plt
from matplotlib import rc_context
from scipy.ndimage import gaussian_filter

from My_Plugins.Zlims import Zlim, Zlim_Projection
from My_Plugins.LoadData import Load_Simulation_Datas
import My_Plugins.Fields as M

# Setup the parameters
# ======================================== #
width = (1000, 'kpc') # Visualization box size
FWHM = 1

#TYPE = 'proj'
TYPE = 'slice'
#TYPE = 'offaxis'

# Orientation of the camera
# Only important when using offaxis plot
theta = 20*np.pi/180 #deg
phi = 0*np.pi/180 # deg

# The simulations
Datas_to_use = [ 
                #'CRpS_RefineTest',
                #'CReS_M13_P5_D5',
                #'CReS_M13_P5_D10',
                #'CReS_M12_P5_D5',
                #'CReS_M12_P5_D10',
                #'CRpS_M13_P5_D5',
                'CRpS_M12_P5_D5',
                #'MIX_M13_P5_D5',
                #'SelfRegCRp_M14',
                #'SelfRegCRe_M14',
                #'SelfRegCRp_M13',
                #'SelfRegCRp_M12',
                ]
# The fields
Fields_dict = { 
                'density':            0,
                'temperature':        0,
                'pressure':           0,
                'velocity_magnitude': 0,
                'CR_energy_density':  0,
                'crht':               0,
                'csht':               0,
                'mag_strength':       0,
                'beta_B':             0,
                'beta_CR':            0,
                'beta_th':            0,
                'cooling_time':       0,
                'Sync':               0,
                'Xray_Emissivity':    0,
                'Fake_gamma':         1,
                'Fake_gamma_electron':0
                }

# ======================================== #

# Load the simulation data into a list
Datas = Load_Simulation_Datas()
DataSet = [Datas[i] for i in Datas_to_use]
Titles = Datas_to_use

# Make the list of all the fields 
Fields = [key for key in Fields_dict if Fields_dict[key]==1]

#rc_context({'mathtext.fontset': 'stix'}) # To make pretty fonts
x = np.sin(theta)*np.cos(phi)
y = np.sin(theta)*np.sin(phi)
z = np.cos(theta)
normal = np.array([x,y,z]) # Calculate normal vector for off axis plot

# Frames
start = 0
end = len(DataSet[0])
Frames = np.arange(start, end)

# CMAP
#CMAP = 'gray'
#CMAP = 'inferno'
CMAP = 'Spectral_r'

matplotlib.use('pdf') # Avoid pop-up windows

# ======================================== #

def Plot(ds, TYPE, width, field, folder, 
         normal=[0,0,1], linear_scale=False, velocity_vector=False, CMAP='inferno', spatial_scale=False):
    if TYPE == 'slice':
        p = yt.SlicePlot(ds, 
                         'x', 
                         field, 
                         width=width)
        p.set_zlim(field, Zlim(field)[0], Zlim(field)[1])
    elif TYPE == 'proj':
        p = yt.ProjectionPlot(ds, 
                              'z', 
                              field, 
                              width=width)
        p.set_zlim(field, Zlim_Projection(field)[0], Zlim_Projection(field)[1])
    elif TYPE == 'offaxis':
        p = yt.OffAxisProjectionPlot(ds, normal, fields=field, width=width)
    else:
        print('What are you doing?! Wrong TYPE!')

    if linear_scale:
        p.set_log(field, False)
    if velocity_vector:
        p.annotate_velocity(normalize=True)
    if spatial_scale:
        p.annotate_scale(coeff=100, unit='kpc')
    p.set_cmap(field, CMAP)
    #p.frb[field] = gaussian_filter(p.frb[field], 30)
    #p.frb = p.frb.apply_white_noise()
    p.annotate_text((0.05, 0.95), "{:.0f} Myr".format(M.Time(ds)), coord_system='axis', text_args={'verticalalignment': 'center', 'color':'white'})
    p.annotate_text((0.05, 0.05), 'Box size: ' + str(width[0]) + ' ' + str(width[1]), coord_system='axis')
    #p.annotate_line_integral_convolution(("flash", "magy"), ("flash", "magz"), lim=(0.5, 0.65))
    Fig = p.export_to_mpl_figure((1,1))
    Fig.axes[0].get_images()[0].set_data(gaussian_filter(Fig.axes[0].get_images()[0].get_array(), FWHM))
    with rc_context({'mathtext.fontset': 'stix'}):
        #Fig.axes[0].text(0.05, 0.05, 'Box size: ' + str(width[0]) + ' ' + str(width[1]), c='w', horizontalalignment='left', verticalalignment='bottom', transform=Fig.axes[0].transAxes, fontsize=10)
        Fig.savefig('./' + folder + '/' + str(ds.parameter_filename).split('/')[-1] + '.jpg', dpi=300)
    #p.save('./' + folder + '/', suffix='.jpg', mpl_kwargs={'dpi':300})

def main():
    for i, DS in enumerate(DataSet):
        for k, field in enumerate(Fields):
            #for j, Frame in enumerate(range(20,30)):
            for j, Frame in enumerate(Frames):
                print('Progress: {}/{}'.format(j + len(Frames)*k + len(Fields)*i + 1,
                                               len(DataSet)*len(Fields)*len(Frames)))
                folder = 'images/'+ Titles[i] + '/' + field
                os.makedirs(folder, exist_ok=True)
                Plot(DS[Frame], TYPE, width, field, folder, 
                     linear_scale=True, spatial_scale=False, velocity_vector=False, CMAP=CMAP)
                plt.close()

if __name__ == '__main__':
    main()
