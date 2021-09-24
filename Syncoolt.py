
def t_sync(E):
    # Synchrotron time scale in https://www.mpi-hd.mpg.de/personalhomes/frieger/HEA5.pdf
    # E is in unit of eV
    m_e = 9.11e-28 # g
    c = 29979245800 # cm/s
    Myr2s = 31556926e6 # s
    gamma = E*1.6e-12/m_e/c**2
    B = 1e-6 # G
    tau = 7.8e8/B**2/gamma/Myr2s
    return tau # In Myr 

print('1 GeV', t_sync(1e9))
print('10 GeV', t_sync(1e10))
print('100 GeV', t_sync(1e11))
