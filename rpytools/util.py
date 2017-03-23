# print basic statistics of an array

import numpy as np
import scipy.stats.mstats as ms
import random
import matplotlib.pyplot as plt
import math
from rpytools.similarity import new_similarity_invcdf
from scipy.integrate import simps

def get_stats(arr):
	sz = arr.size
	amin, amax = arr.min(), arr.max()
	q = ms.mquantiles(arr, [0.1, 0.5, 0.9])
	mu = arr.mean()
	sigma = arr.std()
	cv = sigma/mu

	return {"size": sz, "min": amin, "max": amax, "pct10": q[0], "pct50": q[1], "pct90": q[2], "mu": mu, "sigma": sigma, "cv": cv}

def pstats(arr):
	sz = arr.size
	amin, amax = arr.min(), arr.max()
	q = ms.mquantiles(arr, [0.1, 0.5, 0.9])
	mu = arr.mean()
	sigma = arr.std()

	print "Size: ", sz
	print "Range: ", amin, " - ", amax
	print "Quantiles : 10% - ", q[0], ", 50% - ", q[1], ", 90% - ", q[2]
	print "Mean: ", mu
	print "Std. deviation: ", sigma
	print "CV: ", sigma/mu

def dice(x1, x2):
	simmat = 2*np.sum(x1 * x2)/np.sum(np.power(x1,2.0) + np.power(x2,2.0))
	return simmat

def wave_hedges(x1, x2):
	return np.sum(np.abs(x1-x2)/np.maximum(x1,x2))

def kumar_hassebrook(x1, x2):
	return np.sum(x1 * x2)/( np.sum(np.power(x1,2.0)) + np.sum(np.power(x2,2.0)) - np.sum(x1*x2) )

def ccdf(arr, **kwargs):
	n = float(len(arr))
	cdf = ecdf(arr, **kwargs)
	n1 = len(cdf)
	a_ccdf = np.zeros((n1,2),dtype=float)
	a_ccdf[:,0] = cdf[:,0]
	a_ccdf[:,1] = 1 - cdf[:,1]
	# a_ccdf[:,1] = 1 - cdf[:,1]

	return a_ccdf

def ecdf(arr, **kwargs):
	""" The argument needs to be sorted - That is the default assumption """
	""" arr is assumed to be a single dimension array """
	
	issortedVal = True
	zdispVal = False

	if "issorted" in kwargs:
		issortedVal = kwargs["issorted"]
	
	if "zdisp" in kwargs:
		zdispVal = kwargs["zdisp"]
	
	if issortedVal == False:
		arr.sort()

	n = float(len(arr))
	i = 0
	n_dval = 0
	ce = 0.0	
	a_cdf = np.zeros((int(n),3),dtype=float)

	while i < int(n):
		ce = arr[i]
		while i < n and arr[i] <= ce:
			i+= 1
		
		a_cdf[n_dval, 0] = float(ce)
		a_cdf[n_dval, 1] = float(i)/float(n+1)
		a_cdf[n_dval, 2] = float(i-1)/float(n)
		
		n_dval+= 1
	
	a_cdf = np.resize(a_cdf, (n_dval,3))

	if zdispVal == True and a_cdf[0,1] == 0:
		z = np.array([0,0,0])
		a_cdf = np.append(z,a_cdf).reshape(n_dval+1,3)

	return a_cdf

def gen_points(lo, hi, N):
	""" Generate equidistant points for plotting """
	return np.linspace(lo, hi, num=N)
	
	## a = np.array(range(0, N))
	## return lo + (a * (hi-lo)/float(N))

def runfunc(f, lo, hi, N, **kwargs):
	xy = np.zeros((N,2), dtype=float)

	xy[:,0] = gen_points(lo, hi, N)
	xy[:,1] = f(xy[:,0], **kwargs)

	return xy

