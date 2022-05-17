import My_Plugin as M
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colorbar as cb
import matplotlib
import yt
matplotlib.use('pdf')
from matplotlib import rc_context
from matplotlib.colors import LogNorm, Normalize

def One_Axis(i, j, ds, 
             Field, 
             fig,
             ax,
             plots, 
             colorbars, 
             Titles,
             width=(100, 'kpc'), 
             res=500, 
             PlotType='slice',
             ScaleType='standard',
             theta = 90, # degree
             phi = 0, # degree
             CMAP = 'inferno'
             ):
    
    theta *= np.pi/180
    phi *= np.pi/180
    normal = (np.sin(theta)*np.cos(phi), np.sin(theta)*np.sin(phi), np.cos(theta))

    if PlotType == 'slice':
        Plot = yt.SlicePlot(ds, 'x', fields=Field)
    elif PlotType == 'proj':
        Plot = yt.ProjectionPlot(ds, 'z', fields=Field)
    elif PlotType == 'offaxisproj':
        Plot = yt.OffAxisProjectionPlot(ds, normal, fields=Field, width=width)
        #Plot.annotate_scale()
    else:
        raise NameError('wrong PlotType')

    Fig = Plot.export_to_mpl_figure((1,1))
    
    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)
    Arr = Fig.axes[0].get_images()[0].get_array()
    #Max = np.max(Arr)
    #Min = np.max(Arr)
    if PlotType == 'slice':
        #Arr[Arr <= Min] = Min
        Arr[Arr <= M.Zlim(Field)[0]] = M.Zlim(Field)[0]
    else:
        #Arr[Arr <= Min] = Min
        Arr[Arr <= M.Zlim_Projection(Field)[0]] = M.Zlim_Projection(Field)[0]
        
    if ScaleType == 'log':
        plots.append(ax.imshow(Arr, norm=LogNorm()))
    elif ScaleType == 'standard':
        plots.append(ax.imshow(Arr, norm=LogNorm(M.Zlim_Projection(Field)[0], 
                                                   M.Zlim_Projection(Field)[1])))
    elif ScaleType == 'linear':
        plots.append(ax.imshow(Arr, norm=Normalize(np.max(Arr)/50,
                                                     np.max(Arr))))
    '''
    if Type == 'slice':
        plots[-1].set_clim((M.Zlim(Field)[0], M.Zlim(Field)[1]))
    else:
        plots[-1].set_clim((M.Zlim_Projection(Field)[0], M.Zlim_Projection(Field)[1]))
    '''
    plots[-1].set_cmap(CMAP)
    if j == 0:
        ax.text(0.05, 0.95, 
                  Titles[i], c='w', 
                  horizontalalignment='left', 
                  verticalalignment='top', 
                  transform=ax.transAxes, 
                  fontsize=15)
    ax.text(0.95, 0.95, 
              r'{:.0f} Myr'.format(M.Time(ds)), c='w', 
              horizontalalignment='right', 
              verticalalignment='top', 
              transform=ax.transAxes, 
              fontsize=15)
    return ax
