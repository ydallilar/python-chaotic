#!/usr/bin/python

#linearized pendulum problem
#plots phase space

from numpy import sin,pi
import matplotlib 
matplotlib.use("gtk3cairo")
import matplotlib.pyplot as plt

def f1 (t,x,y) :
  return y

def f2 (t,x,y) :
  return -sin(x)
  
def solve (init) :
  f = (f1,f2)
  dt = 0.001
  t = 0
  i = 0
  
  res = ([init[0]],[init[1]])
  
  while (i < 15000) :
    j = 0
    while (j < 2) :
      k1 = dt * f[j](t,res[0][i],res[1][i])
      k2 = dt * f[j](t+dt/2,res[0][i]+k1/2,res[1][i]+k1/2)
      k3 = dt * f[j](t+dt/2,res[0][i]+k2/2,res[1][i]+k2/2)
      k4 = dt * f[j](t+dt,res[0][i]+k3,res[1][i]+k3)
      res[j].append(res[j][i] + 1./6. * (k1 + 2*k2 + 2*k3 + k4))
      j = j + 1
    i = i + 1  
    t = t + dt
  
  plt.plot(res[0],res[1])
  plt.show()
