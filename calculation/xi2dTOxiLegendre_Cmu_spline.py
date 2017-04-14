#Program to calculate the multipoles of correlation function from 2d correlation function with appropriate alpha(cosmological shifts)
import numpy as np
import matplotlib.pylab as pl
import sys

import scipy.integrate as ssI
from scipy import interpolate


plotss=0 #whether you want to see the plot or not
monopole=0
try:
   xi2d_file=sys.argv[1]
   outfile=xi2d_file+'_L02'
   if(monopole):
      outfile=outfile+'1'
   outfile=outfile+'s'
except:
   print '**********************'
   print 'Usage: python xi2dTOxiLegendre_Cmu.py <xi2d_file>'
   print 'Enter file name for 2d correlation function with columns (r,mu,xi2d)'
   print 'The mu should be equally sampled'
   print '*********************'
   sys.exit()


#change these numbers to get a range for correlation function smin,smax,sbin
smin=0
smax=202
sbin=50

#smin=6.0
#smax=94.0
#sbin=12

#smin = 1.5
#smax = 60.5
#sbin = 60

dss=(smax-smin)/(sbin-1)
wss=0.5  #Mpc/h integration width
PiBy2=np.pi/2

#parameters
apar=1.00
aper=1.0

aper2=aper*aper
diffa2=apar*apar-aper*aper


#load the 2d correlation function
c2d=np.loadtxt(xi2d_file)

#shift the correlation functon with apar and aper
#shifting 2d correlation function with alpha
c2d_shift=np.zeros(c2d.size).reshape(c2d.shape)
c2d_shift[:,0]=np.sqrt(diffa2*np.power(c2d[:,0]*c2d[:,1],2)+aper2*np.power(c2d[:,0],2))
c2d_shift[:,1]=apar*c2d[:,0]*c2d[:,1]/c2d_shift[:,0]


def find_xi2d_sampling(xi2d):
   N=xi2d.shape[0]  # Total number of mu adn r sampling
   rF=xi2d[0,0]     #first r bin
   rL=xi2d[-1,0]    #last r bin
   nrF=0            #number of r bins with first mu
   nrL=0            #number of r bins with last mu
   muF=xi2d[0,1]    #first mu bin
   muL=xi2d[-1,1]   #last mu bin
   nmuF=0           #number of mu bins with first r
   nmuL=0           #number of mu bins with last r
   for ii in range(0,N):
      if(xi2d[ii,0]==rF):
         nmuF=nmuF+1
      elif(xi2d[ii,0]==rL):
         nmuL=nmuL+1

      if(xi2d[ii,1]==muF):
         nrF=nrF+1
      elif(xi2d[ii,1]==muL):
         nrL=nrL+1

   if(nrL!=nrF or nmuF!=nmuL or nrL*nmuL!=N):
      print 'Error, The xi2d seems to have invalid sampling'
      print 'nrF, nrL, nmuF, nmuL,N: ',nrF, nrL, nmuF, nmuL,N
      sys.exit()

   dmus=xi2d[1:nmuF,1]-xi2d[:nmuF-1,1]
   avgmu=np.mean(dmus)
   diff=np.sum(np.power(dmus-avgmu,2))
   if(diff<1e-6):
      print 'Sampling test passed: equal mu sampling'
   elif(diff>1e-6): # and args.sampling=='theta'):
      print 'Sampling test failed: equal theta sampling'

   rr2d=xi2d[np.arange(0,N,nmuF),0]
   mu2d=xi2d[:nmuF,1]
   return rr2d,nrF, mu2d, nmuF

def Interp_shift_2d(c2d_shift,c2d):
   
   rr2d,nr, mu2d, nmu=find_xi2d_sampling(c2d)
   N2d=nr*nmu
   #To store interpolated xi
   c2d_interp=np.zeros(N2d)

   #interpolate along r for same mu
   for ii in range(0,nmu):
      ind=np.arange(ii,N2d,nmu)
      Ixir=interpolate.splrep(c2d_shift[ind,0],c2d[ind,2], s=0,k=1)
      c2d_interp[ind]=interpolate.splev(rr2d,Ixir, der=0)

   #interpolate along mu for same r
   for ii in range(0,nr):
      ind=np.arange(ii*nmu,(ii+1)*nmu)
      Iximu=interpolate.splrep(c2d_shift[ind,1],c2d_interp[ind], s=0,k=1)
      c2d_interp[ind]=interpolate.splev(mu2d,Iximu, der=0)

   c2d[:,2]=c2d_interp

   return c2d,nr,nmu,rr2d,mu2d

