import rpytools.modlav as ml
import rpytools.util as util
import numpy as np
import scipy.optimize as opt

def f1_d(x,b,c,d):
	k = 1.0/(1.0 + d)
	return k * np.ones(len(x))

def f2_d(x,b,c,d):
	tc = 1.0 + np.power((c/x), (1.0/b))
	t1 = 1 - ((1.0 + d)/tc)
	return -1/(t1*tc)

def f1_b(x,b,c,d):
	t1 = np.power((c/x),(1.0/b))*np.log(c/x)
	t2 = (b**2.0)*(1.0 + np.power((c/x),(1.0/b)))
	return t1/t2

def f2_b(x,b,c,d):
	t1 = (1.0 + d)*np.power((c/x),(1.0/b))*np.log(c/x)
	
	t21 = (1.0 + np.power(c/x, 1.0/b))**2.0
	t22 = 1 - ((1.0 + d)/(1 + np.power(c/x, 1.0/b)))
	t2 = (b**2.0)*t21*t22

	return -t1/t2

def f1_c(x,b,c,d):
	t1 = np.power(c/x, -1 + (1.0/b))
	t2 = b * (1.0 + np.power(c/x, 1.0/b)) * x
	return -t1/t2

def f2_c(x,b,c,d):
	t1 = (1.0 + d)*np.power(c/x, -1 + (1.0/b))

	t21 = 1.0 - ( (1.0 + d)/(1.0 + np.power(c/x, 1.0/b)) )
	t22 = (1.0 + np.power(c/x, 1.0/b))**2.0
	t2 = b*t21*t22*x

	return t1/t2

def tll_admin(ival, *args):
	b = ival[0]
	c = ival[1]
	d = ival[2]

	i = args[0]
	x = args[1]
	xrev = args[2]
	n = args[3]

	t1 = (2.0*(i+1)-1)/n
	tb1 = f1_b(x,b,c,d)
	tb2 = f2_b(xrev,b,c,d)
	nb = -np.sum(t1*(tb1+tb2))

	tc1 = f1_c(x,b,c,d)
	tc2 = f2_c(xrev,b,c,d)
	nc = -np.sum(t1*(tc1+tc2))

	td1 = f1_d(x,b,c,d)
	td2 = f2_d(xrev,b,c,d)
	nd = -np.sum(t1*(td1+td2))

	return [nb,nc,nd]

def tlladmin_solver(pts):
	ec = util.ecdf(pts)
	x = ec[:,1]
	xrev = util.reverse(x)
	i = np.array(range(len(x)), dtype=float)
	n = float(len(x))

	ib = 1.0
	ic = float(np.median(x))
	id = ic/float(x.max())

	ivs = [ib,ic,id]
	ovs = (i,x,xrev,n)

	(fvals, infodict, ier, mesg) = opt.fsolve(tll_admin, ivs, ovs, None, 1, 0)
	f_b = fvals[0]
	f_c = fvals[1]
	f_d = fvals[2]

	if ier != 1:	
		raise ml.ModLavConvergenceError(mesg, (f_b,f_c,f_d))

	return ml.ModLav(f_b, f_c, f_d)



