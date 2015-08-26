import numpy as np
import scipy.optimize as opt
import scipy as sp
import util
import math

"""
The biPareto distribution
References:
1. C. Nuzman, I. Saniee, W. Sweldens and A. Weiss, A compound model for TCP connection arrivals for LAN and WAN applications, 
	Computer Networks, vol. 40, no. 3, Oct. 2002, pp. 319 -- 337
Note: THE FORMULAE IN THE ABOVE PAPER FOR THE BiPareto OPTIMIZATION ARE INCORRECT. THESE FORMULAE BELOW ARE COMPUTED BY HAND.
"""

class BiPareto:
	"""
	The biPareto distribution biPareto(alpha, beta, c, k)

	Static methods
	---------------
	mlefit: ML estimation from a set of points
	fromFit: Create a new BiPareto object from parameters estimated by mlefit

	Instance method
	---------------
	pdf: Density function
	cdf: Distribution function
	ccdf: Complementary distribution function
	cdf_inv: Inverse of the distribution function
	ccdf_inv: Inverse of the complementary distribution function
	rnd: Random variates
	alpha: return the alpha-value
	beta: return the beta-value
	c: return the c-value
	k: return the k-value
	"""
	
	@staticmethod
	def __ddc(pts, alpha, beta, gamma):
		""" 
		Non-linear equation dL/d(gamma)
		pts: Set of points
		alpha, beta, gamma: values for that iteration.
		Internal to the MLE solver. DO NOT CALL STANDALONE.
		"""
		
		try:
			n = float(len(pts))
			e_g = math.exp(gamma)

			t1 = (beta - alpha)/(1 + e_g)
			t2 = (alpha - beta -1)/(pts + e_g)
			t3 = alpha/(beta*pts + alpha*e_g)
		except:
			print alpha
			print beta
			print gamma
			raise

		r = np.sum(t1 + t2 + t3)
		return r
	
	@staticmethod
	def __ddalpha(pts, alpha, beta, gamma):
		""" 
		Non-linear equation dL/d(alpha)
		pts: Set of points
		alpha, beta, gamma, u: values for that iteration.
		Internal to the MLE solver. DO NOT CALL STANDALONE.
		"""
		
		try:
			n = float(len(pts))
			e_g = math.exp(gamma)

			t1 = -math.log(1 + e_g)
			t2 = -np.log(pts)
			t3 = np.log(pts + e_g)
			t4 = e_g/(beta*pts + alpha*e_g)
		except:
			print alpha
			print beta
			print gamma
			raise

		r = np.sum(t1 + t2 + t3 + t4)
		return r

	@staticmethod
	def __ddbeta(pts, alpha, beta, gamma):
		""" 
		Non-linear equation dL/d(beta)
		pts: Set of points
		alpha, beta, gamma: values for that iteration.
		Internal to the MLE solver. DO NOT CALL STANDALONE.
		"""

		try:
			n = float(len(pts))	
			e_g = math.exp(gamma)
		
			t1 = math.log(1 + e_g)
			t2 = -np.log(pts + e_g)
			t3 = pts/(beta*pts + alpha*e_g)
		except:
			print alpha
			print beta
			print gamma
			raise

		r = np.sum(t1 + t2 + t3)
		return r

	@staticmethod
	def __d2dalpha2(pts, alpha, beta, gamma):
		"""
		Non-linear equation for d^L/dalpha^2
		pts: Set of points
		alpha, beta, gamma: values for that iteration
		Internal to the MLE solver. DO NOT CALL STANDALONE
		"""

		try:
			e_g = math.exp(gamma)
			t = -alpha*math.pow(e_g, 2.0)/np.power((beta*pts + alpha*e_g), 2.0)
		except:
			print alpha
			print beta
			print gamma
			raise

		r = np.sum(t)
		return r

	@staticmethod
	def __d2dalphabeta(pts, alpha, beta, gamma):
		"""
		Non-linear equation for d^2/dalpha-beta
		pts: Set of points
		alpha, beta, gamma: values for that iteration
		Internal to the MLE solver. DO NOT CALL STANDALONE
		"""

		try:
			e_g = math.exp(gamma)
			t = -e_g*pts/np.power((beta*pts + alpha*e_g), 2.0)
		except:
			print alpha
			print beta
			print gamma
			raise
		
		r = np.sum(t)
		return r
	
	@staticmethod
	def __d2dalphac(pts, alpha, beta, gamma):
		"""
		Non-linear equation for d^2/dalpha-c
		pts: Set of points
		alpha, beta, gamma: values for that iteration
		Internal to the MLE solver. DO NOT CALL STANDALONE
		"""
		try:
			e_g = math.exp(gamma)
			t = -1.0/(1 + e_g) + 1.0/(pts + e_g) + beta*pts/np.power(beta*pts + alpha*e_g, 2.0)
		except:
			print alpha
			print beta
			print gamma
			raise
	
		r = np.sum(t)
		return r

	@staticmethod
	def __d2dbeta2(pts, alpha, beta, gamma):
		"""
		Non-linear equation for d^2/dbeta^2
		pts: Set of points
		alpha, beta, gamma: values for that iteration
		Internal to the MLE solver. DO NOT CALL STANDALONE
		"""
		try:
			e_g = math.exp(gamma)
			t = -np.power(pts, 2.0)/np.power(beta*pts + alpha*e_g, 2.0)
		except:
			print alpha
			print beta
			print gamma
			raise
		
		r = np.sum(t)
		return r

	@staticmethod
	def __d2dbetac(pts, alpha, beta, gamma):
		"""
		Non-linear equation for d^2/dbeta-c
		pts: Set of points
		alpha, beta, gamma: values for that iteration
		Internal to the MLE solver. DO NOT CALL STANDALONE
		"""
		try:
			e_g = math.exp(gamma)
			t = 1.0/(1 + e_g) - 1.0/(pts + e_g) - alpha*pts/np.power(beta*pts + alpha*e_g, 2.0)
		except:
			print alpha
			print beta
			print gamma
			raise
		
		r = np.sum(t)
		return r
	
	@staticmethod
	def __d2dc2(pts, alpha, beta, gamma):
		"""
		Non-linear equation for d^2/dc2
		pts: Set of points
		alpha, beta, gamma: values for that iteration
		Internal to the MLE solver. DO NOT CALL STANDALONE
		"""
		try:
			e_g = math.exp(gamma)
			t1 = -(beta-alpha)/math.pow(1+e_g,2.0) 
			t2 = -(alpha-beta-1)/np.power(pts + e_g, 2.0) 
			t3 = -math.pow(alpha,2.0)*e_g/np.power(beta*pts + alpha*e_g, 2.0)
		except:
			print alpha
			print beta
			print gamma
			raise
	
		r = np.sum(t1 + t2 + t3)
		return r

	@staticmethod
	def __solve_bipareto_mle(ival, *args):
		"""
		Bipareto MLE solver to solve alpha, beta, gamma. DO NOT CALL STANDALONE.
		ival: Initial values
			[0] = alpha
			[1] = beta
			[2] = gamma. gamma = log(c)
		*args: Other arguments
			[0] = set of points
		Return value: New alpha, beta, gamma values
		"""

		pts = args[0]

		print len(ival)

		ialpha = ival[0]
		ibeta = ival[1]
		igamma = ival[2]
		ialpha2 = ival[3]
		ialphabeta = ival[4]
		ialphac = ival[5]
		ibeta2 = ival[6]
		ibetac = ival[7]
		ic2 = ival[8]

		# print "Entry:", alpha, beta, gamma

		nalpha = BiPareto.__ddalpha(pts, ialpha, ibeta, igamma)
		nbeta = BiPareto.__ddbeta(pts, ialpha, ibeta, igamma)
		ngamma = BiPareto.__ddc(pts, ialpha, ibeta, igamma)
		nalpha2 = BiPareto.__d2dalpha2(pts, ialpha, ibeta, igamma)
		nalphabeta = BiPareto.__d2dalphabeta(pts, ialpha, ibeta, igamma)
		nalphac = BiPareto.__d2dalphac(pts, ialpha, ibeta, igamma)
		nbeta2 = BiPareto.__d2dbeta2(pts, ialpha, ibeta, igamma)
		nbetac = BiPareto.__d2dbetac(pts, ialpha, ibeta, igamma)
		nc2 = BiPareto.__d2dc2(pts, ialpha, ibeta, igamma)

		
		# print "Exit:", nalpha, nbeta, ngamma

		return [nalpha, nbeta, ngamma, nalpha2, nalphabeta, nalphac, nbeta2, nbetac, nc2]
		# return [nalpha, nbeta, ngamma]
	
	@staticmethod
	def mlefit(points, **kwargs):
		"""
		MLE fitting for the BiPareto distribution.
		usage: BiPareto.mlefit(points, alpha=, beta=, c=)

		Input
		------
		points: Set of points with which to run the estimation
		*kwargs: Initial values
			alpha = initial alpha value
			beta = initial beta value
			c = initial c value
			The following rules must hold
			beta > 0, c >= 0 and alpha >= -beta/c
		
		Output
		------
		Return value: Tuple (alpha, beta, c, k)
		"""

		pts = np.array(points)
		k = float(pts.min())

		pts1 = pts/k

		initial_values = [kwargs["alpha"], kwargs["beta"], math.log(kwargs["c"]), 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
		# initial_values = [kwargs["alpha"], kwargs["beta"], math.log(kwargs["c"])]
		other_args = (pts1)

		(r1, infodict, ier, mesg) = opt.fsolve(BiPareto.__solve_bipareto_mle, initial_values, other_args, None, 1, 0, 1e-12,maxfev=3000)
		
		if ier != 1:
			prms = {"alpha": r1[0], "beta": r1[1], "c": math.exp(r1[2]), "k": k}
			raise RuntimeError(mesg + " use the following parameters to verify manually - " + str(prms))

		alpha = r1[0]
		beta = r1[1]
		c = math.exp(r1[2])

		return (alpha, beta, c, k)

	@staticmethod
	def fromFit(points, **kwargs):
		"""
		Create a new BiPareto object with parameters estimated from mlefit for the set of points
		usage: BiPareto.fromFit(points, alpha=, beta=, c=)

		Input
		------
		points: Set of points with which to run the estimation
		*kwargs: Initial values
			alpha = initial alpha value
			beta = initial beta value
			c = initial c value
			The following rules must hold
			beta > 0, c >= 0 and alpha >= -beta/c
		
		Output
		-------
		Return value: BiPareto instance with parameters alpha, beta, c, k estimated from points
		"""

		(alpha, beta, c, k) = BiPareto.mlefit(points, **kwargs)
		bp = BiPareto(alpha, beta, c, k)

		return bp
	
	def __init__(self, alpha, beta, c, k):
		"""
		Constructor.
		Input
		------
		alpha, beta, c, k: Input parameters for the BiPareto distribution
		"""
		self.__alpha = float(alpha)
		self.__beta = float(beta)
		self.__c = float(c)
		self.__k = float(k)
	
	def alpha(self):
		""" Return the alpha value for the distribution """
		return self.__alpha
	
	def beta(self):
		""" Return the beta value for the distribution """
		return self.__beta
	
	def c(self):
		""" Return the c value for the distribution """
		return self.__c

	def k(self):
		""" Return the k value for the distribution """
		return self.__k
	
	def params(self):
		""" Return the parameters as a dict object """
		return {"alpha": self.__alpha, "beta": self.__beta, "c": self.__c, "k": self.__k}
	
	def pdf(self, points):
		"""
		Return the density function for the BiPareto distribution.
		Usage: Instance.pdf(points)

		Input
		-----
		points: Array of points to compute the pdf

		Output
		------
		Return value: A numpy array with the corresponding pdf
		"""

		pts = np.array(points)
		
		t1 = math.pow(self.__k, self.__beta)*math.pow(1 + self.__c, self.__beta - self.__alpha)
		t2 = np.power(pts, -self.__alpha-1)*np.power(pts + self.__k*self.__c, self.__alpha-self.__beta-1)
		t3 = self.__beta*pts + self.__alpha*self.__k*self.__c

		apdf = t1*t2*t3

		return apf

	def cdf(self, points):
		"""
		Return the distribution function for the BiPareto distribution.
		Usage: Instance.cdf(points)

		Input
		------
		points: Array of points to compute the cdf

		Output
		------
		Return value: A numpy array with the corresponding cdf
		"""

		pts = np.array(points)

		acdf = 1 - np.power(pts/self.__k, -self.__alpha)*np.power( ((pts/self.__k)+self.__c)/(1+self.__c), self.__alpha-self.__beta)

		return acdf

	def ccdf(self, points):
		"""
		Return the complementary distribution function for the BiPareto distribution
		Usage: Instance.ccdf(points)

		Input
		-----
		points: Array of points to compute the complementary distribution function

		Output
		------
		Return value: A numpy array with the corresponding ccdf
		"""

		accdf = 1 - self.cdf(points)
		return accdf

	@staticmethod
	def __solve_inv(ival, *args):
		"""
		Solver for the inverse cdf or ccdf non-linear equation.
		ival: Initial values
			[0]: The initial x-value
		*args: optional arguments
			[0]: alpha (a)
			[1]: beta (b)
			[2]: c (c)
			[3]: k (k)
			[4]: y - the cdf or ccdf value
			[5]: True - cdf, False - ccdf
		
		DO NOT CALL STANDALONE
		"""

		x = float(ival)
		
		a = args[0]
		b = args[1]
		c = args[2]
		k = args[3]
		y = args[4]
		cdf = args[5]
		
		try:
			r = math.pow(x/k, -a)*math.pow(((x/k)+c)/(1+c), a-b) - y
		except:
			print x
			print a
			print b
			print c
			print k
			print y
			raise
		if cdf == True:
			r = 1 - r
		return r

	def __ccdf_cdf_inv(self, points, cdf=True):
		"""
		Return the inverse of the distribution or complementary distribution function
		Usage: Instance.__ccdf_cdf_inv(points)

		Input
		------
		points: 0 <= points <= 1

		Output
		-------
		Return value: A numpy array with the corresponding inverse values
		"""

		pts = np.array(points)
		inv = []

		for pt in pts:
			optional_args = (self.__alpha, self.__beta, self.__c, self.__k, pt, cdf)
			inv_pt = opt.fsolve(BiPareto.__solve_inv, self.__k, optional_args, None, 0, 0, 1e-12)
			inv.append(inv_pt)
		
		ainv = np.array(cdfinv)
		
		return ainv
	
	def cdf_inv(self, points):
		"""
		Return the inverse of the distribution function
		Usage: Instance.ccdf_inv(points)

		Input
		------
		points: 0 <= points <= 1

		Output
		-------
		Return value: A numpy array with the corresponding inverse values

		Based on the algorithm by Lingsong Zhang & Haipeng Shen - UNC - CH.
		"""
		fylo = self.__k
		fyhi = 1e12
		fxlo = 0.0
		fxhi = self.cdf(fyhi)

		pts = np.array(points)
		cdfinv = []

		for pt in pts:
			if pt < fxlo:
				msg = "Value " + str(pt) + " is too small"
				raise ValueError(msg)
			elif pt > fxhi:
				msg = "Value " + str(pt) + " is outside the seeking range of 0 - 1e12"
				raise ValueError(msg)
			
			stop = False
			ylo = fylo
			yhi = fyhi

			if pt == fxlo:
				cdfinv.append(ylo)
				stop = True
			elif pt == fxhi:
				cdfinv.append(yhi)
				stop = True
			else:
				while self.cdf(yhi) > pt and self.cdf(ylo) < pt and stop == False:
					ysearch = (yhi + ylo)/2.0
					if self.cdf(ysearch) == pt:
						cdfinv.append(ysearch)
						stop = True
					elif self.cdf(ysearch) > pt:
						yhi = ysearch
					else:
						ylo = ysearch
					
					if abs(yhi-ylo) <= 1e-10:
						cdfinv.append((yhi+ylo)/2.0)
						stop = True
		
		acdfinv = np.array(cdfinv)
		return acdfinv
		
	def ccdf_inv(self, points):
		"""
		Return the inverse of the complementary distribution function
		Usage: Instance.ccdf_inv(points)

		Input
		------
		points: 0 <= points <= 1

		Output
		-------
		Return value: A numpy array with the corresponding inverse values
		"""

		accdfinv = self.__ccdf_cdf_inv(points, False)
		return accdfinv
	

	def rnd(self, n):
		"""
		Return random variates for the BiPareto distribution.
		Usage: Instance.rnd(n)

		Input
		------
		n: Number of random variates to return

		Output
		-------
		Return value: A numpy array with n-BiPareto random variates
		"""

		r = util.get_random()
		l = []
		for i in xrange(n):
			l.append(r.uniform(0, 1))
		
		lp = np.array(l)

		arnd = self.cdf_inv(lp)

		return arnd
