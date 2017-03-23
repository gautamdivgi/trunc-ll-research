import numpy as np
import scipy.optimize as opt
import scipy.special as spec
from math import pi as pi
from math import e as e


def create_initial_values(other_args, u, s):
	## Using the following notations
	## "y": y[0..n-1]
	## "z": y[n-i-1..0]
	## "ly_u": [log(y) - u]
	## "lz_u": [log(z) - u]
	## "ly_u_r2s": [log(y) - u]/sqrt(2)*s
	## "lz_u_r2s": [log(z) - u)]/sqrt(2)*s
	## "erf_ly_u_r2s": erf{[log(y) - u]/sqrt(2)*s}
	## "erf_lz_u_r2s": erf{[log(z) - u)]/sqrt(2)*s}

	y = other_args["y"]
	z = other_args["z"]

	ly_u = np.log(y) - u
	lz_u = np.log(z) - u

	ly_u_r2s = ly_u/((2.0**0.5) * s)
	lz_u_r2s = lz_u/((2.0**0.5) * s)

	erf_ly_u_r2s = spec.erf(ly_u_r2s)
	erf_lz_u_r2s = spec.erf(lz_u_r2s)

	other_args["ly_u"] = ly_u
	other_args["lz_u"] = lz_u
	other_args["ly_u_r2s"] = ly_u_r2s
	other_args["lz_u_r2s"] = lz_u_r2s
	other_args["erf_ly_u_r2s"] = erf_ly_u_r2s
	other_args["erf_lz_u_r2s"] = erf_lz_u_r2s

def logn_solver(ivals, *args):
	## u, s values for this iteration
	u = ivals[0]
	s = ivals[1]

	## other arguments needed
	other_args = args[0]
	create_initial_values(other_args, u, s)

	y = other_args["y"]
	z = other_args["z"]
	iter_term = other_args["iter_term"]
	ly_u = other_args["ly_u"]
	lz_u = other_args["lz_u"]
	ly_u_r2s = other_args["ly_u_r2s"]
	lz_u_r2s = other_args["lz_u_r2s"]
	erf_ly_u_r2s = other_args["erf_ly_u_r2s"]
	erf_lz_u_r2s = other_args["erf_lz_u_r2s"]
	n = other_args["n"]

	t1 = e**(-(lz_u_r2s**2.0))
	t2 = ((2.0*pi)**0.5)*s*(0.5 * (-erf_lz_u_r2s - 1) + 1)
	t3 = ((2.0/pi)**0.5)*(e**(-(ly_u_r2s**2.0)))
	t4 = s*(erf_ly_u_r2s+1)

	nu = -np.sum(iter_term * ((t1/t2) - (t3/t4)))/n
	ns = -np.sum(iter_term * ( ((lz_u/s)*(t1/t2)) - ((ly_u/s)*(t3/t4)) ))/n

	return np.array([nu,ns])

def jacobian_d2Sdu2(ivals, *args):
	u = ivals[0]
	s = ivals[1]
	
	other_args = args[0]
	y = other_args["y"]
	z = other_args["z"]
	iter_term = other_args["iter_term"]
	ly_u = other_args["ly_u"]
	lz_u = other_args["lz_u"]
	ly_u_r2s = other_args["ly_u_r2s"]
	lz_u_r2s = other_args["lz_u_r2s"]
	erf_ly_u_r2s = other_args["erf_ly_u_r2s"]
	erf_lz_u_r2s = other_args["erf_lz_u_r2s"]
	n = other_args["n"]

	t1 = 2.0*(e**(-((ly_u/s)**2.0)))
	t2 = pi*(s**2.0)*((erf_ly_u_r2s+1)**2.0)

	t3 = e**(-((lz_u/s)**2.0))
	t4 = 2.0*pi*(s**2.0)*((0.5 * (-erf_lz_u_r2s - 1) + 1)**2.0)

	t5 = ((2.0/pi)**0.5)*ly_u*(e**(-(ly_u_r2s**2.0)))
	t6 = (s**3.0)*(erf_ly_u_r2s+1)

	t7 = lz_u*(e**(-(lz_u_r2s**2.0)))
	t8 = ((2.0*pi)**0.5)*(s**3.0)*(0.5*(-erf_lz_u_r2s-1) + 1)

	j00 = -np.sum(iter_term * (-t1/t2 - t3/t4 - t5/t6 + t7/t8))/n

	return j00