def regress(a, b):
	""" Linear regression, returns slope, intercept and r-value """
	
	if a.size != b.size:
		raise RuntimeError("a and b must be the same size")
	
	abar = a.mean()
	bbar = b.mean()

	b1 = sum( (a - abar)*b )/sum( (a - abar)**2 )
	b0 = bbar - b1 * abar
	
	sst = sum( (b - bbar)**2 )
	bhat = b0 + b1*a
	sse = sum( (b - bhat)**2 )

	r2 = 1 - (sse/sst)

	return (b0, b1, r2)

def reverse(x):
	xp = x.tolist()
	xp.reverse()
	return np.array(xp)

def findidx(X, v, tol=1e-3):
	"""
	Find the first index in the array X whose value is as close to v 
	within the specified tolerance. The tolerance is 1e-3 by default

	Input
	-----
	X: A numpy array
	v: The value whose index needs to be returned
	tol: Tolerance level

	Output
	-------
	index i that contains v or where |X[i] -v| <= tol, or -1 if no such index is found
	"""
	loc = -1
	diff = 1e15 # Take a big difference
	n = len(X)

	for i in xrange(n):
		ndiff = abs(X[i]-v)
		if ndiff <= tol and ndiff < diff:
			loc = i
			diff = ndiff
	
	return loc
			
def remove_outliers(X, lo, hi):
	"""
	Remove all points left of lo and right of hi in the array X.
	Essentially returns the closed interval (lo, hi) in X

	Input
	------
	X: A numpy array
	lo: The low value
	hi: The high value

	Output
	------
	A numpy array that is the intersection of the closed interval (lo, hi) with X
	"""
	
	x1 = np.array(X)
	y1 = x1[np.where(x1 > lo)]
	y2 = y1[np.where(y1 <= hi)]

	return y2

def get_random():
	sr = random.SystemRandom()
	seed = sr.randint(0, 1000000)
	r = random.Random(seed)
	return random.Random()

def modlav_law(r,beta,c,k):
	n = len(r)
	rp = np.array(r)
	xr = c*np.power( (n-r)/(float(k)+r+1.0), beta )
	return xr
	

def read_data(f, sep=" ", dtype=float):
	fid = None
	try:
		fid = open(f, "r")
		x = []	
		for l in fid:
			if l[:1] == "#":
				continue
			y = l.split(sep)
			if len(y) == 1:
				x.append(dtype(y[0]))
			else:
				r = []
				for e in y:
					r.append(dtype(e))
				x.append(r)
		
		fid.close()
		return np.array(x)
	except:
		pass
	finally:
		if fid != None:
			fid.close()
			fid = None

def write_data(f, x, sep=" "):
	fid = None
	try:
		x1 = np.array(x)
		slist = []
		nd = x1.ndim
		for r in x1:
			if nd == 1:
				slist.append(str(r) + "\n")
			else:
				l = len(r)
				i = 0
				s = ""
				while i < l:
					if i < l-1:
						s = s + str(r[i]) + sep
					else:
						s = s + str(r[i])
					i = i + 1
				slist.append(s + "\n")
		
		fid = open(f, "w+")
		fid.writelines(slist)
		fid.close()
	# except:
	# 	print "cannot write..."
	finally:
		if fid != None:
			fid.close()
			fid = None

def kstest(x, x1, y):
	"""
	Kolmogorov-Smirnov statistic.
	x: CDF values counted as i/n+1
	x1: CDF values counted as i-1/n
	y: Fitted CDF values

	Output: double - test metric
	"""

	xy = np.abs(x-y)
	yx1 = np.abs(y-x1)
	acmp = np.zeros((len(x),2))
	acmp[:,0] = xy
	acmp[:,1]=yx1
	mx = np.amax(acmp, axis=1)

	return mx.max()

def wkstest(x, y):
	"""
	Weighted K-S statistic for better power law comparison
	x: CDF of the values counted as i/n+1
	y: Fitted CDF values
	Output: double - test metric
	"""
	w = np.power(y*(1.0 - y), 0.5)
	xy = np.abs(x-y)/w
	return xy.max()

def fitmetric(xi, xhat_i, *args):
	return mitz_tworetzky_fitmetric(xi, xhat_i, *args)

