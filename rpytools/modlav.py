import math
import util
import scipy.optimize as opt
import numpy as np
import minbisect

"""
The MODLAV distribution.
References:
1. E. Chlebus and G. Divgi, A novel probability distribution for modeling Internet traffic and its parameter estimation, 
	IEEE GLOBECOM 2007
2. E. Chlebus and G. Divgi, A versatile probability distribution for light and heavy tails of web file sizes,
	IEEE WCNC 2009
"""

class ModLavConvergenceError(Exception):
	def __init__(self, mesg, values):
		self.__mesg = mesg
		self.__beta = values[0]
		self.__c = values[1]
		self.__d = values[2]

	def __str__(self):
		prms = {"beta": self.__beta, "c": self.__c, "d": self.__d}
		return self.__mesg + " use the following parameters to verify manually - " + str(prms)
	
	def __repr__(self):
		prms = {"beta": self.__beta, "c": self.__c, "d": self.__d}
		return self.__mesg + " use the following parameters to verify manually - " + str(prms)
	
	def beta(self):
		return self.__beta
	
	def c(self):
		return self.__c
	
	def d(self):
		return self.__d

class ModLav:
	"""
	The ModLav class

	Static methods
	---------------
	mlefit: Fit using maximum likelihood estimation.
	mmefit: Fit using moments [special case with beta = 1]
	fromFit: Create a ModLav object from parameters estimated
	
	Instance methods
	-----------------
	pdf: Density function
	cdf: Distribution function
	ccdf: Complementary distribution function
	cdf_inv: Inverse of the distribution function
	ccdf_inv: Inverse of the complementary distribution function
	rnd: Random variates
	beta: beta-value
	c: c-value
	d: d-value
	"""

	@staticmethod
	def __solve_mle(ival, *args):
		"""
		Non-linear equation solver for the MODLAV ML estimation. DO NOT CALL STANDALONE
		ival: Array of initial values
			[0]: beta
			[1]: u [this is log(c)]
		*args: Arg tuple for optional/other parameters
			[0]: points
			[1]: sum(log(points))
			[2]: max(points)
		"""

		beta = ival[0]
		u = ival[1]

		pts = args[0]
		sl_pts = args[1]
		xmax = args[2]
		n = float(len(pts))

		eq1_t1 = ( n / ( 1 + math.pow((xmax/math.exp(u)), (1/beta)) ) ) - n
		eq1_t2 = 2*np.sum(1 / ( 1 + np.power((math.exp(u)/pts), (1/beta)) ))

		eq2_t1 = ( -n / ( 1 + math.pow((xmax/math.exp(u)), (1/beta)) ) ) * math.log(math.exp(u)/xmax) + n*u - n*beta - sl_pts
		eq2_t2 = 2*np.sum( np.log(pts/math.exp(u)) / ( 1 + np.power((math.exp(u)/pts), (1/beta)) ) )

		nbeta = eq2_t1 + eq2_t2
		nu = eq1_t1 + eq1_t2

		r = [nbeta, nu]

		return r

	@staticmethod
	def __solve_mle_ll(ival, *args):
		"""
		Non-linear equation solver for the LogLogistic ML estimation. DO NOT CALL STANDALONE
		ival: Array of initial values
			[0]: beta
			[1]: u = log(c)
		*args: Arg tuple for other / optional parameters
			[0]: points
			[1] = sum(log(points))
		"""
		beta = ival[0]
		u = ival[1]

		pts = args[0]
		sl_pts = args[1]
		n = float(len(pts))

		nu = -n + 2*np.sum(1 / ( 1 + np.power((math.exp(u)/pts), (1/beta)) ))
		nbeta = n*u - n*beta - sl_pts + 2*np.sum( np.log(pts/math.exp(u)) / ( 1 + np.power((math.exp(u)/pts), (1/beta)) ) )

		r = [nbeta, nu]
		return r
	
	@staticmethod
	def __solve_fitmin_ll(ival, *args):
		"""
		Non-linear equation solver for the MODLAV FIT Minimization. DO NOT CALL STANDALONE
		ival: Array of initial values
			[0]: log(beta)
			[1]: log(c)
		*args: Arg tuple for optional parameters
			[0]: CDF
		"""

		# b = ival[0]
		w = ival[0]
		e_w = math.exp(w)

		# c = ival[1]
		u = ival[1]
		e_u = math.exp(u)

		ec = args[0]
		x_i = ec[:,0]
		a_i = ec[:,1]

		t1 = ((1.0 + 1e-10)/a_i) - 1.0

		## Solve for c
		tc1 = -1.0/(e_u**2)
		tc2 = np.sum(np.power(x_i, 2.0)*np.power(t1, e_w))
		tc3 = np.sum(np.power(t1, -e_w))
		nu = tc1*tc2 + tc3

		## Solve for beta
		tb1 = 1/e_u
		tb21 = np.power(x_i, 2.0)
		tb22 = np.power(t1, e_w)
		tb23 = np.log(t1)
		tb2 = np.sum(tb21*tb22*tb23)
		tb3 = e_u
		tb41 = np.log(t1)
		tb42 = np.power(t1, e_w)
		tb4 = np.sum(tb41/tb42)
		nw = tb1*tb2 - tb3*tb4

		r = [nw, nu]

		return r

	@staticmethod
	def __solve_fitmin(ival, *args):
		"""
		Non-linear equation solver for the MODLAV FIT Minimization. DO NOT CALL STANDALONE
		ival: Array of initial values
			[0]: log(beta)
			[1]: log(c)
			[2]: log(d)
		*args: Arg tuple for optional parameters
			[0]: CDF
		"""

		# b = ival[0]
		w = ival[0]
		e_w = math.exp(w)

		# c = ival[1]
		u = ival[1]
		e_u = math.exp(u)

		# d = ival[2]
		v = ival[2]
		e_v = math.exp(v)

		ec = args[0]
		x_i = ec[:,0]
		a_i = ec[:,1]

		t1 = ((1 + e_v)/a_i) - 1.0

		## Solve for c
		tc1 = -1.0/(e_u**2)
		tc2 = np.sum(np.power(x_i, 2.0)*np.power(t1, e_w))
		tc3 = np.sum(np.power(t1, -e_w))
		nu = tc1*tc2 + tc3

		## Solve for d
		td1 = e_w/e_u
		td21 = np.power(x_i, 2.0)/a_i
		td22 = np.power(t1, e_w-1.0)
		td2 = np.sum(td21*td22)
		td3 = e_w*e_u
		td4 = np.sum(np.power(t1, -e_w-1.0)/a_i)
		nv = td1*td2 - td3*td4

		## Solve for beta
		tb1 = 1/e_u
		tb21 = np.power(x_i, 2.0)
		tb22 = np.power(t1, e_w)
		tb23 = np.log(t1)
		tb2 = np.sum(tb21*tb22*tb23)
		tb3 = e_u
		tb41 = np.log(t1)
		tb42 = np.power(t1, e_w)
		tb4 = np.sum(tb41/tb42)
		nw = tb1*tb2 - tb3*tb4

		r = [nw, nu, nv]

		return r

	@staticmethod
	def __solve_mme_alt(ival, *args):
		"""
		Non-linear equation solver for the MODLAV moments estimatation. DO NOT CALL STANDALONE
		ival: Array of initial values
			[0]: u [this is log(c)]
		*args: Arg tuple for optional parameters
			[0]: A = E[x]
			[1]: m - the maximum value
		"""

		u = ival

		A = args[0]
		m = args[1]

		e = lambda x: math.exp(x)
		
		k = e(u)/m
		nu = e(u)*( (1+k)*math.log((1+k)/k) -1 ) - A

		return nu


	@staticmethod
	def __initial_values(pts):
		"""
		Initial values for MODLAV estimation. DO NOT CALL STANDALONE.

		Input
		-----
		points: The set of points on which estimation is to be run

		Output
		------
		Return value: Dictionary object {"beta": 1, "c": median(points), "d": (c/max(points)}
		"""

		c = float(np.median(pts))
		beta = 1.0
		d = c/float(pts.max())

		r = {"beta": beta, "c": c, "d": d}

		return r

	@staticmethod
	def __mirrorxform(pts):
		import copy
		pts1 = copy.deepcopy(pts)

		pts = np.array(pts1)
		pts.sort()

		n = len(pts)
		mid = n/2

		c = pts[mid]
		pts[0:mid-1] = math.pow(c, 2.0)/pts[n-mid+1:n]

		return pts
	
	@staticmethod
	def fitmin_ll(points, **kwargs):
		"""
		Minimization of the FIT metric using the inverse CDF
		Usage: ModLav.fitmin(points, [beta=], [c=])

		Input
		------
		points: Points to run ML estimation
		**kwargs: Initial values for the mle fit. Mostly estimate Initial values from the __initial_values 
		method.
		beta = initial beta value
		c = initial c value

		Output
		------
		Return value: Tuple (beta, c, d)
		"""

		pts = np.array(points)
		c = util.ecdf(pts)
		iv = ModLav.__initial_values(pts)

		i_beta = iv["beta"]
		i_c = iv["c"]
		tol = 1e-10
		
		if "beta" in kwargs:
			i_beta = kwargs["beta"]
		if "c" in kwargs:
			i_c = kwargs["c"]
		if "tol" in kwargs:
			tol = kwargs["tol"]

		ivs = [math.log(i_beta), math.log(i_c)]
		oval = (c)
		
		(fvals, infodict, ier, mesg) = opt.fsolve(ModLav.__solve_fitmin_ll, ivs, oval, None, 1, 0, tol,2000)

		f_beta = math.exp(fvals[0])
		f_c = math.exp(fvals[1])
		f_d = 0.0
		

		if ier != 1:
			prms = {"beta": f_beta, "c": f_c, "d": f_d}
			raise ModLavConvergenceError(mesg, (f_beta, f_c, f_d))
		
		return (f_beta, f_c, f_d)
		

	@staticmethod
	def fitmin(points, **kwargs):
		"""
		Minimization of the FIT metric using the inverse CDF
		Usage: ModLav.fitmin(points, [beta=], [c=], [d=])

		Input
		------
		points: Points to run ML estimation
		**kwargs: Initial values for the mle fit. Mostly estimate Initial values from the __initial_values 
		method.
		beta = initial beta value
		c = initial c value
		d = initial d value

		Output
		------
		Return value: Tuple (beta, c, d)
		"""

		pts = np.array(points)
		c = util.ecdf(pts)
		iv = ModLav.__initial_values(pts)

		i_beta = iv["beta"]
		i_c = iv["c"]
		i_d = iv["d"]
		tol = 1e-10
		
		if "beta" in kwargs:
			i_beta = kwargs["beta"]
		if "c" in kwargs:
			i_c = kwargs["c"]
		if "d" in kwargs:
			i_d = kwargs["d"]
		if "tol" in kwargs:
			tol = kwargs["tol"]

		ivs = [math.log(i_beta), math.log(i_c), math.log(i_d)]
		oval = (c)
		
		(fvals, infodict, ier, mesg) = opt.fsolve(ModLav.__solve_fitmin, ivs, oval, None, 1, 0, tol,2000)

		f_beta = math.exp(fvals[0])
		f_c = math.exp(fvals[1])
		f_d = math.exp(fvals[2])
		

		if ier != 1:
			prms = {"beta": f_beta, "c": f_c, "d": f_d}
			raise ModLavConvergenceError(mesg, (f_beta, f_c, f_d))
		
		return (f_beta, f_c, f_d)
	
	@staticmethod
	def mlefit_ll(points, **kwargs):
		"""
		ML estimation for the MODLAV distribution.
		Usage: ModLav.mlefit(points, [beta=], [c=])

		Input
		-----
		points: Points to run ML estimation
		**kwargs: Initial values for the mle fit. If these values are not specific
					 initial values are estimated from the __initial_values private method.
					 beta = initial beta value
					 c = initial c value
		Output
		------
		Return value: Tuple (beta, c, 0.0)
		"""

		pts = np.array(points)
		sl_pts = np.sum(np.log(pts))
		
		iv = ModLav.__initial_values(pts)
		
		i_beta = iv["beta"]
		i_c = iv["c"]

		if "beta" in kwargs:
			i_beta = kwargs["beta"]
		if "c" in kwargs:
			i_c = kwargs["c"]

		ivs = [i_beta, math.log(i_c)]
		oval = (pts, sl_pts)

		(fvals, infodict, ier, mesg) = opt.fsolve(ModLav.__solve_mle_ll, ivs, oval, None, 1, 0, 1e-12)

		f_beta = fvals[0]
		f_c = math.exp(fvals[1])
		# Try using approximation (min/max)^(1/b)
		# f_d = i_d 
		f_d = 0.0
		
		if ier != 1:
			prms = {"beta": f_beta, "c": f_c, "d": f_d}
			raise ModLavConvergenceError(mesg, (f_beta, f_c, f_d))

		return (f_beta, f_c, f_d)

	@staticmethod
	def mlefit(points, **kwargs):
		"""
		ML estimation for the MODLAV distribution.
		Usage: ModLav.mlefit(points, [beta=], [c=], [d=])

		Input
		-----
		points: Points to run ML estimation
		**kwargs: Initial values for the mle fit. If these values are not specific
					 initial values are estimated from the __initial_values private method.
					 beta = initial beta value
					 c = initial c value
					 d = initial d value
					 xmax = xmax value to have the tail fall off steeper or shallower. This is used when
					 		  optimizing estimated parameters using the FIT metric.
		
		Output
		------
		Return value: Tuple (beta, c, d)
		"""

		pts = np.array(points)
		sl_pts = np.sum(np.log(pts))
		xmax = pts.max()
		
		iv = ModLav.__initial_values(pts)
		
		i_beta = iv["beta"]
		i_c = iv["c"]
		i_d = iv["d"]

		if "beta" in kwargs:
			i_beta = kwargs["beta"]
		if "c" in kwargs:
			i_c = kwargs["c"]
		if "d" in kwargs:
			i_d = kwargs["d"]
		if "xmax" in kwargs:
			xmax = kwargs["xmax"]

		ivs = [i_beta, math.log(i_c)]
		oval = (pts, sl_pts, xmax)

		(fvals, infodict, ier, mesg) = opt.fsolve(ModLav.__solve_mle, ivs, oval, None, 1, 0, 1e-12)

		f_beta = fvals[0]
		f_c = math.exp(fvals[1])
		# Try using approximation (min/max)^(1/b)
		# f_d = i_d 
		f_d = math.pow(f_c/xmax, 1/f_beta)
		
		if ier != 1:
			prms = {"beta": f_beta, "c": f_c, "d": f_d}
			raise ModLavConvergenceError(mesg, (f_beta, f_c, f_d))

		return (f_beta, f_c, f_d)
	
	@staticmethod
	def altmmefit(points, **kwargs):
		"""
		Moments estimation for the MODLAV distribution.
		Usage: ModLav.altmmefit(points, [c=], [d=])
		The solution is for beta=1

		Input
		-----
		points: Points to run the estimation
		**kwargs: Initial values for the mmefit.
			c = initial c value [estimated using __initial values if not supplied]
			d = initial d value [estimated using __initial_values if not supplied]
			xmax = xmax to force the tail to either fall steeper or shallower using optimization
		
		Output
		------
		Return value: Tuple (beta, c, d)
		"""

		pts = np.array(points)
		n = float(len(pts))
		A = np.mean(pts)
		xmax = float(pts.max())
		if "xmax" in kwargs:
			xmax = float(kwargs["xmax"])

		iv = ModLav.__initial_values(pts)
		i_beta = iv["beta"]
		i_c = iv["c"]
		i_d = iv["d"]

		ivs = math.log(i_c)
		ovs = (A, xmax)

		(fval, infodict, ier, mesg) = opt.fsolve(ModLav.__solve_mme_alt, ivs, ovs, None, 1, 0, 1e-12)
		f_c = math.exp(fval)
		f_d = f_c/xmax

		if ier != 1:
			raise ModLavConvergenceError(mesg, (i_beta, f_c, f_d))	


		return (i_beta, f_c, f_d)

	@staticmethod
	def fromFit(points, **kwargs):
		"""
		Create a ModLav object with parameters estimated from points.
		Usage: ModLav.fromFit(points, mlefit=True|False, mt=True|False)

		Input
		-----
		points: set of points to estimate ModLav parameters
		**kwargs: Optional arguments
					 fit=[mmefit|mmefit|mmefitx]: Default mmefit
					 	if fit is mmefit
							dcompute=[estimate|frommax]: Default frommax
					 mt=[True|False] False by default. Mirror Xform done on original dataset if True
					 beta=Initial beta value
					 c=Initial c-value
					 d=Initial d-value
		Output
		------
		Return value: A ModLav object with parameters estimated from points
		"""

		mt = False
		fitType = "mlefit"	
		ignoreConv = True

		if "mt" in kwargs:
			mt = kwargs["mt"]
		if "fit" in kwargs:
			fitType = kwargs["fit"]
		if "ignconv" in kwargs:
			ignoreConv = kwargs["ignconv"]
		
		modlavinst = None
		
		## Using same code for LogLogistic as well
		## Same equation forms with d = 0.0
		fitmap = {"mlefit": ModLav.mlefit, \
					 "mmefit": ModLav.altmmefit, \
					 "fitmin": ModLav.fitmin, \
					 "mlefitll": ModLav.mlefit_ll, \
					 "fitminll": ModLav.fitmin_ll}

		if mt == True:
			points = ModLav.__mirrorxform(points)	
		
		fitFunc = fitmap[fitType]
		try:
			(beta, c, d) = fitFunc(points, **kwargs)
			modlavinst = ModLav(beta, c, d)
		except ModLavConvergenceError as mlce:
			if ( ignoreConv == False ):
				raise(mlce)
			else:
				modlavinst = ModLav(mlce.beta(), mlce.c(), mlce.d())
		
		return modlavinst

	def __init__(self, beta, c, d):
		"""
		Constructor.

		Input
		------
		beta, c and d: Input for the ModLav distribution
		"""

		self.__beta = float(beta)
		self.__c = float(c)
		self.__d = float(d)

	def beta(self):
		""" Return the beta value """
		return self.__beta
	
	def c(self):
		""" Return the c value """
		return self.__c

	def d(self):
		""" Return the d value """
		return self.__d
	
	def params(self):
		""" Return the parameters of the distribution as a dict object """
		return {"beta": self.__beta, "c": self.__c, "d": self.__d}
	
	def pdf(self, points):
		"""
		Return the density function of ModLav for the points
		Usage: Instance.pdf(points)

		Input
		-----
		points: Set of points to return the density function

		Output
		-------
		Return value: A numpy array with the corresponding pdf
		"""

		pts = np.array(points)
		
		t1 = (1 + self.__d)*np.power((pts/self.__c), 1/self.__beta)
		t2 = self.__beta*pts*np.power(np.power((pts/self.__c), 1/self.__beta) + 1, 2.0)
		apdf = t1/t2

		return apdf

	def cdf(self, points):
		"""
		Return the distribution function of MODLAV for the points
		Usage: Instance.cdf(points)

		Input
		------
		points: Set of points to return the cdf

		Output
		------
		Return value: A numpy array with the corresponding pdf
		"""
		
		pts = np.array(points)
		acdf = (1 + self.__d)/(1 + np.power(self.__c/pts, 1/self.__beta))

		return acdf
	
	def ccdf(self, points):
		"""
		Return the complementary distribution function of MODLAV for the points
		Usage: Instance.ccdf(points)

		Input
		-----
		points: Set of points to return the ccdf

		Output
		------
		Return value: A numpy array with the corresponding ccdf
		"""

		accdf = 1 - self.cdf(points)
		return accdf

	def cdf_inv(self, points):
		"""
		Return the inverse cdf of the points
		Usage: Instance.cdf_inv(points)

		Input
		-----
		points: 0 <= points[i] <= 1

		Output
		------
		Return value: A numpy array with the corresponding inverse cdf
		"""

		pts = np.array(points)
		acdfinv = self.__c*np.power(pts/(1 + self.__d - pts), self.__beta)

		return acdfinv
	
	def ccdf_inv(self, points):
		"""
		Return the inverse ccdf of the points
		Usage: Instance.ccdf_inv(points)

		Input
		-----
		points: 0 <= points[i] <= 1

		Output
		------
		Return value: A numpy array with the corresponding inverse ccdf
		"""

		pts = np.array(points)
		accdfinv = self.__c*( np.power((1-pts)/(pts+self.__d), self.__beta) )
		return accdfinv
	
	def rnd(self, n):
		"""
		Return MODLAV random variates
		Usage: Instance.rnd(n)

		Input
		-----
		n = Number of random variates to generate

		Output
		------
		Return value: A numpy array of n MODLAV random variates
		"""

		r = util.get_random()
		U = []
		for i in xrange(n):
			U.append(r.uniform(0, 1))

		arnd = self.cdf_inv(U)

		return arnd
	
	def ksmetric(self, **kwargs):
		"""
		Return the kolmogorov-smirnov metric for MODLAV
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
		Return the FIT metric for MOVLAV
		Input:
		**kwargs:
			points = [set of points to compute the cdf]
			-or-
			cdf = [Already computed cdf]
		
		Output:
			Fit metric
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
		Return the Difference metric for MOVLAV
		Input:
		**kwargs:
			points = [set of points to compute the cdf]
			-or-
			cdf = [Already computed cdf]
		
		Output:
			Difference metric. The closer the difference to 0 the more similar the fit.	
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

def optfit(x, lo, hi, n, **kwargs):
	"""
	Optimum modlav fit using search for the best xmax.
	Input:
	x: Set of points
	lo: Low xmax value
	hi: Hi xmax value [Note lo <= max(x) <= hi]
	n: Number of searches.
	**kwargs:
	mlefit: True - use mlefit, False - use mmefit. True by default
	mt: True| false. Use mirror transform. False by default

	Output:
	Dict: {"fit": (ModLav object, xmax, FIT metric), "ks": (ModLav, xmax, ks)}
	"""

	pts = util.gen_points(lo, hi, n)
	fits_fm = dict()
	fits_ks = dict()
	rval = dict()
	x.sort()
	c = util.ecdf(x)

	mlefit = True
	if "mlefit" in kwargs:
		mlefit = kwargs["mlefit"]
	
	vmt = False
	if "mt" in kwargs:
		vmt = kwargs["mt"]

	for xmax in pts:
		try:
			if mlefit == True:
				m = ModLav.fromFit(x, xmax=xmax, fit="mlefit",mt=vmt)
			else:
				m = ModLav.fromFit(x, xmax=xmax, fit="mmefit",mt=vmt)
		except ModLavConvergenceError, mlce:
			print mlce
			continue
		except BaseException, err:
			print str(err)
			continue
		
		fm = m.fitmetric(cdf=c)
		ks = m.ksmetric(cdf=c)

		fits_fm[fm] = (xmax, m)
		fits_ks[ks] = (xmax, m)
	
	fm_keys = np.array(fits_fm.keys())
	min_fm = fm_keys.min()

	rval["fit"] = (fits_fm[min_fm][1], fits_fm[min_fm][0], min_fm)

	ks_keys = np.array(fits_ks.keys())
	min_ks = ks_keys.min()

	rval["ks"] = (fits_ks[min_ks][1], fits_ks[min_ks][0], min_ks)

	return rval
