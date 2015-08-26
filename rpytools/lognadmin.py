import lognormal as logn
import numpy as np
import math
import scipy.special as spec
import scipy.constants as const
import scipy.optimize as opt
import rpytools.util as util


def f1_mu(x, u, s):
	t1 = math.sqrt(2.0/const.pi)

	t21 = (-u + np.log(x))**2.0
	t22 = 2.0*(s**2.0)
	t2 = np.exp(t21/t22)

	t31 = (-u + np.log(x))
	t32 = (s * math.sqrt(2.0))
	t3 = s * (1 + spec.erf(t31/t32))

	return t1/(t2*t3)

def f2_mu(x, u, s):
	t11 = (-u + np.log(x))**2.0
	t12 = 2.0*(s**2.0)
	t1 = np.exp(t11/t12)

	t2 = s * math.sqrt(2.0*const.pi)
	
	t31 = (-u + np.log(x))
	t32 = (s * math.sqrt(2.0))
	t33 = (-1 -spec.erf(t31/t32))

	t3 = (1 + t33/2.0)

	return 1.0/(t1*t2*t3)

def f1_sigma(x, u, s):
	t1 = math.sqrt(2.0/const.pi) * (-u + np.log(x))

	t21 = (-u + np.log(x))**2.0
	t22 = 2.0*(s**2.0)
	t2 = np.exp(t21/t22)
	
	t31 = (-u + np.log(x))
	t32 = (s * math.sqrt(2.0))
	t33 = (1 + spec.erf(t31/t32))
	t3 = (s**2.0)*t33

	return -t1/(t2*t3)

def f2_sigma(x, u, s):
	t1 = -u + np.log(x)

	t21 = (-u + np.log(x))**2.0
	t22 = 2.0*(s**2.0)
	t2 = np.exp(t21/t22)

	t31 = (-u + np.log(x))
	t32 = (s * math.sqrt(2.0))
	t33 = (-1 -spec.erf(t31/t32))
	t34 = math.sqrt(2.0*const.pi)*(s**2.0)

	t3 = t34*(1 + t33/2.0)

	return t1/(t2*t3)

def solve_admin(ival, *args):
	u = ival[0]
	s = ival[1]


	i = args[0]
	x = args[1]
	xrev = args[2]
	n = args[3]

	t1 = (2.0*(i+1)-1.0)/n
	tu2 = f1_mu(x,u,s)
	tu3 = f2_mu(xrev,u,s)

	nu = -np.sum(t1*(tu2+tu3))

	ts2 = f1_sigma(x,u,s)
	ts3 = f2_sigma(xrev,u,s)
	
	ns = -np.sum(t1*(ts2+ts3))

	return [nu, ns]

def lognormal_adsolver(pts):
	ec = util.ecdf(np.array(pts), issorted=False)
	x = ec[:,0]
	xrev = util.reverse(x)
	n = float((len(x)))
	i = np.array(range(len(x)), dtype=float)

	l1 = logn.Lognormal.fromFit(pts)
	imu = l1.mu()
	isig = l1.sigma()

	ivs = [imu, isig]
	ovs = (i,x,xrev,n)

	print ovs

	(fvals, infodict, ier, mesg) = opt.fsolve(solve_admin, ivs, ovs, None, 1, 0)

	f_mu = fvals[0]
	f_sigma = fvals[1]

	if ier != 1:
		raise logn.LognormalConvergenceError(mesg, (f_mu, f_sigma))

	return logn.Lognormal(f_mu, f_sigma)



def lognormal_nrsolver(pts):
	ec = util.ecdf(np.array(pts), issorted=False)
	x = ec[:,0]
	xrev = util.reverse(x)
	n = float(len(x))
	i = np.array(range(len(x)), dtype=float)

	l1 = logn.Lognormal.fromFit(pts)
	imu = l1.mu()
	isig = l1.sigma()

	ivs = [imu, isig]
	ovs = (i, x, xrev, n)
	
	[mu, sigma] = opt.root(solve_admin, ivs, ovs)

	return [mu, sigma]
