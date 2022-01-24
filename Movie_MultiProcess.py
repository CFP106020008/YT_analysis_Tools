import numpy as np
import yt
import matplotlib
matplotlib.use('pdf')
import matplotlib.pyplot as plt
import My_Plugin as M
from matplotlib import rc_context
#from matplotlib.animation import FuncAnimation
from mpl_toolkits.axes_grid1 import AxesGrid
import multiprocessing as mp
import multiprocessing.managers as mpman
import time
import os

#Set the parameters
Fields = {  'crht':              0,
            'CR_energy_density': 1,
            'density':           1,
            'pressure':          1,
            'temperature':       1,
            'csht':              0,
            'mag_strength':      0,
            'beta_B':            0,
            'beta_CR':           0,
            'beta_th':           0,
            'cooling_time':      0,
            'Sync':              0
            }
CMAP = 'algae' #'dusk'
FPS = 10
#===========================#

Datas = M.Load_Simulation_Datas()
Datas_to_use = ['CRp', 'CRpS', 'CRe', 'CReS']
#Datas_to_use = ['CRe_3E21E0', 'CRe_3E11E0', 'CRe_1E23E0', 'CRe_1E23E-1']
DataSet = [Datas[i] for i in Datas_to_use]
#Titles = ['CRe_1E21E0', 'CRe_3E21E0', 'CRe_1E21E0', 'CRe_1E21E0']

Start_Time = time.time()
start_frame = 0
end_frame = min(map(len, DataSet))
n_thread = 10

rc_context({'mathtext.fontset': 'stix'})

def Frame_In_Range(Start, End, Ds1, Ds2, Ds3, Ds4, Field, MAG):
    for i in range(Start, End):
        print("Making Video: {}/{}".format(i+1,end_frame))
        fig = plt.figure(figsize=(16,16))
        Field = key
        grid = AxesGrid(fig, (0.05,0.075,0.90,0.8),
                        nrows_ncols = (2, 2),
                        axes_pad = 0.5,
                        label_mode = "L",
                        share_all = True,
                        cbar_location = "right",
                        cbar_mode = "single",
                        cbar_size = "3%",
                        cbar_pad  = "3%")
        
        M.One_Plot(0, Ds1, i, Field=Field, fig=fig, grid=grid, mag=MAG, Type='Slice')
        M.One_Plot(1, Ds2, i, Field=Field, fig=fig, grid=grid, mag=MAG, Type='Slice')
        M.One_Plot(2, Ds3, i, Field=Field, fig=fig, grid=grid, mag=MAG, Type='Slice')
        M.One_Plot(3, Ds4, i, Field=Field, fig=fig, grid=grid, mag=MAG, Type='Slice')
        grid[0].axes.set_title(Datas_to_use[0], fontsize=20)
        grid[1].axes.set_title(Datas_to_use[1], fontsize=20)
        grid[2].axes.set_title(Datas_to_use[2], fontsize=20)
        grid[3].axes.set_title(Datas_to_use[3], fontsize=20)
        #fig.text(0.5, 0.95, "$Time: {:03.0f} Myr$".format(M.Time(Ds1[i])), ha='center', va='top', fontsize=20)
        fig.text(0.5, 0.95, "$\mathrm{Time: }%3d \mathrm{ Myr}$" % M.Time(Ds1[i]), ha='center', va='top', fontsize=20)
        fig.savefig('./{}/{}_Frame={:03d}.png'.format(Field, Field, i))
        plt.close()

Lost = end_frame%n_thread
def Draw(Field, Ds1, Ds2, Ds3, Ds4, MAG):
    Pro_List = []
    for i in range(n_thread):
        Pro_List.append(mp.Process(target=Frame_In_Range, args=(int(end_frame/n_thread)*i, int(end_frame/n_thread)*(i+1), Ds1, Ds2, Ds3, Ds4, Field, MAG)))
    Pro_List.append(mp.Process(target=Frame_In_Range, args=(int(end_frame/n_thread)*(i+1), int(end_frame/n_thread)*(i+1) + Lost, Ds1, Ds2, Ds3, Ds4, Field, MAG)))
    for p in Pro_List:
        p.start()
    for p in Pro_List:
        p.join() 
    
for key in Fields:
    if Fields[key] == 1:
        os.system("mkdir {}".format(key))
        if key == 'mag_strength':
            MAG = True
        else:
            MAG = False
        Draw(key, DataSet[0], DataSet[1], DataSet[2], DataSet[3], MAG)
        #os.system("ffmpeg -r 10 -pattern_type glob -i '*.png' -vcodec libx264 -s 1024x1024 -pix_fmt yuv420p movie_{}.mp4".format(key))
        #os.system("rm ./{}/*.png".format(key))
    else: 
        print('IGNORE!')

End_Time = time.time()
print('The code takes {} s to finish'.format(End_Time-Start_Time))
