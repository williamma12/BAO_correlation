import numpy as np
import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pylab as plt
import mpmath

first = int(sys.argv[1])
last = int(sys.argv[2])
len = last - first + 1
coor = np.zeros((len, 3, 50))
plt.figure()

for i in range(len):
    file = np.nan_to_num(np.loadtxt('xi2d/xi2d-' + str(i+1) + '.txt_L02s',
                        dtype={'names':('x','mono','quad'), 'formats':('float32', 'float32', 'float32')}))

    for j in range(50):
        mpmath.mp.dps = 100
        x = file['x'][j]
        mono = file['mono'][j]
        quad = file['quad'][j]
        if abs(mono) < 1000 and abs(quad) < 1000:
            x = mpmath.mpmathify(str(x))
            mono = mpmath.mpmathify(str(mono))
            quad = mpmath.mpmathify(str(quad))
            coor[i][0][j] = file['x'][j]
            coor[i][1][j] = mpmath.fmul(mpmath.power(x, 2), mono)
            coor[i][2][j] = mpmath.fmul(mpmath.power(x, 2), quad)
    
        #plt.plot(coor[i][0], coor[i][1], 'b-')
        #plt.plot(coor[i][0], coor[i][2], 'g-')

mean = np.transpose(np.nanmean(coor, axis=0))
plt.plot(mean[0], mean[1], 'b-', linewidth=2)
plt.plot(mean[0], mean[2], 'g-', linewidth=2)

mean = np.delete(mean, 1, 1)

plt.savefig('corr_' + str(first) + '-' + str(last) + '.png')
np.savetxt('avg_corr_fun.txt', mean)
