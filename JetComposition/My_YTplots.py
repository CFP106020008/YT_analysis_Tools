import yt
import numpy as np
from yt import YTQuantity
from yt.utilities.physical_constants import kb

def One_Plot(i, ts, frame, Field, fig, grid, mag=False, vel=False, CMAP='algae'):
    ds = ts[frame]
    p = yt.SlicePlot(ds, 
                     'x', 
                     Field, 
                     width=(200, 'kpc')
                     ).set_cmap(field = Field, cmap=CMAP)
    #p = yt.ProjectionPlot(ds, 
    #                      'x', 
    #                      Field, 
    #                      width=(200, 'kpc')
    #                      ).set_cmap(field = Field, cmap=CMAP)
    if mag:
        p.annotate_magnetic_field(normalize=True)

    if vel:
        p.annotate_velocity(factor = 16,normalize=True)
    
    p.set_zlim(Field, Zlim(Field)[0], Zlim(Field)[1])
    #p.set_zlim(Field, Zlim_Projection(Field)[0], Zlim_Projection(Field)[1])
    plot = p.plots[Field]        
    plot.figure = fig
    plot.axes = grid[i].axes
    plot.cax = grid.cbar_axes[i]
    p._setup_plots()

