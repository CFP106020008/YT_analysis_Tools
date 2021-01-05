import numpy as np
import yt
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib import rc_context
from mpl_toolkits.axes_grid1 import AxesGrid
import My_Plugin as M

#Set the parameters
Folder = "./CRp_Streaming/crbub_hdf5_plt_cnt_*"
Fields = {  'crht': 0,
            'CR_energy_density': 0,
            'density': 1,
            'pressure': 0,
            'temperature': 0}
CMAP = 'algae' #'dusk'
FPS = 10
#===========================#

Ds = yt.load(Folder) #Proton Jet datasets

start_frame = 1
end_frame = min(len(ts_p),len(ts_e))

rc_context({'mathtext.fontset': 'stix'})

for key in Fields:
    if Fields[key] == 1:
        p = yt.SlicePlot(ts_p[start_frame], 
                         'x', 
                         Field, 
                         width=(200, 'kpc')
                         ).set_cmap(field = Field, cmap=CMAP
                         ).annotate_velocity(factor = 16,normalize=True)

        p.set_zlim(Field, M.Zlim(Field)[0], M.Zlim(Field)[1])
        fig, ax = p.plots['density']

        def animate(i):
            print("Making Video: {}/{}".format(i+1,len(ts_p)))
            ds = Ds[i]
            p._switch_ds(ds)
            fig.suptitle("Time: {:03.0f} Myr".format(float(ts_p[i].current_time/31556926e6)),fontsize=24)

        animation = FuncAnimation(fig = fig, 
                                  func = animate, 
                                  frames = range(start_frame,end_frame),
                                  interval = int(1000/FPS), 
                                  save_count = 0
                                  )
        animation.save('{}_{}.mp4'.format(Folder.split(separator='/')[1], Field), dpi=300)
        plt.close()
    else: 
        print('IGNORE!')
