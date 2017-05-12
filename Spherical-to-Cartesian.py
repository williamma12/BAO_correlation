import pandas as pd
import numpy as np
import scipy.integrate as integrate
import sys

path = '/global/homes/w/wma/correlation/'
suffix = '.v11.1.release.txt'
start = int(sys.argv[2]) + 4000
end = int(sys.argv[3]) + 4001

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
OmegaM = 0.24
OmegaL = 0.7
OmegaK = 1 - OmegaM - OmegaL
hubble = 3000./0.7
w = 1.0
alpha = np.deg2rad(-55.)

# Calculate comoving distance functions
dc = lambda z : hubble/np.sqrt(OmegaM*(1.+z)**3+OmegaK*(1.+z)**2+OmegaL*(1.+z)**(-3.*(1.+w)))

for i in range(start, end):
    result = []
    fname = prefix + str(i) + suffix
    pwd = path + fname
    print(pwd)
    df = pd.read_csv(pwd, comment='#', engine='python', delimiter=' ', usecols=[0, 1, 2, 7], names=['ra', 'dec', 'red', 'veto'])
    df = df[df.veto == 1]

    for index, row in df.iterrows():
        p = integrate.quad(dc, 0, row['red'])
        phi=np.deg2rad(row['ra'])
        theta=np.deg2rad(row['dec'])
        x = p[0] * np.cos(phi) * np.cos(theta)
        y = p[0] * np.sin(phi) * np.cos(theta)
        z = p[0] * np.sin(theta)
        result.append((x,y,z,w))
        rot_x = x * np.cos(alpha) + z * np.sin(alpha)
        rot_y = y
        rot_z = -x * np.sin(alpha) + z * np.cos(alpha)
        #result.append((rot_x, rot_y, rot_z, w))
        
    np.savetxt(path + str(i) + "_" + str(file) + ".xyzw", result, delimiter='\t')
