import numpy as np
import yt
import matplotlib
matplotlib.use('pdf')
import matplotlib.pyplot as plt
import My_Plugin as M
from matplotlib import rc_context
from matplotlib.animation import FuncAnimation
from mpl_toolkits.axes_grid1 import AxesGrid

#Set the parameters
Fields = {  'crht':              0,
            'CR_energy_density': 0,
            'density':           1,
            'pressure':          0,
            'temperature':       0,
            'csht':              0,
            'mag_strength':      0,
            'beta_B':            0,
            'beta_CR':           0,
            'beta_th':           0,
            'cooling_time':      0
            }
CRp, CRe, CRpS, CReS = M.Load_Simulation_Datas()
CMAP = 'algae' #'dusk'
FPS = 10
#===========================#
start_frame = 1
end_frame = min(len(ts_p),len(ts_e))

rc_context({'mathtext.fontset': 'stix'})

for key in Fields:
    if Fields[key] == 1:
        if key == 'mag_strength':
            MAG = True
        else:
            MAG = False
        fig = plt.figure(figsize=(16,16))
        Field = key
        grid = AxesGrid(fig, (0.090,0.075,0.80,0.85),
                        nrows_ncols = (1, 2),
                        axes_pad = 0.5,
                        label_mode = "L",
                        share_all = True,
                        cbar_location = "right",
                        cbar_mode = "single",
                        cbar_size = "3%",
                        cbar_pad = "0%")

        def animate(i):
            print("Making Video: {}/{}".format(i+1,len(ts_p)))
            M.One_Plot(0, ts_p, i, Field=Field, fig=fig, grid=grid, mag=MAG)
            M.One_Plot(1, ts_e, i, Field=Field, fig=fig, grid=grid, mag=MAG)
            grid[0].axes.set_title("Proton / With Streaming", fontsize=20)
            grid[1].axes.set_title("Electron / With Streaming", fontsize=20)
            fig.suptitle("Time: {:03.0f} Myr".format(float(ts_p[i].current_time/31556926e6)),fontsize=24)

        animation = FuncAnimation(fig = fig, 
                                  func = animate, 
                                  frames = range(start_frame,end_frame),
                                  interval = int(1000/FPS), 
                                  save_count = 0,
                                  cache_frame_data = False
                                  )
        animation.save('Comparison_{}.mp4'.format(Field), dpi=100)
        plt.close()
    else: 
        print('IGNORE!')
