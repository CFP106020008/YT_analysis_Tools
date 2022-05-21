# This code is created by Lin Yen-Hsing (NTHU, 2022) on CICA cluster
import numpy as np
import os

import yt
import matplotlib
import matplotlib.colorbar as cb
import matplotlib.pyplot as plt
from matplotlib import rc_context

from My_Plugins.Zlims import Zlim, Zlim_Projection
from My_Plugins.LoadData import Load_Simulation_Datas
import My_Plugins.Fields as M

# Setup the parameters
# ======================================== #
width = (500, 'kpc') # Visualization box size

#TYPE = 'proj'
TYPE = 'slice'
#TYPE = 'offaxis'

# Orientation of the camera
# Only important when using offaxis plot
theta = 20*np.pi/180 #deg
phi = 0*np.pi/180 # deg

# The simulations
Datas_to_use = [#'CRpS', 
                #'ORC_M13_P1_D1', 
                #'ORC_M13_P1_D5',
                'ORC_M12_P1_D10',
                #'ORC_M12_P1_D5',
                #'ORC_M12_P1_D1',
                #'ORC_M12_P1_D5_200'
                #'ORC_M12_P0_D5',
                #'ORC_M12_P0_D10'
                ]
# The fields
Fields_dict = { 
                'density':           1,
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
                'Fake_gamma':        0
                }

# ======================================== #

# Load the simulation data into a list
Datas = Load_Simulation_Datas()
DataSet = [Datas[i] for i in Datas_to_use]
Titles = Datas_to_use

# Make the list of all the fields 
Fields = [key for key in Fields_dict if Fields_dict[key]==1]

rc_context({'mathtext.fontset': 'stix'}) # To make pretty fonts
x = np.sin(theta)*np.cos(phi)
y = np.sin(theta)*np.sin(phi)
z = np.cos(theta)
normal = np.array([x,y,z]) # Calculate normal vector for off axis plot

matplotlib.use('pdf') # Avoid pop-up windows

# ======================================== #

def Plot(ds, TYPE, width, field, folder, 
         normal=[0,0,1], linear_scale=False, velocity_vector=False, CMAP='inferno'):
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
    p.set_cmap(field, CMAP)
    p.save('./' + folder + '/', suffix='.jpg', mpl_kwargs={'dpi':300})

def main():
    for i, DS in enumerate(DataSet):
        for j, Frame in enumerate(range(len(DS))):
            for k, field in enumerate(Fields):
                folder = 'images/'+field
                os.makedirs(folder, exist_ok=True)
                Plot(DS[j], TYPE, width, field, folder)

if __name__ == '__main__':
    main()
