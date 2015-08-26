import util
import numpy as np
import math
import scipy.special as spec
import scipy.constants as const
import scipy.optimize as opt

"""
The Lognormal distribution
References:
1. A. M. Law and W. D. Kelton, Simulation, Modeling and Analysis, 3rd edition, McGraw-Hill
"""

class LognormalConvergenceError(Exception):
	def __init__(self, mesg, values):
		self.__mesg = mesg
		self.__mu = values[0]
		self.__sigma = values[1]

	def __str__(self):
		prms = {"mu": self.__mu, "sigma": self.__sigma}
		return self.__mesg + " use the following to verify manually - " + str(prms)

	def __repr__(self):
		prms = {"mu": self.__mu, "sigma": self.__sigma}
		return self.__mesg + " use the following to verify manually - " + str(prms)

	def mu(self):
		return self.__mu

	def sigma(self):
		return self.__sigma

class Lognormal:
	"""
	The lognormal distribution Lognormal(mu, sigma^2)

	Static methods
	--------------
	mlefit: ML estimation from a set of points
	mmefit: Moments estimation from a set of points
	fromFit: Create a new Lognormal instance using either the mmefit 
				or the mmefit from a set of points
	
	Instance methods
	-----------------
	pdf: Density function
	cdf: Distribution function
	ccdf: Complementary distribution function
	cdf_inv: Inverse distribution
	ccdf_inv: Inverse complementary distribution
	rnd: Random variates
	mu: Get the mu-value
	sigma: Get the sigma value. The parameter is actually sigma^2
	"""

	@staticmethod
	def mlefit(points):
		"""
		MLE fitting to the Lognormal distribution for the set of points.
		usage: Lognormal.mlefit(points)

		Input
		------
		points: Set of points to run the estimation

		Output
		------
		Return value: Tuple (mu, sigma)
		"""

		pts = np.array(points)
		n = float(len(pts))
		rootn = math.sqrt(n)

		mu = np.sum(np.log(pts))/n
		
		# Dividing by root(n) at each step instead of at the end to keep
		# the individual sums as small as possible.
		sigmasq = np.sum(np.power((np.log(pts) - mu)/rootn, 2))

		sigma = math.sqrt(sigmasq)

		return (mu, sigma)

	@staticmethod
	def mmefit(points):
		"""
		Methods estimation fitting to the Lognormal distribution for the set of points.
		usage: Lognormal.mmefit(points)

		Input
		------
		points: Set of points to run the estimation

		Output
		------
		Return value: Tuple (mu, sigma)
		"""

		pts = np.array(points)
		n = float(len(pts))

		ex = pts.mean()
		varx = pts.var()

		sigma = math.sqrt(math.log(varx + math.pow(ex, 2)) - 2*math.log(ex))
		mu = math.log(ex) - (math.pow(sigma, 2)/2.0)

		return (mu, sigma)

	@staticmethod
	def fromFit(points, mmefit=True, fitmin=False):
		"""
		Create a Lognormal object with the parameters estimated from points using either
		the mmefit or the mlefit. The default is the mmefit since it is the fit used in
		most papers.
		usage: Lognormal.fromFit(points, [mmefit = True|False])

		Input
		------
		points: Set of points to estimate parameters
		mmefit: optional. True by default. If false, the parameters are estimated using mlefit
		fitmin: disregard mmefit, use the fitmin

		Output
		------
		Return value: A Lognormal object with the parameters mu and sigma esitmated by the fit functions
		"""
		if ( fitmin == True ):
			(mu, sigma) = Lognormal.fitmin(points, mmefit)
		else:
			if ( mmefit == True ):
				(mu, sigma) = Lognormal.mmefit(points)
			else:
				(mu, sigma) = Lognormal.mlefit(points)

		lgn = Lognormal(mu, sigma)

		return lgn

	@staticmethod
	def __ki(ai):
		return math.sqrt(2.0)*spec.erfinv(2.0*ai-1.0)

	@staticmethod
	def __solve_fitmin(ival, *args):
		imu = ival[0]
		isig = ival[1]
		
		ki = args[0]
		xi2 = args[1]
		sqrt2 = args[2]

		nmu = np.sum(-1.0 * xi2 * np.exp(-isig*ki-imu) + np.exp(isig*ki+imu))
		nsig = np.sum(-1.0 * xi2 * ki * np.exp(-isig*ki-imu) + ki * np.exp(ki*isig+imu))

		return [nmu, nsig]

	@staticmethod
	def fitmin(pts, mmefit):
		x = np.array(pts)

		ec = util.ecdf(x)
		xi = ec[:,0]
		ai = ec[:,1]
		
		if mmefit == True:
			(imu, isig) = Lognormal.mmefit(x)
		else:
			(imu, isig) = Lognormal.mlefit(x)

		sqrt2 = math.sqrt(2)
		xi2 = xi**2.0
		ki = Lognormal.__ki(ai)

		ivs = [imu, isig]
		ovs = (ki, xi2, sqrt2)

		(fvals, infodict, ier, mesg) = opt.fsolve(Lognormal.__solve_fitmin, ivs, ovs, None, 1, 0)
	
		f_mu = fvals[0]
		f_sig = fvals[1]

		if ier != 1:
			raise LognormalConvergenceError(mesg, (f_mu, f_sig))
		
		return (f_mu, f_sig)
			

	def __init__(self, mu, sigma):
		"""
		Constructor.

		Input
		------
		mu, sigma: Parameters for the lognormal distribution
		"""
		self.__mu = float(mu)
		self.__sigma = float(sigma)

		# Storing sigmasq locally since it is used most often
		self.__sigmasq = math.pow(self.__sigma, 2)

	def mu(self):
		""" Return the mu value for the distribution """
		return self.__mu
	
	def sigma(self):
		""" Return the sigma value for the distribution """
		return self.__sigma

	def params(self):
		""" Return mu and sigma as a dict object """
		return {"mu": self.__mu, "sigma": self.__sigma}
	
	def pdf(self, points):
		"""
		Return the density function for the set of points
		usage: Instance.pdf(points)

		Input
		-----
		points: Set of points to compute the pdf

		Output
		------
		Return value: Numpy array with the corresponding pdf
		"""
		
		pts = np.array(points)

		t1 = 1.0/(self.__sigma * math.sqrt(2*const.pi) * pts)
		t2 = -np.power(np.log(pts) - self.__mu, 2)/(2*self.__sigmasq)
		apdf = t1*np.exp(t2)
	
	def cdf(self, points):
		"""
		Return the distribution function for the set of points
		usage: Instance.cdf(points)

		Input
		-----
		points: Set of points to compute the cdf

		Output
		------
		Return value: Numpy array with the corresponding cdf
		"""

		pts = np.array(points)
		acdf = 0.5 * (1 + spec.erf( (np.log(pts) - self.__mu)/(self.__sigma*math.sqrt(2.0)) ))
		return acdf

	def ccdf(self, points):
		"""
		Return the complementary distribution function for the set of points
		usage: Instance.ccdf(points)

		Input
		-----
		points: set of points to compute the ccdf

		Output
		------
		Return value: Numpy array with the corresponding ccdf
		"""

		pts = np.array(points)
		accdf = 0.5 * (1 - spec.erf( (np.log(pts) - self.__mu)/(self.__sigma*math.sqrt(2.0)) ))
		return accdf
	
	def cdf_inv(self, points):
		"""
		Return the inverse cdf of the points
		usage: Instance.cdf_inv(points)

		Input
		------
		points: 0 <= points[i] <= 1

		Output
		-------
		Return value: Numpy array which is the inverse of the cdf
		"""

		pts = np.array(points)
		acdfinv = np.exp(self.__mu + self.__sigma*math.sqrt(2.0)*spec.erfinv(2*pts - 1))
		return acdfinv

	def ccdf_inv(self, points):
		"""
		Return the inverse ccdf of the points
		usage: Instance.ccdf_inv(points)

		Input
		-----
		points: 0 <= points[i] <= 1

		Output
		Return value: Numpy array which is the inverse of the ccdf
		"""

		pts = np.array(points)
		accdfinv = np.exp(self.__mu + self.__sigma*math.sqrt(2.0)*spec.erfinv(1 - 2*pts))
		return accdfinv

	def rnd(self, n):
		"""
		Return an array of Lognormal random variates
		usage: Instance.rnd(n)

		Input
		------
		n: The number of variates

		Output
		------
		Return value: A numpy array with the random variates
		"""

		r = util.get_random()

		l = []

		for i in xrange(n):
			l.append(r.gauss(0, 1))
		
		lp = np.array(l)

		arnd = np.exp(self.__mu + self.__sigma*lp)
		return arnd

	def ksmetric(self, **kwargs):
		"""
		Return the kolmogorov-smirnov metric for lognormal
		Input:
		**kwargs:
			points = [set of points to compute the cdf]
			-or-
			cdf = [Already computed cdf]

		Output:
			ks metric
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
		Return the fit metric for lognormal
		Input:
		**kwargs:
			points = [set of points to compute the cdf]
			-or-
			cdf = [Already computed cdf]
		
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
	
	def difference(self, **kwargs):
		"""
		Return the difference metric for lognormal
		Input:
		**kwargs:
			points = [set of points to compute the cdf]
			-or-
			cdf = [Already computed cdf]
		
		Output:
			Difference metric
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
		return 1 - util.chlebus_divgi_sim_fitmetric(xi, x_hat_i, c[:,1])
	
	def __str__(self):
		return str(self.params())
	
	def __repr__(self):
		return str(self.params())

