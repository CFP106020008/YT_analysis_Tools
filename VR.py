import numpy as np
import yt
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib import rc_context
from mpl_toolkits.axes_grid1 import AxesGrid
import My_Plugin as M

#Set the parameters
Folder_p = "./CRp_Streaming/crbub_hdf5_plt_cnt_*"
Folder_e = "./CRe_Streaming/crbub_hdf5_plt_cnt_*"
#Field = 'Heating/Cooling'
Field = 'CR_energy_density'
#Field = 'density'
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
cam.width = 100*yt.units.kpc
cam.yaw(np.pi/2, rot_center=ds.domain_center)
#cam.focus = ds.domain_center
#cam.switch_orientation()


source = sc[0]
source.tfh.set_bounds((M.Zlim(Field)[0],M.Zlim(Field)[1]))
source.tfh.set_log(True)
source.tfh.grey_opacity = False

#render_source.transfer_function = tfh.tf

source.tfh.plot('./VR/transfer_function.png', profile_field='density')

sc.save('./VR/rendering.png', sigma_clip=4.0)
