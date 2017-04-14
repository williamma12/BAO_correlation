import numpy as np
import sys

file_number = sys.argv[1]

DD=open('result/result_south_' + str(file_number) + '-DD.dat')
DR=open('result/result_south_' + str(file_number) + '-DR.dat')
RR=open('result/result_south_' + str(file_number) + '-RR.dat')
norm=open('result/result_south_' + str(file_number) + '-norm.dat')

#DD=open('result_south2-DD.dat')
#DR=open('result_south2-DR.dat')
#RR=open('result_south2-RR.dat')

#get DD/RR
numDD=float(norm.readline().split()[1])
numRR=float(norm.readline().split()[1])
rat=numDD/numRR

#get s and mu
x=DD.readline().split()
y=DD.readline().split()
x=map(float,x)
y=map(float,y)
x=np.asarray(x)
y=np.asarray(y)

#initialize the xi2d array
num_row=len(y) #101
num_column=len(x) #203
num=(num_row-1)*(num_column-1)
xi2d=np.zeros([num,3])
print(xi2d)
#skip two lines for RR and DR
RR.readline()
RR.readline()
DR.readline()
DR.readline()

ii=0
for line in DD:
   ii=ii+1
   low=(ii-1)*(num_row-1)
   high=(ii)*(num_row-1)
   DD_line=np.asarray(map(float,line.split()))
   RR_line=np.asarray(map(float,RR.readline().split()))
   DR_line=np.asarray(map(float,DR.readline().split()))

   xi2d[low:high,0]=(x[ii-1]+x[ii])/2.0
   xi2d[low:high,1]=(y[0:num_row-1]+y[1:num_row])/2.0
   xi2d[low:high,2]=DD_line-2*rat*DR_line+rat*rat*RR_line

   #xi2d[low:high,2]=xi2d[low:high,2]/(rat*rat*RR_line)
   with np.errstate(divide='ignore', invalid='ignore'):
      xi2d[low:high,2] = np.true_divide(xi2d[low:high,2], (rat*rat*RR_line))
      xi2d[low:high,2][xi2d[low:high,2] == np.inf] = 0
      xi2d[low:high,2] = np.nan_to_num(xi2d[low:high,2])
#   print  xi2d[low:high,2]
#   if(ii==5):
#       print RR_line
#       print DR_line
#       print RR_line

np.savetxt('xi2d/xi2d-' + str(file_number) + '.txt',xi2d,fmt='%6f')
