import numpy as np
import matplotlib.pyplot as plt

# This code use CGS!

sigma_T = 6.65e-25 # cm^2
m_e = 9.11e-28 # g
c = 29979245800. # cm/s
Myr = 3.16e13 # s/yr
GeV = 0.00160217662 # erg/GeV
B = 1 # micro gauss, simple assumption
gamma = 2.5 # cp/cv
z = 0 # redshift?

# From the OOO_unsplitUpdate.F90 
Urad = 4.2e-13*(1.+z)**4.
Ub = 4.e-14*B**2.
Utot = Urad + Ub

# From Yang & Ruszkowski (2018)
beta = 4/3*sigma_T/(m_e**2*c**3)*Utot

V10 = 4.24e68 # cm^3
T = Myr*10

def EEVO_Expansion(E0, t):
    

    return

def EEVO_Sync(E0, t)
    return E0 / (1 + beta*t*E0)







