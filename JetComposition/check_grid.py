import yt
import numpy as np
from yt.visualization.api import get_multi_plot
import matplotlib.colorbar as cb
from matplotlib.colors import LogNorm, Normalize
import My_Plugin as M
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('pdf')
from matplotlib import rc_context

#yt.enable_parallelism()

Datas = M.Load_Simulation_Datas()
Datas_to_use = ['CRpS', 'CRpS_ORCHM', 'CRpS_ORCHMDP', 'CRpS_ORCHMLJ']
#Datas_to_use = ['CRpS_ORCHMNJ', 'CRpS_ORCHMNJNC']
#Datas_to_use = ['CRp', 'CRpS']
#Datas_to_use = ['CRe', 'CReS']
DataSet = [Datas[i] for i in Datas_to_use]
Titles = Datas_to_use

ds = DataSet[0][27]

#field = ('gas', 'density')
field = ('gas', 'temperature')
#field = ('gas', 'beta_B')
#field = ('gas', 'eth')
#field = ('gas', 'Fake_gamma')
#field = ('gas', 'velocity_magnitude')

p = yt.SlicePlot(ds, 'x', field, width=(500, 'kpc'))
#p = yt.ProjectionPlot(ds, 'z', field, width=(200, 'kpc'))

Fig = p.export_to_mpl_figure((1,1))
Arr = Fig.axes[0].get_images()[0].get_array()
Max = np.max(Arr)
Min = np.max(Arr)/50

#p.set_log(field, False)
p.set_zlim(field, 3e6, 3e8)
#p.set_zlim(field, Min, Max)
p.set_cmap(field, 'gist_heat')
p.annotate_grids(linewidth=0.5, alpha=0.5, edgecolors='black')
#p.annotate_cell_edges(line_width=0.0005, alpha=0.5, color='black')
#p.annotate_magnetic_field(factor=10,normalize=True)
p.save()






