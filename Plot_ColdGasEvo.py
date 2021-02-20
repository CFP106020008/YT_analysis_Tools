import numpy as np
import matplotlib.pyplot as plt

D1 = np.load('ColdGasMass_Streaming.npy')
D2 = np.load('ColdGasMass_No_Streaming.npy')
#print(D)
Nrows = 1
Ncols = 1
Figs = Nrows*Ncols
msun = 1.98e33

fig, axes = plt.subplots(nrows=Nrows, ncols=Ncols, figsize=(6*Nrows, 6*Ncols), sharey=True, sharex=True)
plt.subplots_adjust(left=0.125, bottom=0.15, right=0.9, top=0.85, wspace=0.1, hspace=0.2)

def Plot(i, j, D, Name1, Name2, LS, fig=fig, ax=axes, TimeLim=[0, -1]):
    if Figs >= 4:
        axes[i,j].plot(D[TimeLim[0]:TimeLim[1],0], D[TimeLim[0]:TimeLim[1],1]/msun, linestyle=LS, color='r', label=Name1)
        axes[i,j].plot(D[TimeLim[0]:TimeLim[1],0], D[TimeLim[0]:TimeLim[1],2]/msun, linestyle=LS, color='b', label=Name2)
        axes[i,j].set_title("Mass of Cold Gas")
        #axes[i,j].set_ylim(y_lim)
        axes[i,j].legend()
    elif Figs == 2:
        axes[i+j].plot(D[TimeLim[0]:TimeLim[1],0], D[TimeLim[0]:TimeLim[1],1]/msun, linestyle=LS, color='r', label=Name1)
        axes[i+j].plot(D[TimeLim[0]:TimeLim[1],0], D[TimeLim[0]:TimeLim[1],2]/msun, linestyle=LS, color='b', label=Name2)
        axes[i+j].set_title("Mass of Cold Gas")
        #axes[i+j].set_ylim(y_lim)
        axes[i+j].legend()
    else:
        ax.plot(D[TimeLim[0]:TimeLim[1],0], D[TimeLim[0]:TimeLim[1],1]/msun, linestyle=LS, color='r', label=Name1)
        ax.plot(D[TimeLim[0]:TimeLim[1],0], D[TimeLim[0]:TimeLim[1],2]/msun, linestyle=LS, color='b', label=Name2)
        ax.set_title("Mass of Cold Gas")
        #ax.set_ylim(y_lim)
        ax.legend()

Plot(0, 0, D1, 'CRpS', 'CReS', LS='--', TimeLim=[0,15])
Plot(0, 1, D2, 'CRp', 'CRe', LS='-',TimeLim=[0,15])
fig.text(0.5, 0.08, r'Time (Myr)', ha='center')
fig.text(0.04, 0.5, r'Cold Gas Mass ($M_{\odot}$)', va='center', rotation='vertical')
plt.savefig('ColdGasMass_5e5.png', dpi=300)
plt.show()
