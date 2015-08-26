import math
import numpy as np
import scipy.optimize as opt
import util

"""
The Double Pareto distribution.
References:
1. M. Mitzenmacher, Dynamic models for file sizes and Double Pareto distributions, 
	Internet Mathematics, vol. 1, no. 3, pp 305 -- 333
2. M. Mitzenmacher and B. Tworetzky, New models and methods for file size distributions,
	41st Annual Allerton conference on communication, control and computing, pp 603 -- 612, 2003.
3. W. J. Reed and M. Jorgensen, The double pareto distribution - A new parametric model for size distirbutions,
	Statistics: Theory and Methods, vol. 33, no. 8, pp 1733 - 1753
"""

class DoublePareto:
	"""
	The double pareto class

	Static methods
	---------------
	mmefit: Fit using moments
	fromFit: Create a new double pareto object with parameters estimated from mmefit

	Instance methods
	-----------------
	pdf: Density function
	cdf: Distribution function
	ccdf: Complementary distribution function
	cdf_inv: Inverse distribution function
	ccdf_inv: Inverse complementary distribution function
	rnd: Random variates
	alpha: alpha-value
	beta: beta-value
	"""

	@staticmethod
	def __solve_mme(ival, *args):
		ialpha = ival[0]
		ibeta = ival[1]

		EY = args[0]
		EY2 = args[1]

		print ival
		print args

		nalpha = math.pow(ialpha, 2.0)*ibeta - math.pow(ibeta, 2.0)*ialpha - EY
		nbeta = (math.pow(ialpha, 2.0)/(ialpha - ibeta)) - ibeta - EY2/(2.0*EY)

		r = [nalpha, nbeta]

		print r

		return r

	@staticmethod
	def mmefit(points, **kwargs):
		"""
		Methods estimation for the double pareto distribution
		usage: DoublePareto.mmefit

		Input
		------
		points: Points on which to run the estimation
		**kwargs: Initial values
					alpha: Initial alpha value
					beta: Initial beta value

		Output
		-------
		Return value: Tuple (alpha, beta)
		"""

		pts = np.array(points)

		lpts = np.log(pts)

		EY = np.mean(lpts)
		EY2 = np.mean(np.power(lpts, 2.0))
		
		ialpha = 1.0
		ibeta = 1.0

		if "alpha" in kwargs:
			ialpha = float(kwargs["alpha"])
		if "beta" in kwargs:
			ibeta = float(kwargs["beta"])

		ivs = [ialpha, ibeta]
		ovs = (EY, EY2)

		fvals = opt.fsolve(DoublePareto.__solve_mme, ivs, ovs, None, 0, 0, 1e-12)

		return (fvals[0], fvals[1])
	
	@staticmethod
	def fromFit(points, **kwargs):
		"""
		Create a DoublePareto object with parameters estimated from points
		Usage: DoublePareto.fromFit(point)

		Input
		------
		points: points to estimate parameters for double pareto object
		**kwargs: Initial values
					alpha: Initial alpha value
					beta: Initial beta value

		Output
		------
		Return value: A DoublePareto object with alpha, beta estimated by mmefit
		"""

		(alpha, beta) = DoublePareto.mmefit(points, **kwargs)
		dp = DoublePareto(alpha, beta)

		return dp

	def __init__(self, alpha, beta):
		"""
		Constructor.

		Input
		------
		alpha, beta: Parameters for the distribution
		"""

		self.__alpha = alpha
		self.__beta = beta
	
	def alpha(self):
		""" Return the alpha-value """
		return self.__alpha

	def beta(self):
		""" Return the beta-value """
		return self.__beta
	
	def params(self):
		""" Return the alpha and beta values as a dict object """
		return {"alpha": self.__alpha, "beta": self.__beta}

	def pdf(self, points):
		""" 
		Return the density function for the points
		usage: Instance.pdf(points)

		Input
		------
		points: Set of points to return the pdf

		Output
		-------
		Return value: A numpy array with the corresponding density function
		"""

		p = []
		for x in points:
			if x <= 1.0:
				y = (self.__alpha*self.__beta/(self.__alpha+self.__beta))*math.pow(x, self.__beta-1)
			else:
				y = (self.__alpha*self.__beta/(self.__alpha+self.__beta))*math.pow(x, -self.__alpha-1)
			p.append(y)
		
		apdf = np.array(p)
		return apdf
	
	def cdf(self, points):
		"""
		Return the distribution function for the points
		usage: Instance.cdf(points)

		Input
		------
		points: Sef of points to return the cdf

		Output
		-------
		Return value: A numpy array with the corresponding cdf
		"""

		c = []

		for x in points:
			if x <= 1.0:
				y = (self.__alpha/(self.__alpha+self.__beta))*math.pow(x, self.__beta)
			else:
				y = (self.__beta/(self.__alpha+self.__beta))*(1 - math.pow(x, -self.__alpha))
			c.append(y)
		
		acdf = np.array(c)
		return acdf

	def ccdf(self, points):
		"""
		Return the complementary cdf for the points
		usage: Instance.ccdf(points)

		Input
		-----
		points: Set of points to compute the ccdf

		Output
		-------
		Return value: A numpy array with the corresponding ccdf
		"""

		accdf = 1 - self.cdf(points)
		return accdf

	def cdf_inv(self, points):
		"""
		Return the inverse of the cdf in points
		usage: Instance.cdf_inv(points)

		Input
		------
		points: 0 <= points <= 1

		Output
		-------
		Return value: A numpy array with the inverse of the cdf
		"""

		inv = []
		tpoint = self.__alpha/(self.__alpha + self.__beta)

		for y in points:
			if y <= tpoint:
				x = math.pow((self.__alpha + self.__beta)*y/self.__alpha, 1/self.__beta)
			else:
				x = math.pow(1 - ((self.__alpha + self.__beta)*y/self.__beta), -1/self.__alpha)
			inv.append(x)
		
		acdfinv = np.array(inv)

		return acdfinv

	def ccdf_inv(self, points):
		"""
		Return the inverse of the complmentary cdf in points
		usage: Instance.ccdf_inv(points)

		Input
		------
		points: 0 <= points <= 1

		Output
		------
		Return value: A numpy array with the inverse of the ccdf
		"""

		raise NotImplemented("ccdf_inv is currently not implemented")
	
	def rnd(self, n):
		"""
		Return n random variates of the Double Pareto distribution.
		usage: Instance.rnd(n)

		Input
		-----
		n: Number of random variates to generate

		Output
		------
		Return value: A numpy array with n random variates
		"""

		r = util.get_random()
		U = []
		for i in xrange(n):
			U.append(r.uniform(0,1))

		arnd = self.cdf_inv(U)

		return arnd


		


