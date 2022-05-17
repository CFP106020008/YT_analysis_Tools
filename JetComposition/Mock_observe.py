import yt
import numpy as np
from yt import YTQuantity
import os
import My_Plugin as M
import matplotlib.pyplot as plt

def detect_bubble_dimension(ds, Field='cooling_time', plot=False):
    from skimage import feature
    from skimage import filters
    width = (100, 'kpc')
    res = [500, 500]
    kpc = 3.08e21 # cm
    sli = yt.SlicePlot(ds, 'x', fields=Field)
    frb  = sli.data_source.to_frb(width, res)
    Arr = np.array(frb[Field])
    edges =  filters.roberts(Arr) 
    std = np.std(edges)
    mean = np.mean(edges)
    edges_index = np.where(edges>(mean + 3*std))
    width  = (np.max(edges_index[1])-res[1]/2)/(res[1]/2)*50*kpc # cm
    height = (np.max(edges_index[0])-res[0]/2)/(res[0]/2)*50*kpc # cm
    if plot:
        fig, ax = plt.subplots()
        ax.imshow(edges)
        ax.hlines(np.max(edges_index[0]), 0, 500)
        ax.vlines(np.max(edges_index[1]), 0, 500)
        ax.set_xlim([0,500])
        ax.set_ylim([0,500])
        fig.savefig("Edge_{:04d}.png".format(int(M.Time(ds))))
    return [width, height]

def bubble_center(ds, Field='Xray_Emissivity', plot=False):
    width = (100, 'kpc')
    res = [500, 500]
    kpc = 3.08e21 # cm
    sli = yt.SlicePlot(ds, 'x', fields=Field)
    frb  = sli.data_source.to_frb(width, res)
    Arr = 1/np.array(frb[Field])[:250,:]
    x, y = np.meshgrid(np.arange(0,res[0]), np.arange(0,int(res[1]/2)))
    xmean = np.sum(x*Arr)/np.sum(Arr)
    ymean = np.sum(y*Arr)/np.sum(Arr)
    if plot:
        fig, ax = plt.subplots()
        ax.imshow(Arr)
        ax.scatter(xmean, ymean, color='w')
        plt.show()
    dimension = [xmean/res[0]*width[0]*kpc, (res[1]/2-ymean)/res[1]*width[0]*kpc] #cm
    return dimension

def t_sync(ds):
    B = 1e-6
    nu = 1.5e8
    t_sync = 2.7e7*(B/1e-5)**(-3/2)*(nu/1e9)**(-1/2)
    return t_sync

def t_sound(ds, BubbleDef=3e9*86400*365, radius=50):
    mu = 0.61 # assuming fully ionized gas
    mp = 1.67e-24
    Myr2s = 3.1556926e13
    kpc = 3.08e21 # cm
    kb = 1.3807e-16
    gamma = 5/3 # Thermal gas should be ideal gas (?
    sp = ds.sphere(ds.domain_center, (radius, "kpc"))
    T = sp.quantities.weighted_average_quantity('temperature', 'cell_mass').v
    cs = np.sqrt(gamma*kb*T/(mu*mp)) # cm/s
    width, height = detect_bubble_dimension(ds)
    rl = height
    t_sound = 2*rl/cs
    return t_sound

def t_bouy(ds, radius=50, BubbleDef=9.47e16):
    kpc = 3.08e21 # cm
    sp = ds.sphere(ds.domain_center, (radius, "kpc"))
    CR = ds.cut_region(sp, ["obj['cooling_time'] > {}".format(BubbleDef)])
    V = CR.quantities.total_quantity("cell_volume").v/2
    width, height = detect_bubble_dimension(ds)
    Rdist = bubble_center(ds)[1] # Naive!
    #print(Rdist/kpc)
    G = 6.67e-8
    sp = ds.sphere(ds.domain_center, (Rdist, "kpc"))
    M = sp.quantities.total_quantity(["cell_mass"]).v
    g = G*M/Rdist**2
    CD = 0.75 # Churazov et al. 2001
    S = width**2*np.pi

    vb = np.sqrt(2*g*V/(S*CD))

    tbouy = Rdist/vb
    return tbouy

def t_refill(ds):
    kpc = 3.08e21 # cm
    width, height = detect_bubble_dimension(ds)
    
    # Assuming the bubble center is always 0.8 bubble height
    Rdist = bubble_center(ds)[1]
    r = height - Rdist 
    print(height/kpc, Rdist/kpc)

    G = 6.67e-8
    sp = ds.sphere(ds.domain_center, (Rdist, "kpc"))
    M = sp.quantities.total_quantity(["cell_mass"]).v
    g = G*M/Rdist**2

    trefill = 2*Rdist*np.sqrt(r/(G*M))
    return trefill
