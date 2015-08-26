import random
import numpy as np
import util
import math

"""
The modified truncated pareto distribution. A special case with for TPareto(k, m, alpha), alpha is approx. 0
References:
1. E. Chlebus and G. Divgi, The Pareto or truncated Pareto distribution? Measurement-based modeling of session
	traffic for Wi-Fi wireless Internet Access, IEEE WCNC 2007
"""

class MTPareto:
	"""
	The modified truncated pareto class.
	Static methods
	--------------
	fit: There is no MLE/MME for this distribution. There are 2 parameters that are trivially derived.
		  The fit method uses the min and the max from the data set and returns them.
	fromFit: Create a MTPareto object from the parameters returned by fit

	Instance methods
	-----------------
	pdf: Density function
	cdf: Distribution function
	ccdf: Complementary distribution function
	cdf_inv: Inverse CDF function
	ccdf_inv: Inverse CCDF function
	rnd: Generate random variates
	k: get the k-value [xmin]
	m: get the m-value [xmax]
	"""

	# static methods
	@staticmethod
	def fit(points):
		"""
		Return the min and the max of the values in points. These are the distributions parameters.
		usage: MTPareto.fit(points)

		Input
		-----
		points: A set of points.

		Output
		------
		Return value: k, m values for the set of points. k = min(points), m = max(points)
		"""

		pts = np.array(points)
		k = pts.min()
		m = pts.max()

		return (k, m)
	
	@staticmethod
	def fromFit(points):
		"""
		Return a MTPareto instance with parameters k, m estimated by MTPareto.fit
		usage: MTPareto.fromFit(points)

		Input
		------
		points: A set of points

		Output
		------
		Return value: A MTPareto instance with parameters k, m estimated.
		"""

		(k, m) = MTPareto.fit(points)
		return MTPareto(k, m)
	
	def __init__(self, k, m):
		"""
		Constructor

		Input
		------
		k, m: Parameters for the distribution
		"""

		self.__k = float(k)
		self.__m = float(m)

	def k(self):
		""" Return the k-value """
		return self.__k

	def m(self):
		""" Return the m-value """
		return self.__m

	def params(self):
		""" Return the params as a dict object """
		return {"k": self.__k, "m": self.__m}

	def pdf(self, points):
		"""
		Return the probability density function for MTPareto
		Usage: Instance.pdf(points)

		Input
		-----
		points: Set of points (preferably sorted) to generate the density function

		Output
		------
		Return value: A Numpy array with the corresponding pdf values
		"""
		pts = np.array(points)
		apdf = 1/(pts * math.log(self.__m/self.__k))

		return apdf
	
	def cdf(self, points):
		"""
		Return the distribution for the MTPareto
		Usage: Instance.cdf(points)

		Input
		-----
		points: Set of points (preferably sorted) to generate the distribution function

		Output
		------
		Return value: A numpy array with the corresponding cdf values
		"""

		pts = np.array(points)
		acdf = np.log(pts/self.__k)/math.log(self.__m/self.__k)
		return acdf

	def ccdf(self, points):
		"""
		Return the complementary distribution for the MTPareto distribution
		Usage: Instance.ccdf(points)

		Input
		------
		points: Set of points (preferably sorted) to generate the CCDF

		Output
		------
		Return value: A numpy array with the corresponding CCDF values
		"""

		accdf =  1 - self.cdf(points)
		return accdf

	def cdf_inv(self, points):
		"""
		Return the inverse CDF of points.
		Usage: Instance.cdf_inv(points)

		Input
		------
		points: 0 <= points[i] <= 1

		Output
		-------
		Return value: A numpy array with the corresponding inverse CDF
		"""
		
		pts = np.array(points)
		acdfinv = self.__k*np.power(self.__m/self.__k, pts)
		return acdfinv
	
	def ccdf_inv(self, points):
		"""
		Return the inverse CCDF of points.
		Usage: Instance.ccdf_inv(points)

		Input
		------
		points: 0 <= points[i] <= 1

		Output
		-------
		Return value: A numpy array with the corresponding inverse CCDF
		"""

		pts = np.array(points)
		accdfinv = self.__k*np.power(self.__m/self.__k, 1 - pts)
		return accdfinv
	
	def rnd(self, n):
		"""
		Return random variates for the MTPareto distribution
		Usage: Instance.rnd(n)

		Input
		------
		n: Number of random variates to return

		Output
		-------
		Return value: A numpy array with MTPareto random variates
		"""

		r = util.get_random()
		l = []
		for i in xrange(n):
			l.append(r.uniform(0,1))
		
		lp = np.array(l)

		arnd = self.__k*np.power(self.__m/self.__k, lp)

		return arnd
