import yt 
import os
import matplotlib.pyplot as plt
from matplotlib import rc_context
from astropy.cosmology import FlatLambdaCDM
from scipy.optimize import bisect

source_path = './'
image_path = './dens/'

#Field = ('PartType0','InternalEnergy')
Field = ('gas','density')
#Field = ('gas','velocity_magnitude')

#Cmap = 'gist_heat'
Cmap = 'cividis'

Zlim = [5e-4, 3e-3] # For density
#Zlim = [1e33, 5e33] # For internal energy?

# Get the files
fnames = [f for f in os.listdir(source_path) if f.endswith(".hdf5")]
fnames.sort()

# Define cosmology
cosmo = FlatLambdaCDM(H0=67.8, Om0=0.308)
t_i = cosmo.lookback_time(1e9).value
def a_to_t(a):
    z = 1/a - 1
    return cosmo.age(z).value

# Enable parallelization
yt.enable_parallelism()

# Load data
unit_base = {'UnitLength_in_cm'         : 3.08568e+24,
             'UnitMass_in_g'            :   1.989e+43,
             'UnitVelocity_in_cm_per_s' :      100000,
             'UnitEnergy_in_erg'        :           1,
             'UnitInternalenergy_in_erg/g':         1
             }
bbox_lim = 50 #Mpc
bbox = [[0,bbox_lim],
        [0,bbox_lim],
        [0,bbox_lim]]
DS = yt.load(source_path+"*.hdf5", unit_base=unit_base, bounding_box=bbox)

def Gas_Plot(ds, Field, Cmap='cividis'):
    p = yt.ProjectionPlot(ds, 'x', Field)
    #p = yt.SlicePlot(ds, 'x', Field)
    p.set_cmap(Field, Cmap)
    #p.set_zlim(Field, Zlim[0], Zlim[1])
    fig = p.export_to_mpl_figure((1,1))
    ax = fig.axes[0]
    ax.text(0.05, 0.95, 
            '$\mathrm{Cosmic~Age:~}' + '{:4.1f}$'.format(a_to_t(ds.current_time.v)) + '$\mathrm{~billion~years}$', 
            size = 20,
            color = 'w',
            horizontalalignment='left',
            verticalalignment='top', 
            transform=ax.transAxes)
    plt.tight_layout()
    fig.savefig(image_path+"{}.jpg".format(ds.parameter_filename.split(".")[0].split('/')[-1]))

# This is main
def main():
    if not(os.path.isdir(source_path)):
        print("No source files! Wrong path!")
    if not(os.path.isdir(image_path)):
        os.system('mkdir ' + image_path)

    for i, ds in enumerate(DS.piter()):
        with rc_context({"mathtext.fontset":"stix"}):
            Gas_Plot(ds, Field, Cmap=Cmap)
            #DM.Plot(source_path+fnames[i])
if __name__ == '__main__':
    main()

