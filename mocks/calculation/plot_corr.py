import numpy as np
import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pylab as plt

file_number = sys.argv[1]

x=np.loadtxt('xi2d/xi2d-' + str(file_number) + '.txt_L02s')
plt.figure()
#plot monople
plt.plot(x[:,0],x[:,0]**2*x[:,1],'b-')
#plot quadruple
plt.plot(x[:,0],x[:,0]**2*x[:,2],'r-')
plt.savefig('plots/corr_R_' + str(file_number) + '.png')
