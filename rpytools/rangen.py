import numpy as np
import rpytools.tpareto as tpr
import rpytools.modlav as ml
import rpytools.lognormal as logn
import rpytools.pareto as par
import random
import math

# Individual random number with random seed.
def get_random():
	r = random.SystemRandom()
	return r

# Random number generator class
class Rangen:
	"""
	Random number generator class. The class will be configured for one type of random generator
	and save the random state.
	The generator will be seeded using random.SystemRandom number.
	"""

	def __init__(self, d, plist):
		"""
		Constructor.

		Inputs
		-------
		d: The distribution for random variates. Currently supported values are
			normal, lognormal, modlav, exponential, pareto, tpareto [for Truncated Pareto]

		plist: A tuple of parameters for the distribution.
		Normal, Lognormal: [0] = mu, [1] = sigma
		ModLav: [0] = beta, [1] = c, [2] = d
		Exponential: [0] = lambda
		Pareto: [0] = k, [1] = alpha
		Truncated pareto: [0] = k, [1] = m, [2] = alpha
		"""

		self.__dist_map = {"normal": self.__normal_rnd, \
								 "lognormal": self.__lognormal_rnd, \
								 "modlav": self.__modlav_rnd, \
								 "exponential": self.__exponential_rnd, \
								 "pareto": self.__pareto_rnd, \
								 "tpareto": self.__tpareto_rnd, \
								 "uniform": self.__uniform_rnd
								 }
		
		if d not in self.__dist_map:
			raise NotImplemented("Distribution is not implemented - " + str(d))

		self.__df = self.__dist_map[d]
		self.__plist = plist
		self.__rnd = get_random()

	def __normal_rnd(self, n):
		arnd = np.zeros(n, dtype=float)	
		mu = self.__plist[0]
		sigma = self.__plist[1]

		for i in xrange(n):
			arnd[i] = self.__rnd.gauss(mu, sigma)
		
		return arnd
	
	def __lognormal_rnd(self, n):
		arnd = np.zeros(n, dtype=float)
		mu = self.__plist[0]
		sigma = self.__plist[1]

		for i in xrange(n):
			arnd[i] = self.__rnd.lognormvariate(mu, sigma)
		
		return arnd
	
	# Re-coding the cdf-inverse here. Need the random numbers to come from
	# the same seed/state that is stored.
	def __modlav_rnd(self, n):
		beta = self.__plist[0]
		c = self.__plist[1]
		d = self.__plist[2]

		ur = np.zeros(n, dtype=float)
		for i in xrange(n):
			ur[i] = self.__rnd.random()

		rvs = c*np.power(ur/(1 + d - ur), beta)
		return rvs

	def __exponential_rnd(self, n):
		arnd = np.zeros(n, dtype=float)
		ex_lambda = self.__plist[0]
		for i in xrange(n):
			arnd[i] = self.__rnd.expovariate(ex_lambda)

		return arnd

	
	# Re-coding the cdf-inverse here. The random numbers need to come
	# from the same seed/state and the npr.pareto is a simplistic 
	# implementation.
	def __pareto_rnd(self, n):
		k = self.__plist[0]
		alpha = self.__plist[1]

		ur = np.zeros(n, dtype=float)
		for i in xrange(n):
			ur[i] = self.__rnd.random()

		rvs = k/np.power(ur, 1.0/alpha)
		return rvs
	
	# Re-coding the cdf-inverse here. The random numbers need to come
	# from the same seed/state.
	def __tpareto_rnd(self, n):
		k = self.__plist[0]
		m = self.__plist[1]
		alpha = self.__plist[2]
		
		lb = math.pow(k/m, alpha)/(1 + math.pow(k/m, alpha))
		ub = 1/(1 + math.pow(k/m, alpha))
		
		ur = np.zeros(n, dtype=float)
		for i in xrange(n):
			ur[i] = self.__rnd.uniform(lb, ub)

		k1 = k/math.pow((1 + math.pow(k/m, alpha)), 1/alpha)
		rvs =  k1*np.power(ur, -1/alpha)
		return rvs
	
	def __uniform_rnd(self, n):
		lb = self.__plist[0]
		ub = self.__plist[1]

		arnd = np.zeros(n, dtype=float)
		for i in xrange(n):
			arnd[i] = self.__rnd.uniform(lb, ub)

		return arnd

	
	def rvs(self, n):
		"""
		Generate n random variantes

		Input
		-----
		n: Number of variates to generate

		Output
		------
		A numpy array with n random variates
		"""
		
		rvs = self.__df(n)
		return rvs

