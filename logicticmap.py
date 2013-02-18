#!/usr/bin/python

##################################################################
#  Yigit Dallilar  04.02.2013                                    #
#                                                                #
#  Logistic map study libraries for chaotic dynamics.            #
##################################################################

import pylab as plt
from numpy import linspace
from sympy import diff,var,log,Abs,N

##################################################################
# function with parameters
def f(mu,x,times) :
  if (times == 1) :
    return mu*x*(1-x)
  else :
    times = times - 1
    return f(mu,mu*x*(1-x),times)

##################################################################  
def plot(mu,xi,times,steps=50) :
  
  point = ([xi],[0.])
  
  i=0
  while i < steps :
    point[0].append(xi)
    xi = f(mu,xi,times)
    point[1].append(xi)
    point[0].append(xi)
    point[1].append(xi)
    i = i + 1
    
  plt.plot(point[0],point[1],'k-')
  sp = linspace(0,1,num=500)
  plt.plot(sp,f(mu,sp,times),'b-')
  plt.plot([0,1],[0,1],'r-')
  plt.show()

##################################################################
def lyapunovexp(muint,xi,int=0.1,n=1000) :
  x = var('x')
  lexp = ([])
  steps = (muint[1]-muint[0])/int
  mu = linspace(muint[0],muint[1],num=steps+2)
  j = 0
  while ( j < len(mu)) :
    fp = diff(f(mu[j],x,1),x,1)
    total = 0.
    i = 0
    while (i < n) :
      total = total + N(log(Abs(fp.subs(x,xi)))) 
      xi = f(mu[j],xi,1)
      i = i + 1
    lexp.append(1./n*total)  
    j = j + 1
  
  plt.plot(mu,lexp,'k-')
  plt.show()
  
##################################################################  