def chlebus_divgi_sim_fitmetric(xi, x_hat_i, *args):
	"""
	Chlebus, Divgi similarity metric
	xi: Original values
	x_hat_i: Values computed F_inv(i/n+1) from the original values

	Output: Fit metric [double]
	"""
	if len(args) == 0:
		ec = ecdf(xi)
		xspace = ec[:,1]
	else:
		xspace = args[0]
	
	yspace = np.minimum(xi, x_hat_i)/np.maximum(xi, x_hat_i)
	return simps(yspace, xspace)

def mitz_tworetzky_fitmetric(xi, x_hat_i, *args):
	"""
	FIT metric statistic
	xi: Original values.
	x_hat_i: Values computed F_inv(i/n+1) from the original values

	Output: Fit metric [double]
	"""
	n = float(len(xi))
	return np.sum(np.power(xi - x_hat_i, 2.0)/(n * x_hat_i))

def simenv(pts, dist, pcc=True):
	"""
	Simulation envelope plotting
	Input:
	-----
	pts: The set of points
	dist: The distribution fitted to the set of points
	pcc: Envelope for ccdf - default is true. If false, then the envelope is for the cdf

	Output
	-----
	None
	"""

	x = np.array(pts)
	x.sort()
	
	
	N = 100
	n = len(x) + 100
	
	for i in xrange(N):
		r = dist.rnd(n)
		r.sort()

		if pcc == True:
			ncc = ccdf(r, issorted=True)
			plt.loglog(ncc[:,0], ncc[:,1], color='#A0A0A0' , linestyle='steps', linewidth=0.5)
		else:
			ncc = ecdf(r, issorted=True)
			plt.plot(ncc[:,0], ncc[:,1], color='#A0A0A0', linestyle='steps', linewidth=0.5)
	

	if pcc == True:
		cc = ccdf(x, issorted=True)
		plt.loglog(cc[:,0],cc[:,1],'k-',linestyle='steps',linewidth=3)
	else:
		cc = ecdf(x, issorted=True)
		plt.plot(cc[:,0],cc[:,1],'k-',linestyle='steps',linewidth=3)

def wsimenv(pts, dist, pcc=True):
	"""
	Simulation envelope for multiple distributions
	Input
	-----
	pts: The set of points
	dist: The distributions with their weights as a list of tuples [(w1, d1), (w2, d2),...(wn, dn)]
	      The precondition on the weights is that w1 + w2 + ... + wn = 1.0
			and that w1 >= w2 >= .... >= wn. Also, each wi * len(pts) should be an integer value, i.e.
			there should be enough points generated to cover all possibilities.
	pcc: True|False. True to plot CCDF, False to plot CDF

	Output
	------
	None
	"""
	N = 100
	x = np.array(pts)
	n = len(x)

	rgen = get_random()
	
	for e in xrange(N):
		r = []
		prev_dtup = None
		for dtup in dist:
			if prev_dtup == None:
				lb = 0.0
			else:	
				lb = prev_dtup[0]
			ub = dtup[0] + lb
			n1 = int(math.ceil(dtup[0]*n))
	
			for i in xrange(n1):
				rvar = rgen.uniform(lb,ub)
				r.append(dtup[1].cdf_inv(rvar))
			
			prev_dtup = dtup
		
		if pcc == True:
			ncc = ccdf(r, issorted=False)
			plt.loglog(ncc[:,0], ncc[:,1], color='#A0A0A0' , linestyle='steps', linewidth=0.5)
		else:
			ncc = ecdf(r, issorted=False)
			plt.plot(ncc[:,0], ncc[:,1], color='#A0A0A0', linestyle='steps', linewidth=0.5)
		
	if pcc == True:
		cc = ccdf(x, issorted=True)
		plt.loglog(cc[:,0],cc[:,1],'k-',linestyle='steps',linewidth=3)
	else:
		cc = ecdf(x, issorted=True)
		plt.plot(cc[:,0],cc[:,1],'k-',linestyle='steps',linewidth=3)
