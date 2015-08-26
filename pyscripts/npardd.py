#! /usr/bin/python

import sys
import rpytools.util as util
import parmlfit
import numpy as np
import math
import rpytools.modlav as ml
import scipy.stats.mstats as ms
import time

def usage():
	print "usage: npardd.py <file1, [file2], [file3],...>"

def pardd(fname):
	
	inpf = fname
	x1 = util.read_data(inpf)
	x1.sort()
	xmx = x1.max()

	n = 500
	lo = 0.1*xmx
	hi = 10*xmx

	ccf = inpf + "_ccdf"
	ecf = inpf + "_ecdf"

	cc = util.ccdf(x1)
	ec = util.ecdf(x1)

	util.write_data(ccf, cc)
	util.write_data(ecf, ec)

	# Moved the xmx into calculation for the optimized set. That way a specialized piece is not needed here.
	# mle = ml.ModLav.fromFit(x1, fit="mlefit")
	# mme = ml.ModLav.fromFit(x1, fit="mmefit")
	# mle_mt = ml.ModLav.fromFit(x1, fit="mlefit", mt=True)
	# mme_mt = ml.ModLav.fromFit(x1, fit="mmefit", mt=True)

	# no_mle = (mle, xmx, mle.fitmetric(cdf=ec), mle.ksmetric(cdf=ec), mle.difference(cdf=ec))
	# no_mme = (mme, xmx, mme.fitmetric(cdf=ec), mme.ksmetric(cdf=ec), mme.difference(cdf=ec))
	# no_mle_mt = (mle_mt, xmx, mle_mt.fitmetric(cdf=ec), mle_mt.ksmetric(cdf=ec), mle_mt.difference(cdf=ec))
	# no_mme_mt = (mme_mt, xmx, mme_mt.fitmetric(cdf=ec), mme_mt.ksmetric(cdf=ec), mme_mt.difference(cdf=ec))

	omle = parmlfit.paroptfit(x1, hi, lo, n, "mlefit", False)
	omle_mt = parmlfit.paroptfit(x1, hi, lo, n, "mlefit", True)
	omme = parmlfit.paroptfit(x1, hi, lo, n, "mmefit", False)
	omme_mt = parmlfit.paroptfit(x1, hi, lo, n, "mmefit", True)

	mle_opt = omle["fit"]
	mle_opt_mt = omle_mt["fit"]
	mme_opt = omme["fit"]
	mme_opt_mt = omme_mt["fit"]
	
	# Not using K-S metric any more. Remove
	# k_mle_opt = omle["ks"]
	# k_mle_opt_mt = omle_mt["ks"]
	# k_mme_opt = omme["ks"]
	# k_mme_opt_mt = omme_mt["ks"]
	
	d_mle_opt = omle["diff"]
	d_mle_opt_mt = omle_mt["diff"]
	d_mme_opt = omme["diff"]
	d_mme_opt_mt = omme_mt["diff"]

	fitlist = [("MLE-OPT", mle_opt), \
				  ("MLE-OPT-MT", mle_opt_mt), \
				  ("MME-OPT", mme_opt), \
				  ("MME-OPT-MT", mme_opt_mt), \
				  ("D-MLE-OPT", d_mle_opt), \
				  ("D-MLE-OPT-MT", d_mle_opt_mt), \
				  ("D-MME-OPT", d_mme_opt), \
				  ("D-MME-OPT-MT", d_mme_opt_mt)]

	n,amin,amax,mu,sigma = len(x1), x1.min(), xmx, x1.mean(), x1.std()
	cv = sigma/mu
	q = ms.mquantiles(x1, [0.1, 0.5, 0.9])
	
	op1_str = []
	op_str = []
	op_str.append("BASIC STATISTICS")
	op_str.append("--------------------------------------------------------------------------")
	op_str.append("Size: " + str(n))
	op_str.append("Range: " + str(amin) + " - " + str(amax))
	op_str.append("Quantiles: 10% - " + str(q[0]) + " 50% - " + str(q[1]) + " 90% - " + str(q[2]))
	op_str.append("Mean: " + str(mu))
	op_str.append("Sigma: " + str(sigma))
	op_str.append("CV: " + str(cv))
	op_str.append("\n")
	
	best_fit_map = dict()

	for f in fitlist:
		lbl = f[0]
		m = f[1][0]
		mx = f[1][1]
		fitm = f[1][2]
		## ksm = f[1][3]
		diffm = f[1][3]

		best_fit_map[lbl] = (m, mx, fitm, diffm)

		op_str.append(lbl)
		op_str.append("--------------------------------------------------------------------------")
		op_str.append("Modlav params: " + str(m))
		op_str.append("Xmax: " + str(mx))
		op_str.append("Xmax/Max: " + str(mx/xmx))
		## op_str.append("FIT Metric: " + str(m.fitmetric(points = x1)))
		## op_str.append("K-S Metric: " + str(m.ksmetric(points = x1)))
		op_str.append("FIT Metric: " + str(fitm))
		## op_str.append("K-S Metric: " + str(ksm))
		op_str.append("DIFF Metric: " + str(diffm))
		op_str.append("--------------------------------------------------------------------------")
		op_str.append("\n")

		flbl = lbl.lower().replace("-", "_")
		fname_pfx = inpf + "_" + flbl

		lx = util.gen_points(math.log10(x1.min()), math.log10(mx), 2000)
		ex = np.power(10, lx)

		mcc = m.ccdf(ex)
		mec = m.cdf(ec[:,0])

		fmcc = np.array([ex, mcc]).transpose()
		fmec = np.array([ec[:,0], mec]).transpose()

		util.write_data(fname_pfx + "_ccdf", fmcc)
		util.write_data(fname_pfx + "_ecdf", fmec)

	recom = best_fit(best_fit_map, xmx)
	for s1 in op_str:
		op1_str.append(s1 + "\n")
	op1_str.append("RECOMMENDATIONS: " + str(recom) + "\n")

	txf = open(inpf + "_metric", "w+")
	txf.writelines(op1_str)
	txf.close()
	
