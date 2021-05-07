import numpy as np
import yt
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib import rc_context
from mpl_toolkits.axes_grid1 import AxesGrid
import My_Plugin as M

#Set the parameters

ds = 
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
