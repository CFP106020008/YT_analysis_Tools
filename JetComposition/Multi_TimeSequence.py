import yt
import numpy as np
from yt.visualization.api import get_multi_plot
import matplotlib.colorbar as cb
import My_Plugin as M
import My_Plots as MP
import matplotlib.pyplot as plt
import matplotlib
import os
import glob
matplotlib.use('pdf')
from matplotlib import rc_context
from matplotlib.colors import LogNorm, Normalize

yt.enable_parallelism()

Datas = M.Load_Simulation_Datas()
Datas_to_use = ['CRpS', 'CRpS_ORCLM']
DataSet = [Datas[i] for i in Datas_to_use]
Titles = Datas_to_use
DIRs = ['/data/yhlin/CRpS_ORCLM/',
        '/data/yhlin/Final_Sims/CRp_Streaming/']


width = (200, 'kpc')
res = [500, 500]
#TYPE = 'proj'
TYPE = 'offaxisproj'
#TYPE = 'slice'
Frames = [3,6,9,12]

Fields_dict = { 
                'density':           0,
                'temperature':       0,
                'pressure':          0,
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
                'Fake_gamma':        1
                }
Fields = [key for key in Fields_dict if Fields_dict[key]==1]
orient = 'vertical'
rc_context({'mathtext.fontset': 'stix'})

fig, axes, colorbars = get_multi_plot(len(Frames), len(DataSet), colorbar=orient, bw = 3)


def main():
    plots = []
    for Field in Fields:
        #for i, DS in enumerate(DataSet):
        for i, path in enumerate(DIRs):
            filename = glob.glob(os.path.join(path, 'crbub_hdf5_plt_cnt_*'))
            files = [filename[frame] for frame in Frames]
            TS = yt.DatasetSeries(files)
            for j, ds in enumerate(TS.piter()):
                print(i, j)
                print(len(TS))
                MP.One_Axis(i, j, ds, Field, fig, axes[i][j], 
                            plots=plots,
                            colorbars=colorbars,
                            PlotType=TYPE,
                            Titles=Titles,
                            theta=0,
                            phi=0)

        titles = [  
                    '{}'.format(Field), 
                    '{}'.format(Field) 
                    ]

        for p, cax, t in zip(plots, colorbars, titles):
            cbar = fig.colorbar(p, cax=cax, orientation=orient)
            cbar.set_label(t)
        fig.savefig("Time_Sequence_{}_{}.png".format(Field, TYPE))

if __name__ == "__main__":
    main()
