import math as pm
import numpy as np
import random
import util

"""
The pareto distribution
References:
1. M. Rytgaard, Estimation in the Pareto distribution, ASTIN Bulletin, vol. 20, no. 2. 1990, pp 201 -- 216
2. V. Brazauskas and R. Serfling, Favorable estimators for fitting Pareto models: A study using goodness-of-fit
	measures with actual data, ASTIN Bulletin, vol. 33, no. 2, 2003, pp. 365 -- 381
"""

class Pareto:
	"""
	The pareto distribution Pareto(alpha, k)
	
	Static methods
	--------------
	mlefit: Return MLE parameters k and alpha for the set of points
	fromFit: Create a new Pareto class by estimating the parameters with MLE.

	Instance methods
	----------------
	pdf: Density function
	cdf: Distribution function
	ccdf: Complementary Distribution function
	cdf_inv: Inverse CDF
	ccdf_inv: Inverse CCDF
	rnd: Random variates
	k: get the k-value
	alpha: get the alpha-value
	"""

	@staticmethod
	def mlefit(points):
		"""
		MLE fitting for the Pareto distribution for the set of points.
		usage: Pareto.mlefit(points)

		Input
		------
		points: Set of points to run MLE.

		Output
		------
		Return value: Tuple (k, alpha)
		"""

		pts = np.array(points)

		k = float(pts.min())
		n = float(len(pts))

		alpha = (n - 1)/np.sum(np.log(pts/k))

		return (k, alpha)

	@staticmethod
	def mmefit(points):
		"""
		Moments estimation for the Pareto distribution from the mean(points).
		usage: Pareto.mmefit(points)

		Input
		-----
		points: Set of points to run the moments estimation

		Output
		------
		Return value: Tuple (k, alpha)
		"""

		pts = np.array(points)

		k = float(pts.min())
		EX = np.mean(pts)
		
		# For a heavy tailed distribution k << EX
		# So, alpha approx. equal to 1
		alpha = EX/(EX-k)

		return (k, alpha)

	@staticmethod
	def fromFit(points, mlefit=True):
		"""
		Create a Pareto object with parameters estimated from points.
		usage: Pareto.fromFit(points)

		Input
		-----
		points: Set of points to estimate parameters

		Output
		------
		Return value: Pareto object with parameters estimated using Pareto.mlefit(points)
		"""
		p = None

		if mlefit == True:
			p = Pareto.mlefit(points)
		else:
			p = Pareto.mmefit(points)

		return Pareto(p[0], p[1])

	def __init__(self, k, alpha):
		"""
		Constructor

		Input
		-------
		k, alpha: Parameters for the Pareto distribution
		"""
		
		self.__k = float(k)
		self.__alpha = float(alpha)
	
	def k(self):
		"""
		Return the k-value of the distribution
		"""
		return self.__k
	
	def alpha(self):
		"""
		Return the alpha-value of the distribution
		"""
		return self.__alpha
	
	def params(self):
		"""
		Return the k and alpha values as a dict object
		"""
		return {"k": self.__k, "alpha": self.__alpha}

	def pdf(self, points):
		"""
		Return the density function for the points.
		Usage: Instance.pdf(points)

		Input
		-----
		points: The set of points to compute the density values.

		Output
		-----
		Return value: Numpy array with the density values.
		"""

		pts = np.array(points)

		apdf = self.__alpha * pm.pow(self.__k, self.__alpha) * np.power(pts, -(self.__alpha + 1.0))

		return apdf

	def cdf(self, points):
		"""
		Return the distribution function.
		Usage: Instance.cdf(points)

		Input
		------
		points: The set of points (preferable sorted) to compute the distribution function.

		Output
		------
		Return value: Numpy array with the distribution function for the points.
		"""

		pts = np.array(points)

		acdf = 1 - np.power(self.__k/pts, self.__alpha)

		return acdf

	def cdf_inv(self, points):
		"""
		Return the inverse CDF for the distribution specified in points.
		Usage: Instance.cdf_inv(points)

		Input
		------
		points: 0 <= points[i] <= 1.

		Output
		------
		Return value: Inverse distribution of the points.
		"""

		pts = np.array(points)

		acdfinv = self.__k/np.power((1 - pts), 1/self.__alpha)

		return acdfinv
	
	def ccdf(self, points):
		"""
		Return the complementary distribution function
		Usage: Instance.ccdf(points)

		Input
		-----
		points: Array on which to compute the Pareto ccdf

		Output
		------
		Return value: Numpy array with the Pareto CCDF of points
		"""

		accdf = 1 - self.cdf(points)

		return accdf
	
	def ccdf_inv(self, points):
		"""
		Return the CCDF inverse function for the points
		Usage: Instance.ccdf_inv(points)

		Input
		-----
		points: 0 <= points[i] <= 1

		Output
		------
		Return value: Numpy array with the Pareto CCDF inverse function for points
		"""

		pts = np.array(points)
		accdfinv = self.__k/np.power(pts, 1/self.__alpha)

		return accdfinv
	
	def rnd(self, n):
		"""
		Return an array of Pareto random variates
		Usage: Instance.rnd(n)

		Input
		------
		n: The number of random variates to return

		Output
		------
		Return value: Numpy array of Pareto random variates
		"""

		r = util.get_random()
		l = []
		for i in xrange(n):
			l.append(r.uniform(0, 1))

		lp = np.array(l)

		arnd = self.__k/np.power(lp, 1/self.__alpha)

		return arnd


		
