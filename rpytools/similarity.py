from scipy.special import gamma
from scipy.integrate import simps
from scipy.integrate import quad
from scipy.integrate import fixed_quad
from scipy.stats.mstats import mquantiles
from math import pi
from math import pow
from math import exp
from math import factorial
import numpy as np

def bws(x, y, **kwargs):
	"""
	The baumgartner weiss schindler test. To ascertain similarity between two data sets
	Input
	-----
	x1: Sample X
	x2: Sample Y
	**kwargs: j = number of iterations
	"""
	x.sort()
	y.sort()
	npx = np.array(x)
	npy = np.array(y)

	xs = np.unique(npx)
	ys = np.unique(npy)
	xys = set(xs).union(set(ys))
	axy = np.array(list(xys))
	axy.sort()

	G = np.array([len(axy[np.where(axy <= xi)]) for xi in xs])
	H = np.array([len(axy[np.where(axy <= yi)]) for yi in ys])

	n = len(G)
	m = len(H)
	fn = float(n)
	fm = float(m)

	N = np.linspace(1,n,num=n)
	M = np.linspace(1,m,num=m)

	xt1 = np.power(G - N*(fm + fn)/fn, 2.0)
	xtt = N/(fn+1.0)
	xt2 = xtt*(1 - xtt)*(fm * (fm+fn)/fn)
	Bx = np.sum(xt1/xt2)/fn
	
	yt1 = np.power(H - M*(fm + fn)/fm, 2.0)
	ytt = M/(fm+1.0)
	yt2 = ytt*(1 - ytt)*(fn * (fm+fn)/fm)
	By = np.sum(yt1/yt2)/fm

	B = (Bx+By)/2.0

	print "B = ", B
	
	J = 3
	if "j" in kwargs:
		J = kwargs["j"]
	
	return compute_xi(B, J)

def compute_xi(B, J):
	jspace = np.linspace(0,J,num=J+1)
	fbws = np.vectorize(compute_b)
	xi_array = fbws(jspace, B)
	return pow(pi/2.0, 0.5)*np.sum(xi_array)/B
	

def compute_b(j, b):
	ij = int(j)
	t1 = (-1)**ij * gamma(ij+0.5)/gamma(0.5)*factorial(ij)
	t2 = 4*ij + 1

	t3 = quad(integral_function, 0.0, 1.0, args=(j,b,))

	return t1*t2*t3

def integral_function(r, j, b):
	t1 = 1.0/pow( pow(r,3.0)*(1-r), 0.5)
	t2 = (r*b)/8.0
	t3 = (pi**2)*( (4.0*j +1)**2 )/(8.0*r*b)
	return t1 * exp(t2-t3)


def new_similarity_invcdf(x,y):
	x.sort()
	y.sort()
	npx = np.array(x)
	npy = np.array(y)

	## simidx = quad(sy_integral_function, 0.0, 1.0, args=(npx, npy,),full_output=1)

	## print "Error: ", simidx[1]
	## print "Info: ", simidx[2]
	## print "Message: ", simidx[3]

	xspace = np.linspace(0.0, 1.0, num=max(len(npx), len(npy)))
	yspace = np.array([sy_integral_function(q, npx, npy) for q in xspace])
	simidx = simps(yspace, xspace)
		


	return simidx

def sy_integral_function(q, x, y):
	f1_inv = mquantiles(x, [q])
	f2_inv = mquantiles(y, [q])
	
	if ( f1_inv[0] == 0.0 and f2_inv[0] == 0.0 ):
		return 1.0
	else:
		return min(f1_inv[0], f2_inv[0])/float(max(f1_inv[0], f2_inv[0]))
