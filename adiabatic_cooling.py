import yt
import numpy as np
from yt.visualization.api import get_multi_plot
import matplotlib.colorbar as cb
from matplotlib.colors import LogNorm
import My_Plugin as M
import matplotlib.pyplot as plt
from matplotlib import rc_context
import matplotlib.ticker as ticker

Datas = M.Load_Simulation_Datas()
Datas_to_use = ['CRpS','CReS']
DataSet = [Datas[i] for i in Datas_to_use]
Titles = [r'$\mathrm{CRpS}$',r'$\mathrm{CReS}$']#,r'$\mathrm{CReS~0.01GeV}$']

rc_context({'mathtext.fontset': 'stix'})

width = (100, 'kpc')
res = [500, 500]

Fields_dict = { 
                'density':           0,
                'temperature':       1,
                'pressure':          1,
                'CR_energy_density': 1,
                'crht':              0,
                'csht':              0,
                'mag_strength':      0,
                'beta_th':           1,
                'beta_B':            0,
                'beta_CR':           1,
                'cooling_time':      0,
                'Sync':              0
                }
Fields = [key for key in Fields_dict if Fields_dict[key]==1]
orient = 'horizontal'
fig, axes, colorbars = get_multi_plot(len(Fields), len(DataSet), colorbar=orient, bw = 3)

cmaps = [
         'gist_heat',
         'inferno',
         'inferno', 
         'Blues',
         'Blues'
         ]

