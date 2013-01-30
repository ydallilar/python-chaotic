#!/usr/bin/python

##################################################################
#  Yigit Dallilar  30.01.2010
#
#  For chaotic pendulum problem, program draws phase space euler
# or runge-kutta is optional.
##################################################################
# variables :
# w  : angular frequency
# th : angle
# ph : driven angle
# wd : driven angular frequency
# q  : damping factor
# g  : driven force amplitude
##################################################################
# How to use : 
# var = numpy.array([w,th,ph])
# cnst = numpy.array([q,g,wd])
#
# for runge-kutta :
# solve(var,cnst,'dt','steps','plotstep')
# for euler : 
# solve2(var,cnst,'dt','steps','plotstep')
##################################################################

from numpy import sin,cos,pi,array,zeros,rint
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
  res = ([var[0]],[var[1]],[var[2]],[t])
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
    res[3].append(t+dt)
    
    i = i + 1  
    t = t + dt
  
  i = 0
  while (i < steps + 1) :
    if ((res[1][i] % (2*pi)) > (res[1][i] % pi)) : 
      res[1][i] = - (pi - (res[1][i] % pi))
    else :
      res[1][i] = res[1][i] % pi
    i = i + 1 
  
  return res
  
##################################################################
# euler method
def solve2(var,cnst,dt=0.0001,steps=100000,plotstep=100) :
  f = (fw,fth,fph)
  t = 0
  tmp = var
  res = ([var[0]],[var[1]],[var[2]],[t])
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
  
  return res
  
##################################################################  
# plots phase space
def phase_space(res,plotstep=100) :
  plt.plot(res[1][0::plotstep],res[0][0::plotstep],'k.',markersize=1)
  plt.xlim(-pi,pi)
  plt.show()  

##################################################################
# plots poincare sections
def poincare_sec(res,const,strobe=1./5,plotstep=100,steady=30) :
  sect_res = ([],[],[])
  time = 2*pi*strobe/const[2]
  
  i = 0
  j = 0
  while (i < len(res[0])) :
    if (time*j <= res[3][i]) :
      if (j >= steady) :
        sect_res[0].append(res[0][i])
        sect_res[1].append(res[1][i])
        sect_res[2].append(res[2][i])
      mult = mult + 1
    i = i + 1
  
  plt.plot(sect_res[1][0::plotstep],sect_res[0][0::plotstep],'k*',markersize=5)
  plt.xlim(-pi,pi)
  plt.show()  
  
##################################################################
# plots t versus th or w
def plott(res,opt="w",timeint=0.1) :
  arr = ([],[],[],[])
  i = 0
  j = 0
  while (i < len(res[0])) :
    if (timeint*j <= res[3][i]) :
      arr[0].append(res[0][i])
      arr[1].append(res[1][i])
      arr[2].append(res[2][i])
      arr[3].append(res[3][i])
      j = j + 1
    i = i + 1
  
  if (opt == "w") : plt.plot(arr[3],arr[0])
  if (opt == "th") : plt.plot(arr[3],arr[1])
  if (opt == "ph") : plt.plot(arr[3],arr[2])
  plt.show()  
    
##################################################################      
# fourier transform
def fourier (res) :
  dt = res[3][1] - res[3][0]
  term1 = lambda t,w,dt : res[1][int(rint(t/dt))]*cos(w*t)*dt
  term2 = lambda t,w,dt : -res[1][int(rint(t/dt))]*sin(w*t)*dt
  
  power = []
  i = 0
  while (i < 100) :
    w = i/50.
    sum1 = 0
    sum2 = 0
    for t in res[3] :
      sum1 = sum1 + term1(t,w,dt)
      sum2 = sum2 + term1(t,w,dt)
    power.append((sum1 + sum2)**2)
    i = i + 1
  return power
  
##################################################################  
