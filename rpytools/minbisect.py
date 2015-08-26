import numpy as np
import scipy.optimize as opt
import math
from scipy.optimize import fsolve
from scipy.optimize import bisect
from rpytools.util import read_data
from rpytools.util import ecdf

def solve_t(a_i, d):
	return ((1.0 + d)/a_i) - 1.0

def dqdc(x_i, a_i, b, c, d):
	t = solve_t(a_i, d)

	t1 = (-1/math.pow(c,2.0))*np.sum(np.power(x_i, 2.0)*np.power(t, b))
	t2 = np.sum(np.power(t, -b))

	r = t1 + t2

	return r

def dqdd(x_i, a_i, b, c, d):
	t = solve_t(a_i, d)

	t1 = (1.0/c)*np.sum( (np.power(x_i, 2.0)/a_i)*np.power(t, b-1.0) )
	t2 = c*np.sum(np.power(t, -b-1.0)/a_i)

	r = t1 - t2

	return r

def dqdb(x_i, a_i, b, c, d):
	t = solve_t(a_i, d)

	t1 = (1.0/c)*np.sum(np.power(x_i, 2.0)*np.power(t, b)*np.log(t))
	t2 = c*np.sum(np.log(t)/np.power(t,b))

	r = t1 - t2

	return r

def eq_beta(ival, *args):
	d = args[0]
	x_i = args[1]
	a_i = args[2]

	t = solve_t(a_i, d)

	b = ival

	t11 = np.sum((np.power(x_i, 2.0)/a_i)*np.power(t, b-1.0))
	t12 = np.sum(np.power(x_i, 2.0)*np.power(t, b)*np.log(t))
	t1 = t11/t12

	t21 = np.sum(np.power(t, -b-1.0)/a_i)
	t22 = np.sum(np.log(t)*np.power(t, -b))
	t2 = t21/t22

	r = t1 - t2

	return r

def solve_beta(x_i, a_i, d):
	
	# oval = (d, x_i, a_i)
	# ival = [np.median(x_i)]

	# (fvals, infodict, ier, mesg) = fsolve(eq_beta, ival, oval, None, 1, 0, 1e-12, 2000)
	# beta = fvals[0]
	# if ier != 1:
	# 	final_mesg = mesg + " solved upto beta = " + str(beta)
	# 	raise RuntimeError(final_mesg)

	# return beta

	beta = bisect(eq_beta, 0.5, 1.5, (d, x_i, a_i))

	return beta

		
def solve_c(x_i, a_i, b, d):
	t = solve_t(a_i, d)
	t1 = np.sum(np.power(x_i, 2.0)*np.power(t, b))
	t2 = np.sum(np.power(t, -b))

	c = math.sqrt(t1/t2)

	return c

def eq_d(ival, *args):
	d = ival

	b = args[0]
	c = args[1]
	x_i = args[2]
	a_i = args[3]

	r = dqdb(x_i, a_i, b, c, d)

	return r

def solve_d(x_i, a_i, b, c):
	oval = (b, c, x_i, a_i)
	## ival = [0.0]

	## (fvals, infodict, ier, mesg) = fsolve(eq_d, ival, oval, None, 1, 0, 1e-12, 2000)
	## d = fvals[0]

	## if ier != 1:
	## 	final_mesg = mesg + " solved upto d = " + str(d)
	## 	raise RuntimeError(final_mesg)

	## return d

	d = bisect(eq_d, 0, 0.3, oval)

	return d

def solver(pts):
	npts = np.array(pts)
	pts.sort()

	c = ecdf(pts)
	x_i = c[:,0]
	a_i = c[:,1]

	b = 1.0
	c = np.median(npts)
	d = c/float(pts.max())

	N = 2000
	n = 0
	tol = 1e-8

	tolc = float('Inf')
	tolb = float('Inf')
	told = float('inf')

	while (n < N and (tolc > tol or told > tol or tolb > tol)):
		b = solve_beta(x_i, a_i, d)
		c = solve_c(x_i, a_i, b, d)
		d = solve_d(x_i, a_i, b, c)

		tolc = abs(dqdc(x_i, a_i, b, c, d))
		told = abs(dqdd(x_i, a_i, b, c, d))
		tolb = abs(dqdb(x_i, a_i, b, c, d))

		print "n: ", n
		print "beta: ", b, " c: ", c, "d: ", d
		print "tolc: ", tolc, " told: ", told, "tolb: ", tolb

	if ( n >= N ):
		params = {"beta": b, "c": c, "d": d}
		raise RuntimeError("Cannot converge: " + str(params))
	
	return (b, c, d)
