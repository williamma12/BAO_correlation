import numpy as np
import scipy.integrate as integrate
import sys

path = '/global/homes/w/wma/correlation/'
suffix = '.v11.1.release.txt'
try:
    file = sys.argv[1]
    if file == 'data_north':
        prefix = 'cmass_dr11_north_ir'
        path += 'data_north/'
    elif file == 'data_south':
        prefix = 'cmass_dr11_south_ir'
        path += 'data_south/'
    elif file == 'random_north':
        prefix = 'cmass_dr11_north_randoms_ir'
        path += 'random_north/'
    elif file == 'random_south':
        prefix = 'cmass_dr11_south_randoms_ir'
        path += 'random_south/'
except:
    print("**********************************")
    print("Run as 'python Spherical-to-Cartesian {data_north, data_south, random_north, random_south}'")
    print("**********************************")

# Cosmological parameters
OmegaM = 0.274
OmegaL = 0.726
OmegaK = 1 - OmegaM - OmegaL
hubble = 3000./0.7
w = -1.0

# Calculate comoving distance functions
dc = lambda z : hubble/np.sqrt(OmegaM*(1.+z)**3+OmegaK*(1.+z)**2+OmegaL*(1.+z)**(-3.*(1.+w)))

for i in range(4001, 4006):
    result = []
    fname = prefix + str(i) + suffix
    pwd = path + fname
    print(pwd)
    arr = np.loadtxt(pwd, dtype={'names': ('ra', 'dec', 'red', 'weight_boss', 'weight_cp', 'weight_red', 'veto'), 
        'formats': ('double', 'double', 'double', 'int', 'int', 'int', 'double')}, usecols=(0, 1, 2, 4, 5, 6, 7))

    np.where(arr['veto']!=1, arr['weight_boss'], 0)

    for j in range(0, len(arr)):
        w = 1
        p = integrate.quad(dc, 0, arr[j][2])
        phi=np.deg2rad(arr[j][0])
        theta=np.deg2rad(90-arr[j][1])
        x = p[0] * np.cos(phi) * np.cos(theta)
        y = p[0] * np.sin(phi) * np.cos(theta)
        z = p[0] * np.cos(theta)
        result.append((x,y,z,w))
        
    np.savetxt(path + str(i) + "_" + str(file) + ".xyzw", result, delimiter='\t')
