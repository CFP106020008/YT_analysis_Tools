# This file stores the color limits for each field we would use.

def Zlim(Field):
    ZLIMS = {'Heating/Cooling':[1e-1, 1e1],
             'CR_energy_density':[1e-15, 1.e-9],
             #'CR_energy_density':[1e-13, 1.e-8],
             #'CR_energy_density':[1e-10, 1.e-8],
             #'density':[1e-28, 1e-23],
             'density':[1e-29, 1e-23],
             #'temperature':[1e6, 5e8],
             'temperature':[5e5, 5e8],
             'crht':[1e-29, 1e-25],
             'pressure':[1.e-13, 1.e-9],
             'csht':[1e-29, 1e-25],
             #'mag_strength':[1e-7, 1e-5],
             'mag_strength':[1e-8, 1e-6],
             'beta_B':  [1e1, 3e5],
             'beta_CR': [1, 10],
             'beta_th': [1, 3],
             'cooling_time': [3.15e16, 3.17e16],
             'Sync': [1e-10, 1e-7],
             'Xray_Emissivity': [4e-24, 3e-23],
             'adiabatic_time': [-1e3, 1e3],
             'velocity_magnitude':[1e2,1e8],
             'Fake_gamma_electron': [1e-23, 2e-21],
             'Fake_gamma': [1e-63, 2e-39],
             'Heating_Cooling_Ratio': [1e-2, 1e2],
             'j_nu_Sync': [1e0, 1e1]
            }
    return ZLIMS[Field]

def Zlim_Projection(Field):
    ZLIMS = {'Heating/Cooling':[1e-1, 1e1],
             'CR_energy_density':[1e0, 1e15],
             'density':[1e-5, 1e-1],
             #'density':[1e-3, 1e-1],
             'temperature':[1e7, 1e9],
             'crht':[1e-12, 1e-7],
             'pressure':[1e-11, 1e-8],
             'csht':[1e-29, 1e-25],
             'mag_strength':[1e-5, 1e-3],
             'beta_B': [1, 1e3],
             'beta_CR': [1, 1e3],
             'beta_th': [1, 1e3],
             'cooling_time': [3.15e16, 3.17e16],
             'Sync': [1e-30, 1e-10],
             'Xray_Emissivity': [2e-5, 5e-1],
             #'Fake_gamma': [1e-32, 1e-22],
             #'Fake_gamma': [1e-23, 2.95e-22], # CRpS_M13_P5_D5
             'Fake_gamma': [1e-26, 8.9e-26], # CRpS_M12_P5_D5
             'Fake_gamma_electron': [1e4, 1e5],
             'j_nu_Sync': [1e0, 1e1]
            }
    return ZLIMS[Field]
