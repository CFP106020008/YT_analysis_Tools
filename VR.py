import numpy as np
import yt
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib import rc_context
from mpl_toolkits.axes_grid1 import AxesGrid
import My_Plugin as M

#Set the parameters
Folder_p = "./AGNCRp/crbub_hdf5_plt_cnt_*"
Folder_e = "./AGNCRe/crbub_hdf5_plt_cnt_*"
#Field = 'Heating/Cooling'
#Field = 'CR_energy_density'
Field = 'density'
#Field = 'pressure'
#Field = 'temperature'
CMAP = 'algae' #'dusk'
Frames = [1,10,20,30,40,50]
#===========================#

ts_p = yt.load(Folder_p) #Proton Jet dataset
ts_e = yt.load(Folder_e) #Electron Jet dataset

fns = [ts_p, ts_e] # Total set of datas

ds = ts_p[-1]
sc = yt.create_scene(ds, Field)

cam = sc.camera
cam.pitch(np.pi/4.0)
cam.width = 100*yt.units.kpc
cam.focus = ds.domain_center

sc.save("VR.png")