def best_fit(fit_map, xmx):
	l = fit_map.items()

	# ks_idx = 3
	fit_idx = 2
	dif_idx = 3
	
	# Best K-S fit
	# best_ks_fit = None
	# for d in l:
	# 	lbl = d[0]
	# 	params = d[1]
	# 	if best_ks_fit == None:
	# 		best_ks_fit = lbl
	# 	else:
	# 		curr_ks = fit_map[best_ks_fit][ks_idx]
	# 		new_ks = params[ks_idx]
	# 		if new_ks < curr_ks:
	# 			best_ks_fit = lbl

	# Best fit metric
	best_fit_fit = None
	for d in l:
		lbl = d[0]
		params = d[1]
		if best_fit_fit == None:
			best_fit_fit = lbl
		else:
			curr_fit = fit_map[best_fit_fit][fit_idx]
			new_fit = params[fit_idx]
			if new_fit < curr_fit:
				best_fit_fit = lbl

	# Best fit metric for the extreme tail
	# best_fit_no_opt = None
	# if fit_map[best_fit_fit][1]/float(xmx) < 1.0:
	# 	for d in l:
	# 		lbl = d[0]
	# 		if lbl.find("OPT") > -1:
	# 			continue
	# 		else:
	# 			params = d[1]
	# 			if best_fit_no_opt == None:
	# 				best_fit_no_opt = lbl
	# 			else:
	# 				curr_fit = fit_map[best_fit_no_opt][fit_idx]
	# 				new_fit = params[fit_idx]
	# 				if new_fit < curr_fit:
	# 					best_fit_no_opt = lbl
		
	# Best diff metric
	best_dif_fit = None
	for d in l:
		lbl = d[0]
		params = d[1]
		if best_dif_fit == None:
			best_dif_fit = lbl
		else:
			curr_fit = fit_map[best_dif_fit][dif_idx]
			new_fit = params[dif_idx]
			if new_fit < curr_fit:
				best_dif_fit = lbl

	# Best diff metric for the extreme tail
	# best_dif_no_opt = None
	# if fit_map[best_dif_fit][1]/float(xmx) < 1.0:
	# 	for d in l:
	# 		lbl = d[0]
	# 		if lbl.find("OPT") > -1:
	# 			continue
	# 		else:
	# 			params = d[1]
	# 			if best_dif_no_opt == None:
	# 				best_dif_no_opt = lbl
	# 			else:
	# 				curr_fit = fit_map[best_dif_no_opt][dif_idx]
	# 				new_fit = params[dif_idx]
	# 				if new_fit < curr_fit:
	# 					best_dif_no_opt = lbl

	# return (best_ks_fit, best_fit_fit, best_fit_no_opt, best_dif_fit, best_dif_no_opt)
	return (best_fit_fit, best_dif_fit)

def main():
	if len(sys.argv) < 2:
		usage()
		sys.exit(2)
	
	n = len(sys.argv)
	for i in xrange(1,n):
		print "processing " + sys.argv[i] + " ..."
		pardd(sys.argv[i])
		print "sleeping for 60 seconds..."
		if i < n-1:
			time.sleep(60)

if __name__ == "__main__":
	main()
