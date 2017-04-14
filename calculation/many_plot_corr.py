import numpy as np
import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pylab as plt

first = int(sys.argv[1])
last = int(sys.argv[2])
len = last - first + 1
coor = np.zeros((len, 3, 50))
plt.figure()

for i in range(len):
    file_number = i+1
    if file_number != 2 and file_number != 25:
        file = np.nan_to_num(np.loadtxt('xi2d/xi2d-' + str(file_number) + '.txt_L02s',
                            dtype={'names':('x','mono','quad'), 'formats':('float32', 'float32', 'float32')}))

        for j in range(50):
            x = file['x'][j]
            mono = file['x'][j]**2*file['mono'][j]
            quad = file['x'][j]**2*file['quad'][j]
            if mono < 1000 and quad > -1000:
                coor[i][0][j] = x
                coor[i][1][j] = mono
                coor[i][2][j] = quad
        
            #plt.plot(coor[i][0], coor[i][1], 'b-')
            #plt.plot(coor[i][0], coor[i][2], 'g-')

mean = np.nanmean(coor, axis=0)
plt.plot(mean[0], mean[1], 'b-', linewidth=2)
plt.plot(mean[0], mean[2], 'g-', linewidth=2)

plt.savefig('corr_' + str(first) + '-' + str(last) + '.png')
np.savetxt('avg_corr_fun', np.transpose(mean))
