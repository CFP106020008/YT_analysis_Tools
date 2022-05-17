# This file stores the color limits for each field we would use.

def Zlim(Field):
    ZLIMS = {'Heating/Cooling':[1e-1, 1e1],
             'CR_energy_density':[1e-13, 1.e-8],
             'density':[1e-28, 1e-23],
             'temperature':[1e6, 5e8],
             'crht':[1e-29, 1e-25],
             'pressure':[1.e-13, 1.e-9],
             'csht':[1e-29, 1e-25],
             'mag_strength':[1e-7, 1e-5],
             'beta_B':  [1e1, 3e5],
             'beta_CR': [1, 1e3],
             'beta_th': [1, 3],
             'cooling_time': [3.15e16, 3.17e16],
             'Sync': [1e-10, 1e-7],
             'Xray_Emissivity': [4e-24, 3e-23],
             'adiabatic_time': [-1e3, 1e3],
             'velocity_magnitude':[1e2,1e8]
            }
    return ZLIMS[Field]

def Zlim_Projection(Field):
    ZLIMS = {'Heating/Cooling':[1e-1, 1e1],
             'CR_energy_density':[1e9, 1e17],
             'density':[2e-2, 6e-2],
             'temperature':[1e7, 1e9],
             'crht':[1e-29, 1e-25],
             'pressure':[1e-11, 1e-8],
             'csht':[1e-29, 1e-25],
             'mag_strength':[1e-7, 1e-5],
             'beta_B': [1, 1e3],
             'beta_CR': [1, 1e3],
             'beta_th': [1, 1e3],
             'cooling_time': [3.15e16, 3.17e16],
             'Sync': [1e-30, 1e-10],
             'Xray_Emissivity': [2e-3, 3e-2],
             'Fake_gamma': [1e-32, 1e-22]
            }
    return ZLIMS[Field]
