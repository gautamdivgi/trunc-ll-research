import math as pm
import numpy as np
import scipy.optimize as opt
import random
import util

"""
The Truncated Pareto distribution
References:
1. I. B. Aban, M. M. Meerchaert and A. K. Panorska, Parameter Estimation for the Truncated Pareto distribution,
	Journal of the American Stat. Assoc., vol. 101, no. 473, pp. 270 -- 278, March 2006.

2. E. Chlebus and G. Divgi, The Pareto or the Truncated Pareto distribution? Measurement-based modeling of session
	traffic for Wi-Fi Wireless Internet Access, IEEE WCNC 2007.
"""


class TPareto:
	"""
	The truncated pareto class.
	Static methods
	--------------
	mlefit: Fit using maximum likelihood estimation to a set of points
	fromFit: Create a new TPareto class by estimating the parameters with MLE.	

	Instance methods	
	----------------
	pdf: Density function
	cdf: Distribution function
	ccdf: Complementary distribution function
	cdf_inv: Inverse distribution
	ccdf_inv: Inverse complementary distribution
	rnd: Random variates
	k: get the k-value
	m: get the m-value
	alpha: get the alpha-value
	"""

	# Static methods
	
	@staticmethod
	def mlefit(points, initial_alpha = 1.0):
		"""
		MLE fitting for the truncated pareto distribution.
		usage: TPareto.mlefit(points, [initial_alpha])
		Input
		-----
		points: Set of points to run MLE.
		initial_alpha: Initial value for alpha. The default is 1.0

		Output
		------
		Return values: Tuple (k, m, alpha)
		"""

		pts = np.array(points)

		k = float(pts.min())
		m = float(pts.max())
		n = float(len(pts))

		alpha = opt.fsolve(TPareto.__alpha_solver, initial_alpha, (pts, k, m, n), None, 0, 0, 1e-12)

		return (k, m, alpha)
	
	@staticmethod
	def __alpha_solver(ival, *args):
		"""
		Non-linear equation for solving alpha for the truncated pareto MLE. DO NOT CALL STANDALONE.
		ival: Initial alpha value from the mlefit function
		args[0]: The set of points
		args[1]: k
		args[2]: m
		args[3]: n - the number of points in args[0]
		Return value: New alpha value as invoked by the fsolve optimization.
		"""

		alpha = float(ival)
		x = args[0]
		xmin = args[1]
		xmax = args[2]
		n = args[3]

		t1 = n/alpha
		t2 = n*pm.pow((xmin/xmax),alpha)*pm.log(xmin/xmax)/(1 - pm.pow((xmin/xmax),alpha))
		t3 = np.sum(np.log(x) - pm.log(xmin))

		return t1 + t2 - t3
	
	@staticmethod
	def fromFit(points, initial_alpha = 1.0):
		"""
		Create a TPareto instance by estimating k, m and alpha using MLE
		Usage: fromFit(points, [initial_alpha])
		Input
		-----
		points: The set of points to estimate k, m and alpha
		initial_alpha: Initial estimate for alpha for MLE. The default is 1.0.

		Output:
		-------
		Return value: A TPareto instance with k, m and alpha estimated using mlefit
		"""

		(k, m, alpha) = TPareto.mlefit(points, initial_alpha)
		return TPareto(k, m, alpha)


	def __init__(self, k, m, alpha):
		"""
		Constructor
		Input
		-----
		k, m, alpha: Parameters for the truncated Pareto distribution
		"""
		self.__k = float(k)
		self.__m = float(m)
		self.__alpha = float(alpha)

	def k(self):
		""" Return the k-value of the distribution """
		return self.__k
	
	def m(self):
		""" Return the m-value of the distribution """
		return self.__m

	def alpha(self):
		""" Return the alpha value of the distribution """
		return self.__alpha
	
	def params(self):
		""" Return parameters as a dict object"""
		return {"k": self.__k, "m": self.__m, "alpha":self.__alpha}
	
	def pdf(self, points):
		""" 
		Return the probability density function for the TPareto
		Usage: Instance.pdf(points)
		Input
		-----
		points: Set of points (preferably sorted) to generate the density function

		Output
		------
		Return value: Numpy array of the density function
		"""

		pts = np.array(points)
		
		apdf = self.__alpha*pm.pow(self.__k, self.__alpha)*np.power(pts, -(self.__alpha+1))/(1 - pm.pow(self.__k/self.__m, 1))
		return apdf
	
	def cdf(self, points):
		"""
		Return the truncated pareto distribution function for a set of points
		Usage: Instance.cdf(points)
		Input
		-----
		points: Set of points (perferable sorted) to generate the density function

		Output
		------
		Return value: Numpy array of the distribution function
		"""

		pts = np.array(points)

		acdf = (1 - np.power(self.__k/pts, self.__alpha))/(1 - pm.pow(self.__k/self.__m, self.__alpha))
		return acdf
	
	def ccdf(self, points):
		"""
		Return the complementary distribution function for a set of points
		Usage: Instance.ccdf(points)
		Input
		-----
		ponts: Set of points (preferably sorted) to generate the complementary distribution function.

		Output
		------
		Return value: Numpy arry of the complementary distribution function
		"""

		return 1 - self.cdf(points)
	
	def cdf_inv(self, points):
		"""
		Return the inverse of the CDF specified in points
		Usage: Instance.cdf_inv(points)
		Input
		-----
		points: Set of points 0 <= points[i] <= 1.

		Output
		------
		The inverse of the CDF that points[i] represent. 
		"""
		
		pts = np.array(points)
		t1 = 1 - pm.pow(self.__k/self.__m, self.__alpha)
		t2 = 1 - pts*t1
		t3 = np.power(t2, 1/self.__alpha)
		ainv = self.__k/t3

		return ainv

	def ccdf_inv(self, points):
		"""
		Return the inverse of the CCDF specified in points
		Usage: Instance.ccdf_inv(points)
		Input
		-----
		points: Set of points 0 <= points[i] <=1.

		Output
		------
		The inverse of the CCDF that points[i] represent.
		"""

		pts = np.array(points)
		t1 = pts - (pts-1)*pm.pow(self.__k/self.__m, self.__alpha)
		t2 = np.power(t1, 1/self.__alpha)
		ainv = self.__k/t2

		return ainv
	
	def rnd(self, n):
		"""
		Return an array of random variates for the truncated pareto distribution
		Usage: Instance.rnd(n)
		Input
		-----
		n: The number of variates needed

		Output
		------
		Return value: Numpy array with n TPareto variates
		"""

		r = util.get_random()

		lb = pm.pow(self.__k/self.__m, self.__alpha)/(1 + pm.pow(self.__k/self.__m, self.__alpha))
		ub = 1/(1 + pm.pow(self.__k/self.__m, self.__alpha))

		l = []
		for i in xrange(n):
			l.append(r.uniform(lb, ub))
		
		lp = np.array(l)

		k1 = self.__k/pm.pow((1 + pm.pow(self.__k/self.__m, self.__alpha)), 1/self.__alpha)
		arnd = k1*np.power(lp, -1/self.__alpha)

		return arnd

	def ksmetric(self, **kwargs):
		"""
		Return the ks metris for truncated pareto
		Input:
		**kwargs:
			points = [set of points]
			-or-
			cdf = [Precomputed cdf]

		Output:
			KS metric
		"""

		c = None
		if "cdf" in kwargs:
			c = kwargs["cdf"]
		else:
			p = kwargs["points"]
			p.sort()
			c = util.ecdf(p, issorted=True)
		
		y = self.cdf(c[:,0])
		return util.kstest(c[:,1],c[:,2],y)

	def fitmetric(self, **kwargs):
		"""
		Return the FIT metric for truncated pareto
		Input:
		**kwargs:
			points = [set of points]
			-or-
			cdf = [Precomputed cdf]

		Output:
			FIT metric
		"""

		c = None
		if "cdf" in kwargs:
			c = kwargs["cdf"]
		else:
			p = kwargs["points"]
			p.sort()
			c = util.ecdf(p, issorted=True)
		
		xi = c[:,0]
		x_hat_i = self.cdf_inv(c[:,1])
		return util.fitmetric(xi, x_hat_i, c[:,1])

