import numpy as np
import matplotlib.pyplot as plt
from os import listdir
from os.path import isfile, join
from matplotlib import rc_context
#rc_context({'mathtext.fontset': 'stix'})
#Math = {'mathtext.fontset': 'stix'}

path = "/data/yhlin/ColdGasData"
files = [f for f in listdir(path) if isfile(join(path, f))]
DataSet = [np.load(join(path, i)) for i in files]
Names = ['_'.join(''.join(f.split('.')[:-1]).split('_')[1:]) for f in files]

Nrows = 1
Ncols = 1
Figs = Nrows*Ncols
msun = 1.98e33
LineStyles = ['-', '--', '-.', ':']

fig, axes = plt.subplots(nrows=Nrows, ncols=Ncols, figsize=(6.4*Nrows, 4.8*Ncols), sharey=True, sharex=True)
plt.subplots_adjust(left=0.125, bottom=0.15, right=0.9, top=0.85, wspace=0.1, hspace=0.2)

def Plot(i, j, D, Name, LS, fig=fig, ax=axes, TimeLim=[0, -1], color='r'):
    if Figs >= 4:
        axes[i,j].plot(D[TimeLim[0]:TimeLim[1],0], D[TimeLim[0]:TimeLim[1],1]/msun, linestyle=LS, color='r', label=Name)
        axes[i,j].plot(D[TimeLim[0]:TimeLim[1],0], D[TimeLim[0]:TimeLim[1],2]/msun, linestyle=LS, color='b', label=Name)
        axes[i,j].set_title("Mass of Cold Gas")
        #axes[i,j].set_ylim(y_lim)
        axes[i,j].legend()
    elif Figs == 2:
        axes[i+j].plot(D[TimeLim[0]:TimeLim[1],0], D[TimeLim[0]:TimeLim[1],1]/msun, linestyle=LS, color='r', label=Name)
        axes[i+j].plot(D[TimeLim[0]:TimeLim[1],0], D[TimeLim[0]:TimeLim[1],2]/msun, linestyle=LS, color='b', label=Name)
        axes[i+j].set_title("Mass of Cold Gas")
        #axes[i+j].set_ylim(y_lim)
        axes[i+j].legend()
    else:
        ax.plot(D[TimeLim[0]:TimeLim[1],0], D[TimeLim[0]:TimeLim[1],1]/msun, linestyle=LS, color=color, label=Name)
        ax.set_title("Mass of Cold Gas")
        #ax.set_ylim(y_lim)
        ax.legend()

TO_PLOT = ['CRp', 'CRe', 'CRpS', 'CReS']
DataSet = [DataSet[Names.index(i)] for i in TO_PLOT]
print(len(DataSet))
'''
for i, Data in enumerate(DataSet):
    if Names[i] in TO_PLOT:
        print(i)
        Plot(0, 0, Data, Names[i], LS=LineStyles[i%4], TimeLim=[0, -1])
'''
Plot(0, 0, DataSet[0], TO_PLOT[0], LS=LineStyles[0], TimeLim=[0, -1], color='r')
Plot(0, 0, DataSet[1], TO_PLOT[1], LS=LineStyles[0], TimeLim=[0, -1], color='b')
Plot(0, 0, DataSet[2], TO_PLOT[2], LS=LineStyles[1], TimeLim=[0, -1], color='r')
Plot(0, 0, DataSet[3], TO_PLOT[3], LS=LineStyles[1], TimeLim=[0, -1], color='b')
axes.set_xlim([0, 50])

fig.text(0.5, 0.08, r'$\mathrm{Time~(Myr)}$', ha='center')
fig.text(0.04, 0.5, r'$\mathrm{Cold~Gas~Mass~}(M_{\odot})$', va='center', rotation='vertical')
#plt.tight_layout()
plt.savefig('ColdGasMass_5e5.png', dpi=300)
plt.show()
