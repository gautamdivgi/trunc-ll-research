#!/usr/bin/python

import rpytools.modlav as ml
import rpytools.util as util
import numpy as np
import multiprocessing as mp
from multiprocessing import Pool
import sys
import getopt

max_of_x = None
x = None
fit = None
mt = None
c = None

def usage():
	print "parmlfit <-f input pts> <-l low> <-h high> <-n #. of pts in [low,high]> <-t mlefit|mmefit> <-m true|false>"
	print "-f input pts: The full path name of the file containing the data points"
	print "-l low: The lowest xmax for the ML fit"
	print "-h high: The highest xmax for the ML fit"
	print "-n: The number of points to divide the [low,high] range. Each point is taken as an xmax to evaluate the fit"
	print "-t: The fit type - mlefit|mmefit"
	print "-m: Use mirror transform - true or false."

def optfit(mx):
	global x,fit,mt, c
	dummy_m = ml.ModLav(0.0, 0.0, 0.0)
	dummy_mx = float('NaN')
	dummy_ks = float('Inf')
	dummy_fit = float('Inf')
	dummy_dif = float('Inf')

	try:
		xfit=fit
		xmt=mt
		xmx=mx
		m = ml.ModLav.fromFit(x, xmax=xmx, fit=xfit, mt=xmt)
		fm = m.fitmetric(cdf=c)
		# Removing KS
		## ks = m.ksmetric(cdf=c)
		df = m.difference(cdf=c)
		return (m, xmx, fm, df)
	#except ml.ModLavConvergenceError, mlce:
	#	return (dummy_m, dummy_mx, dummy_ks, dummy_fit)
	except BaseException, be:
		print "Exception -> ", be
		return (dummy_m, dummy_mx, dummy_fit, dummy_dif)

def best_fit(rs, idx):

	minv = float('Inf')
	opt_result = None

	for r in rs:
		if r[idx] < minv:
			minv = r[idx]
			opt_result = r
	
	return opt_result

def paroptfit(x1, hi, lo, n, fit1, mt1):
	"""
	x1: Sorted array of points
	hi: Max. xmax to estimate to
	lo: Min. xmax to estimate to
	n: #. of points from hi to lo for the estimation
	fit1: Type of fit - mlefit or mmefit
	mt1: Mirror xform - True or False
	"""

	global x, fit, mt, c, max_of_x

	## Initialize globals prior to the parallel run
	##
	
	x = x1
	max_of_x = max(x)
	fit = fit1
	mt = mt1
	c = util.ecdf(x)
	
	xmax_pts = util.gen_points(lo, hi, n)
	l_xmax_pts = xmax_pts.tolist()
	l_xmax_pts.append(max_of_x)
	l_xmax_pts.sort()
	xmax_pts = np.array(l_xmax_pts)

	ncpus = mp.cpu_count()
	proc_pool = Pool(ncpus)
	result = proc_pool.map(optfit, xmax_pts)
	
	# definitions to compare fit and k-s values
	# 2 = index of k-s metric in each tuple of the result
	# 3 = index of fit metric in each tuple of the result
	# !!! REMOVING KS COMP !!!
	FIT_COMP_IDX = 2
	# KS_COMP_IDX = 3
	DIFF_COMP_IDX = 3

	return {"fit": best_fit(result, FIT_COMP_IDX), "diff": best_fit(result, DIFF_COMP_IDX)}

def main():
	input_file = None
	lo = None
	hi = None
	n = None
	x1 = None
	fit1 = None
	mt1 = None

	
	try:
		opts, args = getopt.getopt(sys.argv[1:], "f:l:h:n:t:m:")
		for o, a in opts:
			if o == "-f":
				input_file = a
			elif o == "-l":
				lo = float(a)
			elif o == "-h":
				hi = float(a)
			elif o == "-n":
				n = int(a)
			elif o == "-t":
				fit1 = a.lower()
			elif o == "-m":
				smt = a.lower()
				if smt == "true":
					mt1 = True
				elif smt == "false":
					mt1 = False
				else:
					usage()
					sys.exit(2)
			else:
				usage()
				sys.exit(2)
	except getopt.GetoptError, opt_err:
		print str(opt_err)
		usage()
		sys.exit(2)
	
	if input_file == None or lo == None or hi == None or n == None or fit1 == None or mt1 == None:
		usage()
		sys.exit(2)

	x1 = util.read_data(input_file)
	x1.sort()

	rs = paroptfit(x1, hi, lo, n, fit1, mt1)

	print rs

	## xmax_pts = util.gen_points(lo, hi, n)

	## ncpus = mp.cpu_count()
	## proc_pool = Pool(ncpus)
	## result = proc_pool.map(optfit, xmax_pts)

	# definitions to compare fit and k-s values
	# 2 = index of k-s metric in each tuple of the result
	# 3 = index of fit metric in each tuple of the result
	## FIT_COMP_IDX = 2
	## KS_COMP_IDX = 3
	## print "Best FIT fit:", best_fit(result, FIT_COMP_IDX)
	## print "Best K-S fit:", best_fit(result, KS_COMP_IDX)

if __name__ == "__main__":
	main()

