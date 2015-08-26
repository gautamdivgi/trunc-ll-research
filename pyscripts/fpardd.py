#! /usr/bin/python

import sys
import rpytools.util as util
import fparmlfit
import numpy as np
import math
import rpytools.modlav as ml
import scipy.stats.mstats as ms
import time

def usage():
	print "usage: npardd.py <file1, [file2], [file3],...>"

def pardd(x1):
	
	xmx = x1.max()

	n = 500
	lo = 0.1*xmx
	hi = 10*xmx

	omle = fparmlfit.paroptfit(x1, hi, lo, n, "mlefit", False)
	omle_mt = fparmlfit.paroptfit(x1, hi, lo, n, "mlefit", True)
	omme = fparmlfit.paroptfit(x1, hi, lo, n, "mmefit", False)
	omme_mt = fparmlfit.paroptfit(x1, hi, lo, n, "mmefit", True)

	fitlist = [("MLE-OPT", omle), \
				  ("MLE-OPT-MT", omle_mt), \
				  ("MME-OPT", omme), \
				  ("MME-OPT-MT", omme_mt)]
	
	bfit = fitlist[0]
	minfm = fitlist[0][1][2]
	for f in fitlist:
		fm = f[1][2]
		if fm < minfm:
			minfm = fm
			bfit = f

	# 0: The name of the fit
	# [1][0]: The distribution
	# [1][2]: The fit metric
	return bfit

		
