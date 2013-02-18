#!/usr/bin/python

##################################################################
#  Yigit Dallilar  18.02.2013                                    #
#                                                                #
#  Circle map study libraries for chaotic dynamics.             #
##################################################################

import pylab as plt
from numpy import linspace,pi,sin,array
from sympy import diff,var,log,Abs,N

##################################################################
#function with parameters
def f(om,K,x,times) :
  if (times == 1) :
    return x+om-(K/(2.*pi))*sin(2.*pi*x)
  else :
    times = times - 1
    return f(om,K,x+om-(K/(2.*pi))*sin(2.*pi*x),times)

##################################################################
def plot(om,K,xi,times,steps=50) :
  
  point = ([xi],[0.])
  
  i=0
  while i < steps :
    point[0].append(xi)
    xi = f(om,K,xi,times)
    point[1].append(xi)
    point[0].append(xi)
    point[1].append(xi)
    i = i + 1
  
  point = array([point[0],point[1]])
  point = point % 1  
  plt.plot(point[0],point[1],'k-')
  
  sp = linspace(0,1,num=500)
  res = f(om,K,sp,times)
  res = res % 1
  plt.plot(sp,res,'b.')
  
  plt.plot([0,1],[0,1],'r-')
  
  plt.show()

##################################################################
def plotomvswinding(omint,K,xi=0.1,int=0.01,iter=1000) :
  
  res = ([])
  steps = (omint[1]-omint[0])/int
  om = linspace(omint[0],omint[1],num=steps+1)
    
  for val in om :
    tmp = f(val,K,xi,1)
    i = 0
    while ( i < iter -1 ) : 
      tmp = f(val,K,tmp,1)
      i = i + 1
    res.append((tmp-xi)/iter)  
    
  plt.plot(om,res,'k-')
  plt.ylim(-0.1,1.1)
  plt.show()
##################################################################
