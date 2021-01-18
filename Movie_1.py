import numpy as np
import yt
import os
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib import rc_context
from mpl_toolkits.axes_grid1 import AxesGrid
import My_Plugin as M

#Set the parameters
Folder = "./CRp_Streaming/crbub_hdf5_plt_cnt_*"
Fields = {  'crht': 0,
            'csht': 1,
            'CR_energy_density': 0,
            'density': 0,
            'pressure': 0,
            'temperature': 0}
CMAP = 'algae' #'dusk'
FPS = 10
L = 100 #kpc
#===========================#

Ds = yt.load(Folder) #Proton Jet datasets

start_frame = 2
end_frame = len(Ds)

rc_context({'mathtext.fontset': 'stix'})

for key in Fields:
    if Fields[key] == 1:
        Field = key
        fig = plt.figure(figsize=(16,16))
        grid = AxesGrid(fig, (0.090,0.075,0.80,0.85),
                        nrows_ncols = (1, 1),
                        axes_pad = 0.5,
                        label_mode = "L",
                        share_all = True,
                        cbar_location = "right",
                        cbar_mode = "single",
                        cbar_size = "3%",
                        cbar_pad = "0%")
        
        def animate(i):
            print("Making Video: {}/{}".format(i+1,len(Ds)))
            M.One_Plot(0, Ds, i, Field=Field, fig=fig, grid=grid)
            
            fig.suptitle("Time: {:03.0f} Myr".format(float(ds.current_time/31556926e6)),fontsize=24)

        animation = FuncAnimation(fig = fig, 
                                  func = animate, 
                                  frames = range(start_frame,end_frame),
                                  interval = int(1000/FPS), 
                                  save_count = 0
                                  )
        animation.save('{}_{}.mp4'.format(os.path.dirname(Folder), Field), dpi=300)
        plt.close()
    else: 
        print('IGNORE!')
