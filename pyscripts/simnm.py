import numpy as np
import numpy.random as npr
from random import SystemRandom
from pyscripts.simidx import newmetric
from rpytools.pareto import Pareto
import rpytools.util as util
from rpytools.similarity import new_similarity_invcdf
from scipy.stats import norm
import math

def conf_est(darray,conf_level):
	n = float(len(darray))
	mu = np.mean(darray)
	sigma = np.std(darray)
	alpha = 1-conf_level
	z_alpha_2 = norm.ppf(1-(alpha/2.0))
	e = z_alpha_2/math.sqrt(n)
	print mu, " ", e, " ", mu-e, " ", mu+e
	return (mu-e,mu+e)

def min_conf_est(darray,conf_level):
	(x,y) = conf_est(darray,conf_level)
	return x

def max_conf_est(darray,conf_level):
	(x,y) = conf_est(darray, conf_level)
	return y

def simexp(nvars):
	nvar1 = nvars[0]
	nvar2 = nvars[1]

	r = SystemRandom()
	npr.seed(r.randint(0,1e15))
	x = npr.exponential(30, nvar1)
	npr.seed(r.randint(0,1e15))
	y = npr.exponential(35,nvar2)
	
	if False:
		x.sort()
		y.sort()
	
		darray = np.zeros(100)
		for i in xrange(0,100):
			yprime = r.sample(y, len(x))
			yprime.sort()
			darray[i] = util.dice(x,yprime)
			return max_conf_est(darray, 0.99)


	return new_similarity_invcdf(x,y)
	

def simpareto(nvars):
	nvar1 = nvars[0]
	nvar2 = nvars[1]

	p1 = Pareto(2000.0, 2.0)
	p2 = Pareto(2000.0, 1.0)

	x = p1.rnd(nvar1)
	y = p2.rnd(nvar2)

	x.sort()
	y.sort()
	
	if False:
		r = SystemRandom()

		darray = np.zeros(100)
		for i in xrange(0,100):
			yprime = r.sample(y, len(x))
			darray[i] = util.dice(x,yprime)
			return max_conf_est(darray, 0.99)

	return new_similarity_invcdf(x, y)

def main():
	tups = [(200,2000),(2000,3000),(3000,4000)]
	
	print "------------- Exponential -----------------"
	for tup in tups:
		for i in xrange(0,3):
			s = simexp(tup)
			print tup, " ", i, " ", s


	print "------------- Pareto -----------------"
	for tup in tups:
		for i in xrange(0,3):
			s = simpareto(tup)
			print tup, " ", i, " ", s

if __name__ == "__main__":
	main()