def Legendre_basis(c2d,nr,nmu,rr2d,mu2d):
   mu2=np.power(c2d[:,1],2)
   P0=np.ones(mu2.size)
   P1=3*c2d[:,1]
   P2=2.5*(3*mu2-1)
   
   print 'nr,nmu: ',nr,nmu, rr2d.size
   xi0_r=np.zeros(nr)
   xi2_r=np.zeros(nr)
   if(monopole==1):
      xi1_r=np.zeros(nr)

   #integrate along mu
   for ii in range(0,nr):
      ind=np.arange(ii*nmu,(ii+1)*nmu)
      Imu0=interpolate.splrep(c2d[ind,1],c2d[ind,2]*P0[ind], s=0,k=1)
      xi0_r[ii]=ssI.quad(lambda mu: interpolate.splev(mu,Imu0, der=0), 0,1,maxp1=500)[0]
  
      Imu2=interpolate.splrep(c2d[ind,1],c2d[ind,2]*P2[ind], s=0,k=1)
      xi2_r[ii]=ssI.quad(lambda mu: interpolate.splev(mu,Imu2, der=0), 0,1,maxp1=500)[0]
      if(monopole==1): 
         Imu1=interpolate.splrep(c2d[ind,1],c2d[ind,2]*P1[ind], s=0,k=1)
         xi1_r[ii]=ssI.quad(lambda mu: interpolate.splev(mu,Imu1, der=0), 0,1,maxp1=500)[0]

      #if(ii<nmu):
      #   pl.plot(rr2d,np.power(rr2d,2)*c2d[np.arange(ii,nr*nmu,nmu),2],'k--')

   #pl.figure()
   #pl.plot(rr2d,np.power(rr2d,2)*xi0_r,'r-')
   #pl.show()

   #bin xi02 as per requirement

   Ixi0=interpolate.splrep(rr2d,xi0_r, s=0,k=1)
   Ixi2=interpolate.splrep(rr2d,xi2_r, s=0,k=1)
   if(monopole==1): 
      Ixi1=interpolate.splrep(rr2d,xi1_r, s=0,k=1)

   # To store xi02
   npole=2
   if(monopole==1):
      npole=3
   xi_leg=np.zeros(sbin*(npole+1)).reshape(sbin,npole+1)
   for ii in range(0,sbin):
      ss=smin+dss*ii
      s1=ss-wss; s2=ss+wss
      xi_leg[ii,0]=ss
      xi_leg[ii,1]=ssI.quad(lambda rr: interpolate.splev(rr,Ixi0, der=0), s1,s2,maxp1=500)[0]
      xi_leg[ii,2]=ssI.quad(lambda rr: interpolate.splev(rr,Ixi2, der=0), s1,s2,maxp1=500)[0]
      if(monopole==1):
         xi_leg[ii,3]=ssI.quad(lambda rr: interpolate.splev(rr,Ixi1, der=0), s1,s2,maxp1=500)[0]

      xi_leg[ii,1:]=xi_leg[ii,1:]/(2*wss)
  
   #write into file
   np.savetxt(outfile,xi_leg)
   print 'input  file: ',xi2d_file
   print 'output file: ',outfile
 
   if(plotss==1):
      r2=np.power(rr2d,2)
      pl.plot(rr2d,r2*xi0_r,'r-')
      pl.plot(rr2d,r2*xi2_r,'r--')
      r2=np.power(xi_leg[:,0],2)
      pl.plot(xi_leg[:,0],r2*xi_leg[:,1],'k-')
      pl.plot(xi_leg[:,0],r2*xi_leg[:,2],'k--')
      pl.show()
      plots(xi_leg)

   return xi_leg

def plots(xi02):
   pl.plot(xi02[:,0],xi02[:,0]*xi02[:,0]*xi02[:,1],'ro-',label='mono')
 #  pl.plot(xi02[:,0],xi02[:,0]*xi02[:,0]*xi02[:,2],'ro-',label='quad')
   pl.legend()
   pl.title('CMASS simulation galaxy (rand 1600000)')
   pl.show()

find_xi2d_sampling(c2d)
c2d,nr,nmu,rr2d,mu2d=Interp_shift_2d(c2d_shift,c2d)
Legendre_basis(c2d,nr,nmu,rr2d,mu2d)