def jacobian_d2Sdsdu(ivals, *args):
	u = ivals[0]
	s = ivals[1]
	
	other_args = args[0]
	y = other_args["y"]
	z = other_args["z"]
	iter_term = other_args["iter_term"]
	ly_u = other_args["ly_u"]
	lz_u = other_args["lz_u"]
	ly_u_r2s = other_args["ly_u_r2s"]
	lz_u_r2s = other_args["lz_u_r2s"]
	erf_ly_u_r2s = other_args["erf_ly_u_r2s"]
	erf_lz_u_r2s = other_args["erf_lz_u_r2s"]
	n = other_args["n"]

	t1 = ((2.0/pi)**0.5)*(e**(-(ly_u_r2s**2.0)))
	t2 = (s**2.0)*(erf_ly_u_r2s+1)

	t3 = e**(-(lz_u_r2s**2.0))
	t4 = ((2.0*pi)**0.5)*(s**2.0)*(0.5*(-erf_lz_u_r2s-1)+1)

	t5 = ((2.0/pi)**0.5)*(ly_u**2.0)*(e**(-(ly_u_r2s**2.0)))
	t6 = (s**4.0)*(erf_ly_u_r2s+1)

	t7 = (lz_u**2.0)*(e**(-(lz_u_r2s**2.0)))
	t8 = ((2.0*pi)**0.5)*(s**4.0)*(0.5*(-erf_lz_u_r2s-1)+1)

	t9 = 2.0*ly_u*(e**(-((ly_u/s)**2.0)))
	t10 = pi*(s**3.0)*((erf_ly_u_r2s+1)**2.0)

	t11 = lz_u*(e**(-((lz_u/s)**2.0)))
	t12 = 2.0*pi*(s**3.0)*((0.5*(-erf_lz_u_r2s-1)+1)**2.0)

	j01 = -np.sum(iter_term * (t1/t2 - t3/t4 -t5/t6 + t7/t8 - t9/10 - t11/t12))/n

	return j01
		

def jacobian_d2Sduds(ivals, *args):
	j10 = jacobian_d2Sdsdu(ivals, *args)
	return j10

def jacobian_d2Sds2(ivals, *args):
	u = ivals[0]
	s = ivals[1]
	
	other_args = args[0]
	y = other_args["y"]
	z = other_args["z"]
	iter_term = other_args["iter_term"]
	ly_u = other_args["ly_u"]
	lz_u = other_args["lz_u"]
	ly_u_r2s = other_args["ly_u_r2s"]
	lz_u_r2s = other_args["lz_u_r2s"]
	erf_ly_u_r2s = other_args["erf_ly_u_r2s"]
	erf_lz_u_r2s = other_args["erf_lz_u_r2s"]
	n = other_args["n"]

	t1 = ((2.0/pi)**0.5)*(ly_u**3.0)*(e**(-(ly_u_r2s**2.0)))
	t2 = (s**5.0)*(erf_ly_u_r2s+1)

	t3 = (lz_u**3.0)*(e**(-(lz_u_r2s**2.0)))
	t4 = ((2.0*pi)*0.5)*(s**5.0)*(0.5*(-erf_lz_u_r2s-1)+1)

	t5 = 2.0*(ly_u**2.0)*(e**(-((ly_u/s)**2.0)))
	t6 = pi*(s**4.0)*((erf_ly_u_r2s+1)**2.0)

	t7 = (lz_u**2.0)*(e**(-((lz_u/s)**2.0)))
	t8 = 2*pi*(s**4.0)*((0.5*(-erf_lz_u_r2s-1)+1)**2.0)

	t9 = 2.0*((2.0/pi)**0.5)*ly_u*(e**(-(ly_u_r2s**2.0)))
	t10 = (s**3.0)*(erf_ly_u_r2s+1)

	t11 = ((2.0/pi)**0.5)*lz_u*(e**(-(lz_u_r2s**2.0)))
	t12 = (s**3.0)*(0.5*(-erf_lz_u_r2s-1)+1)

	j11 = -np.sum(iter_term*(-t1/t2 + t3/t4 -t5/t6 -t7/t8 +t9/t10 -t11/t12))/n

	return j11
	

def jacobian(ivals, *args):
	j00 = jacobian_d2Sdu2(ivals, *args)
	j01 = jacobian_d2Sdsdu(ivals, *args)
	j10 = jacobian_d2Sduds(ivals, *args)
	j11 = jacobian_d2Sds2(ivals, *args)

	return np.array([[j00,j01],[j10,j11]])

def solver_main(data_pts):
	
	## Scrub data points, remove 0's
	## Ideally should be done by whatever is calling this 
	## But better to be sure
	## y is the scrubbed set of data points
	dp = np.array(data_pts)
	y = dp[np.where(dp > 0)]

	## z = y[n-i-1], with i = 0..n-1, n = len(data_pts)
	z = np.flipud(y)

	## Initial estimates - use MLE
	n = float(len(y))
	rootn = (n**0.5)
	initial_u = np.sum(np.log(y))/n
	initial_s = (np.sum(np.power((np.log(y) - initial_u)/rootn, 2)))**0.5

	other_args = {"y": y, "z": z, "iter_term": (2.0*np.array(xrange(len(y)))+1), "n": n}

	(fval, infodict, ier, mesg) = opt.fsolve(logn_solver, [initial_u, initial_s], (other_args), jacobian, 1, 0)

	if ier != 1:
		print "Failed to converge: ", mesg
	print "u: ", fval[0]
	print "s: ", fval[1]
