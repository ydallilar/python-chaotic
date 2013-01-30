##################################################################
#!/usr/bin/python

#chaotic pendulum problem
#plots phase space

# variables
# w  : angular frequency
# th : angle
# ph : driven angle
# wd : driven angular frequency
# q  : damping factor
# g  : driven force amplitude

from numpy import sin,cos,pi,array,zeros,concatenate
import matplotlib 
matplotlib.use("gtk3cairo")
import matplotlib.pyplot as plt

##################################################################
# dw/dt
def fw (t,var,cnst) :
  return -var[0]/cnst[0]-sin(var[1])+cnst[1]*cos(var[2])

# dth/dt
def fth (t,var,cnst) :
  return var[0]

# dph/dt  
def fph (t,var,cnst) :
  return cnst[2]

##################################################################
# just runge-kutta for this problem  
def solve (var,cnst,dt=0.001,steps=100000,plotstep=100) :
  f = (fw,fth,fph)
  t = 0
  tmp = var
  res = ([var[0]],[var[1]],[var[2]])
  k = zeros((4,3))
  
  i = 0
  while (i < steps) :
    k[0] = dt * array([f[0](t,tmp,cnst),f[1](t,tmp,cnst),f[2](t,tmp,cnst)])
    k[1] = dt * array([f[0](t+0.5*dt,tmp+k[0]*0.5,cnst),f[1](t+0.5*dt,tmp+k[0]*0.5,cnst),f[2](t+0.5*dt,tmp+k[0]*0.5,cnst)])
    k[2] = dt * array([f[0](t+0.5*dt,tmp+k[1]*0.5,cnst),f[1](t+0.5*dt,tmp+k[1]*0.5,cnst),f[2](t+0.5*dt,tmp+k[1]*0.5,cnst)])
    k[3] = dt * array([f[0](t+dt,tmp+k[2],cnst),f[1](t+dt,tmp+k[2],cnst),f[2](t+dt,tmp+k[2],cnst)])
    tmp = array([res[0][i],res[1][i],res[2][i]]) + 1./6. * (k[0] + k[3] + 0.5*(k[1] + k[2]))
    res[0].append(tmp[0])
    res[1].append(tmp[1]) 
    res[2].append(tmp[2])
    
    i = i + 1  
    t = t + dt
  
  i = 0
  while (i < steps + 1) :
    if ((res[1][i] % (2*pi)) > (res[1][i] % pi)) : 
      res[1][i] = - (pi - (res[1][i] % pi))
    else :
      res[1][i] = res[1][i] % pi
    i = i + 1 
  
  plt.plot(res[1][0::100],res[0][0::100],'k.',markersize=1)
  plt.xlim(-pi,pi)
  plt.show()
  return res
  
##################################################################
# euler method
def solve2(var,cnst,dt=0.0001,steps=100000,plostep=100) :
  f = (fw,fth,fph)
  t = 0
  tmp = var
  res = ([var[0]],[var[1]],[var[2]])
  k = zeros(3)
  
  i = 0
  while (i < steps) :
    k = dt * array([f[0](t,tmp,cnst),f[1](t,tmp,cnst),f[2](t,tmp,cnst)])
    tmp = array([res[0][i],res[1][i],res[2][i]]) + k
    res[0].append(tmp[0])
    res[1].append(tmp[1]) 
    res[2].append(tmp[2])
    i = i + 1
  
  i = 0
  while (i < steps + 1) :
    if ((res[1][i] % (2*pi)) > (res[1][i] % pi)) : 
      res[1][i] = - (pi - (res[1][i] % pi))
    else :
      res[1][i] = res[1][i] % pi
    i = i + 1 
  
  plt.plot(res[1][0::plotstep],res[0][0::plotstep],'k.',markersize=1)
  plt.xlim(-pi,pi)
  plt.show()  
  return res
