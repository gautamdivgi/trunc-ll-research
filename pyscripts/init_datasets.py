import rpytools.datasets as dsets
import sqlite3
import atexit
import datetime as dt
import rpytools.util as util
import os
import fpardd
import rpytools.lognormal as logn
import rpytools.tpareto as tpar
import rpytools.modlav as ml

gFdbConnection = None


def closeConnection():
	global gFdbConnection
	if gFdbConnection != None:
		try:
			gFdbConnection.rollback()
		except BaseException as be:
			pass
		
		try:
			gFdbConnection.close()
		except BaseException as be:
			pass

def getConnection():
	global gFdbConnection
	if gFdbConnection == None:
		gFdbConnection = sqlite3.connect("/home/gautam/dbs/files_and_analysis.db")
		atexit.register(closeConnection)
	return gFdbConnection


def validateEntry(entry):
	tag = entry["tag"]
	fname = entry["filename"]
	r = os.access(fname, os.R_OK)
	print "\t\t Existence of " + tag + "[" + fname + "]: ", str(r)
	return r

def insertEntry(entry):
	c = getConnection()
	t = (entry["tag"], entry["filename"], entry["description"])
	q = "insert into datasets(unique_id, filename, description) values(?, ?, ?)"

	tag = entry["tag"]
	fname = entry["filename"]

	try:
		print "\t\t Inserting base entry for " + tag + "[" + fname + "]"
		c.execute(q, t)
		c.commit()
		print "\t\t OK"
	except BaseException as be:
		c.rollback()
		print "\t\t FAILED"

def computeBasicStats(entry):
	tag = entry["tag"]
	fname = entry["filename"]
	x = util.read_data(fname)
	x.sort()
	s = util.get_stats(x)
	
	t = (entry["tag"], s["size"], s["min"], s["max"], s["pct10"], s["pct50"], s["pct90"], s["mu"], s["sigma"], s["cv"])
	q = "insert into basic_stats(unique_id, size, min, max, pct10, pct50, pct90, mu, sdev, cv) values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
	c = getConnection()
	try:
		print "\t\t Inserting basic stats for " + tag + "[" + fname + "]"
		c.execute(q, t)
		c.commit()
		print "\t\t OK"
	except BaseException as be:
		c.rollback()
		print "\t\t FAILED"

def initializeTransaction(entry_tag):
	q1 = "delete from fits where unique_id = '" + entry_tag + "'"
	q2 = "delete from basic_stats where unique_id = '" + entry_tag + "'"
	q3 = "delete from datasets where unique_id = '" + entry_tag + "'"
	
	c = getConnection()
	try:
		print "\t\t Initializing - deleting all data"
		c.execute(q1)
		c.execute(q2)
		c.execute(q3)
		c.commit()
		print "\t\t OK"
	except BaseException as be:
		c.rollback()
		print "\t\t FAILED"
		raise(be)

def computeTparetoFit(tag, x, ecdf, ccdf):
	t = tpar.TPareto.fromFit(x)
	q = t.fitmetric(points=x)
	k = t.ksmetric(points=x)

	iq1 = "insert into fits(unique_id, distribution, type, pname_1, pvalue_1, pname_2, pvalue_2, pname_3, pvalue_3, q_fit, ks_fit) " + \
			"values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
	
	c = getConnection()
	iv1 = (tag, "TPARETO", "MLE", "k", t.k(), "m", t.m(), "alpha", t.alpha(), q, k)
	try:
		print "\t\t Inserting Tpareto fits for " + tag
		c.execute(iq1, iv1)
		c.commit()
		print "\t\t OK"
	except BaseException as be:
		c.rollback()
		print "\t\t FAILURE"
		raise(be)

def computeLogLogisticFit(tag, x, ecdf, ccdf):
	ll_mle = ml.ModLav.fromFit(x,fit="mlefitll")
	q_mle = ll_mle.fitmetric(points=x)
	ll_mle_mt = ml.ModLav.fromFit(x,fit="mlefitll",mt=True)
	q_mle_mt = ll_mle_mt.fitmetric(points=x)

	l1 = None
	ftype1 = None
	q1 = None

	if ( q_mle < q_mle_mt ):
		l1 = ll_mle
		ftype1 = "MLE"
		q1 = q_mle
	else:
		l1 = ll_mle_mt
		ftype1 = "MLE-MT"
		q1 = q_mle_mt

	ll_fmin = ml.ModLav.fromFit(x,fit="fitminll")
	q_fmin = ll_fmin.fitmetric(points=x)
	ll_fmin_mt = ml.ModLav.fromFit(x,fit="fitminll",mt=True)
	q_fmin_mt = ll_fmin_mt.fitmetric(points=x)

	l2 = None
	ftype2 = None
	q2 = None

	if ( q_fmin < q_fmin_mt ):
		l2 = ll_fmin
		ftype2 = "FITMIN"
		q2 = q_fmin
	else:
		l2 = ll_fmin_mt
		ftype2 = "FITMIN-MT"
		q2 = q_fmin_mt

	l = None
	ftype = None
	q = None

	if ( q1 < q2 ):
		l = l1
		ftype = ftype1
		q = q1
	else:
		l = l2
		ftype = ftype2
		q = q2

	k = l.ksmetric(points=x)

	iq1 = "insert into fits(unique_id, distribution, type, pname_1, pvalue_1, pname_2, pvalue_2, q_fit, ks_fit) " + \
			"values(?, ?, ?, ?, ?, ?, ?, ?, ?)"

	c = getConnection()
	iv1 = (tag, "LOGLOGISTIC", ftype, "beta", l.beta(), "c", l.c(), q, k)
	try:
		print "\t\t Inserting LogLogistic fits for " + tag
		c.execute(iq1, iv1)
		c.commit()
		print "\t\t OK"
	except BaseException as be:
		c.rollback()
		print "\t\t FALURE"
		raise(be)

