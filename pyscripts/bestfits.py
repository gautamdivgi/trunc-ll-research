from rpytools.sql import *
from os import getenv
from os import path
import math
from rpytools.modlav import ModLav
from rpytools.tpareto import TPareto
from rpytools.lognormal import Lognormal
import numpy as np
from rpytools.util import read_data
from rpytools.util import ecdf
from rpytools.util import write_data
from rpytools.util import gen_points


def get_dist(dset_id, dname):
	q = "select distribution, pname_1, pvalue_1, pname_2, pvalue_2, pname_3, pvalue_3 from fits" + \
		  " where unique_id = '" + dset_id + "' and" + \
		  " distribution = '" + dname + "'"

	r = RunSQL("files_and_analysis.db")
	dist_row = r.sqlq(q)
	dist = dist_row[0]
	
	pname_1 = dist[1]
	pvalue_1 = dist[2]
	pname_2 = dist[3]
	pvalue_2 = dist[4]
	pname_3 = dist[5]
	pvalue_3 = dist[6]

	params = dict()
	if ( pname_1 != None and pvalue_1 != None ):
		params[pname_1] = pvalue_1
	if ( pname_2 != None and pvalue_2 != None ):
		params[pname_2] = pvalue_2
	if ( pname_3 != None and pvalue_3 != None ):
		params[pname_3] = pvalue_3

	if ( dname == "LOGLOGISTIC" ):
		return ModLav(params["beta"], params["c"], 0.0)
	elif ( dname == "TRUNCLL" ):
		return ModLav(params["beta"], params["c"], params["d"])
	elif ( dname == "LOGN" ):
		return Lognormal(params["mu"], params["sigma"])
	elif ( dname == "TPARETO" ):
		return TPareto(params["k"], params["m"], params["alpha"])
	else:
		return None



def gen_cdf_ccdf():
	r = RunSQL("files_and_analysis.db")
	dsets = r.sqlq("select unique_id, filename from datasets")

	for dpair in dsets:
		dset_id = dpair[0]
		dset_file = dpair[1]

		print "Processing data set - ", dset_id

		x = read_data(dset_file)
		x.sort()
		ec = ecdf(x, issorted=True)
		pts = np.power(10, gen_points(math.log10(min(x)), math.log10(max(x)), 2000))
		
		# dist_list = ["LOGLOGISTIC", "LOGN", "TPARETO", "TRUNCLL"]
		dist_list = ["LOGN"]
		fext_map = {"LOGLOGISTIC": "ll", "LOGN": "lgn", "TPARETO": "tp", "TRUNCLL": "tll"}

		for distname in dist_list:
			print "\t Getting distribution - ", distname
			dist = get_dist(dset_id, distname)
			dec = dist.cdf(ec[:,0])
			dcc = dist.ccdf(pts)

			fdec = np.array([ec[:,0], dec]).transpose()
			fdcc = np.array([pts, dcc]).transpose()

			op_dir = os.path.dirname(dset_file)
			op_ec_file = op_dir + "/" + os.path.basename(dset_file)+"_ecdf" + "." + fext_map[distname]
			op_cc_file = op_dir + "/" + os.path.basename(dset_file)+"_ccdf" + "." + fext_map[distname]
			
			print "\t Writing CDF - ", op_ec_file
			write_data(op_ec_file, fdec)

			print "\t Writing CCF - ", op_cc_file
			write_data(op_cc_file, fdcc)




def get_bestfits():
	r = RunSQL("files_and_analysis.db")
	dsets = r.sqlq("select unique_id from datasets")

	for dset in dsets:
		q = "select distribution, type, q_fit, ks_fit from fits where unique_id = '" + dset + "' order by q_fit"
		f = r.sqlq(q)
		if ( f == None or len(f) == 0 ):
			continue
		fbest = f[0]

		print "********************* DATA SET " + dset + " *********************************"
		print "BEST FIT: " + fbest[0]
		print "\t FIT-ALG: " + fbest[1]
		print "\t FIT-METRIC: " + str(fbest[2])
		print "\t KS-METRIC: " + str(fbest[3])
		
		tllfit = None
		llfit = None
		lognfit = None
		for f1 in f:
			if ( f1[0] == "TRUNCLL" ):
				tllfit = f1
			if ( f1[0] == "LOGLOGISTIC" ):
				llfit = f1
			if ( f1[0] == "LOGN" ):
				lognfit = f1
		
		if ( fbest[0] != tllfit[0] ):
			print
			print "TRUNC-LL FIT: " + tllfit[0]
			print "\t FIT-ALG: " + tllfit[1]
			print "\t FIT-METRIC: " + str(tllfit[2])
			print "\t KS-METRIC: " + str(tllfit[3])

		if ( fbest[0] != llfit[0] ):
			print
			print "LL FIT: " + llfit[0]
			print "\t FIT-ALG: " + llfit[1]
			print "\t FIT-METRIC: " + str(llfit[2])
			print "\t KS-METRIC: " + str(llfit[3])
		
		if ( fbest[0] != lognfit[0] ):
			print
			print "LL FIT: " + lognfit[0]
			print "\t FIT-ALG: " + lognfit[1]
			print "\t FIT-METRIC: " + str(lognfit[2])
			print "\t KS-METRIC: " + str(lognfit[3])
		print
		print
				


if __name__ == "__main__":
	## get_bestfits()
	gen_cdf_ccdf()
