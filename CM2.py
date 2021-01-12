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
Fields = {  'crht': 0,
            'CR_energy_density': 0,
            'density': 0,
            'pressure': 0,
            'temperature': 0,
            'csht': 1}
CMAP = 'algae' #'dusk'
FPS = 10
#===========================#

ts_p = yt.load(Folder_p) #Proton Jet dataset
ts_e = yt.load(Folder_e) #Electron Jet dataset

start_frame = 1
end_frame = 10 #min(len(ts_p),len(ts_e))

fns = [ts_p, ts_e] # Total set of datas

rc_context({'mathtext.fontset': 'stix'})

def One_Plot(i, ts, frame):
    p = yt.SlicePlot(ts[frame], 
                     'x', 
                     Field, 
                     width=(200, 'kpc')
                     ).set_cmap(field = Field, cmap=CMAP
                     )#.annotate_velocity(factor = 16,normalize=True)

    p.set_zlim(Field, M.Zlim(Field)[0], M.Zlim(Field)[1])
    plot = p.plots[Field]        
    plot.figure = fig
    plot.axes = grid[i].axes
    plot.cax = grid.cbar_axes[i]
    p._setup_plots()

for key in Fields:
    if Fields[key] == 1:
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

        # Proton Jet        
        One_Plot(0, ts_p, start_frame)
        # Electron Jet
        One_Plot(1, ts_e, start_frame)


        def animate(i):
            print("Making Video: {}/{}".format(i+1,len(ts_p)))
            One_Plot(0, ts_p, i)
            One_Plot(1, ts_e, i)
            #pp._switch_ds(ts_p[i])
            #pe._switch_ds(ts_e[i])
            grid[0].axes.set_title("Proton / With Streaming", fontsize=20)
            grid[1].axes.set_title("Electron / With Streaming", fontsize=20)
            fig.suptitle("Time: {:03.0f} Myr".format(float(ts_p[i].current_time/31556926e6)),fontsize=24)

        animation = FuncAnimation(fig = fig, 
                                  func = animate, 
                                  frames = range(start_frame,end_frame),
                                  interval = int(1000/FPS), 
                                  save_count = 0
                                  )
        animation.save('Comparison_{}.mp4'.format(Field), dpi=300)
        plt.close()
    else: 
        print('IGNORE!')