def computeModLavFit(tag, x, ecdf, ccdf):
	mopt_all = fpardd.pardd(x)
	opt_type = mopt_all[0]
	mopt = mopt_all[1][0]
	qopt = mopt_all[1][2]
	try:
		if ( qopt == float('Inf') ):
			mmin1 = ml.ModLav.fromFit(x, fit="fitmin", mt=True)
		else:
			mmin1 = ml.ModLav.fromFit(x, fit="fitmin", mt=True, beta=mopt.beta(), c=mopt.c(), d=mopt.d())
		qmin1 = mmin1.fitmetric(points=x)
	except BaseException as be1:
		mmin1 = None
		qmin1 = float('Inf')

	try:
		if ( qopt == float('Inf') ):
			mmin2 = ml.ModLav.fromFit(x, fit="fitmin")
		else:
			mmin2 = ml.ModLav.fromFit(x, fit="fitmin", beta=mopt.beta(), c=mopt.c(), d=mopt.d())
		qmin2 = mmin2.fitmetric(points=x)
	except BaseException as be2:
		mmin2 = None
		qmin2 = float('Inf')

	if ( qmin1 == float('Inf') and qmin2 == float('Inf') ):
		print "\t\t NO TRUNCLL for - ", tag
		print "\t\t BOTH FITS ARE NOT VALID"
		return

	mmin = mmin1
	qmin = qmin1
	fitmin_tag = "FITMIN-MT"
	if qmin2 < qmin1:
		fitmin_tag = "FITMIN"
		mmin = mmin2
		qmin = qmin2
	
	k = mmin.ksmetric(points=x)
	k1 = mopt.ksmetric(points=x)
	iq1 = "insert into fits(unique_id, distribution, type, pname_1, pvalue_1, pname_2, pvalue_2, pname_3, pvalue_3, q_fit, ks_fit) " + \
			"values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
	
	iv1 = (tag, "TRUNCLL", opt_type, "beta", mopt.beta(), "c", mopt.c(), "d", mopt.d(), qopt, k1)
	iv2 = (tag, "TRUNCLL", fitmin_tag, "beta", mmin.beta(), "c", mmin.c(), "d", mmin.d(), qmin, k)

	c = getConnection()
	try:
		print "\t\t Inserting TruncLogLogistic fits for " + tag
		c.execute(iq1, iv1)
		c.execute(iq1, iv2)
		c.commit()
		print "\t\t OK"
	except BaseException as be:
		c.rollback()
		print "\t\t FAILURE"
		raise(be)


def computeLognormalFit(tag, x, ecdf, ccdf):
	lmme = logn.Lognormal.fromFit(x)
	lmle = logn.Lognormal.fromFit(x, mmefit=False)

	try:
		lfit = logn.Lognormal.fromFit(x, True, True)
		qfit = lfit.fitmetric(points=x)
	except BaseException as be:
		print "Lognormal FITMIN error --> ", str(be)
		qfit = float('Inf')

	qmme = lmme.fitmetric(points=x)
	qmle = lmle.fitmetric(points=x)

	l = None
	q = None
	ftype = None

	if ( qmme < qmle ):
		l = lmme
		q = qmme
		ftype = "MME"
	else:
		l = lmle
		q = qmle
		ftype = "MLE"

	if q > qfit:
		l = lfit
		q = qfit
		ftype = "FITMIN"

	k = l.ksmetric(points=x)
	
	iqdel = "delete from fits where unique_id = ? and distribution = ?"
	iq1 = "insert into fits(unique_id, distribution, type, pname_1, pvalue_1, pname_2, pvalue_2, q_fit, ks_fit) " + \
			"values(?, ?, ?, ?, ?, ?, ?, ?, ?)"

	c = getConnection()
	try:
		print "\t\t Inserting logn fits for " + tag 
		c.execute(iqdel, (tag, "LOGN"))
		c.execute(iq1, (tag, "LOGN", ftype, "mu", l.mu(), "sigma", l.sigma(), q, k))
		c.commit()
		print "\t\t OK"
	except BaseException as be:
		c.rollback()
		print "\t\t FAILURE"
		raise(be)


def computeFits(entry):
	tag = entry["tag"]
	fname = entry["filename"]

	x = util.read_data(fname)
	x_ecdf = util.read_data(fname + "_ecdf")
	x_ccdf = util.read_data(fname + "_ccdf")
	x.sort()

	computeLognormalFit(tag, x, x_ecdf, x_ccdf)
	#computeTparetoFit(tag, x, x_ecdf, x_ccdf)
	#computeLogLogisticFit(tag, x, x_ecdf, x_ccdf)
	#computeModLavFit(tag, x, x_ecdf, x_ccdf)


def validateAndInsertFiles():
	for dset in dsets.DATASETS:
		for entry in dset:
			# print "Removing old data - ", entry["tag"]
			# initializeTransaction(entry["tag"])
			print "Validating entry - ", entry["tag"]
			if validateEntry(entry) == True:
				# print "\t Inserting entry - ", entry["tag"]
				# insertEntry(entry)
	
				# print "\t Computing basic stats for - ", entry["tag"]
				# computeBasicStats(entry)
	
				print "\t Computing FITs for - ", entry["tag"]
				computeFits(entry)
			else:
				print "NOT VALID - ", entry["tag"]

if __name__ == "__main__":
	print "Processing datasets..."
	validateAndInsertFiles()
