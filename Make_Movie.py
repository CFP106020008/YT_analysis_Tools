import yt
from matplotlib.animation import FuncAnimation
from matplotlib import rc_context

#Set the parameters
Folder = "./AGNCRp/crbub_hdf5_plt_cnt_*"
Field = 'density'
CMAP = 'dusk'
FPS = 24
OUT_NAME = 'AGNCRp_density_cmap=dusk_vel.mp4'

#===========================#

ts = yt.load(Folder)
plot = yt.SlicePlot(ts[0], 'x', Field, width = (100,'kpc')).set_cmap(field = Field, cmap=CMAP).annotate_velocity(factor = 16,normalize=True)
#plot.set_zlim('density', 8e-29, 3e-26)

fig = plot.plots[Field].figure

# animate must accept an integer frame number. We use the frame number
# to identify which dataset in the time series we want to load
def animate(i):
    ds = ts[i]
    print("Making Video: {}/{}".format(i+1,len(ts)))
    plot._switch_ds(ds)

animation = FuncAnimation(fig, 
                          animate, 
                          frames=len(ts),
                          interval = int(1000/FPS)
                          )

# Override matplotlib's defaults to get a nicer looking font
with rc_context({'mathtext.fontset': 'stix'}):
    animation.save(OUT_NAME)

