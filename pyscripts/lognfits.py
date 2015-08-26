#! /usr/bin/python

import rpytools.datasets as dsets
import sqlite3
import atexit
import datetime as dt
import rpytools.util as util
import os
import rpytools.lognormal as logn
import shutil
import math
import numpy as np
import rpytools.plotdata as pdata
from matplotlib import pyplot as plt

db_conn = None
main_dir = "research/logn_fits"
plots_dir = "plots"

def close_connection():
	global db_conn
	print "closing connection..."
	if db_conn != None:
		try:
			db_conn.rollback()
		except BaseException as be:
			pass

		try:
			db_conn.close()
		except BaseException as be:
			pass

def get_connection():
	global db_conn
	if db_conn == None:
		db_path = os.path.join(os.getenv("TRACE_DB_LOC"), "logn_fits.db")
		db_conn = sqlite3.connect(db_path)
		atexit.register(close_connection)

	return db_conn

def prepare_directory():
	"""
	Step 1: Clean the directory
	Step 2: For every data set copy the base data to this directory
	"""
	
	full_proc_path = os.path.join(os.getenv("HOME"), main_dir)
	if os.access(full_proc_path, os.X_OK):
		print "Directory ", full_proc_path, " exists, removing..."
		shutil.rmtree(full_proc_path)

	print "Creating directory ", full_proc_path
	os.mkdir(full_proc_path)

	tag_file_map = {}

	for dset in dsets.DATASETS:
		for entry in dset:
			tag = entry["tag"]
			fname = entry["filename"]
			if os.access(fname, os.R_OK):
				set_name = os.path.basename(fname)
				from_file = fname
				to_file = os.path.join(full_proc_path, tag.lower())
				print "Copying ", from_file, " to ", to_file
				shutil.copyfile(from_file, to_file)
				tag_file_map[tag] = to_file

	return tag_file_map

def best_fits(fit_map):
	
	lmme = fit_map["MME"][0]
	lmle = fit_map["MLE"][0]
	lfit = fit_map["FITMIN"][0]

	ksmme = fit_map["MME"][1]
	ksmle = fit_map["MLE"][1]
	ksfit = fit_map["FITMIN"][1]

	qmme = fit_map["MME"][2]
	qmle = fit_map["MLE"][2]
	qfit = fit_map["FITMIN"][2]

	btype = "MME"
	ks = ksmme

	ttype = "MME"
	q = qmme

	if ksmle < ks: 
		btype = "MLE"
		ks = ksmle
	
	if ksfit < ks:
		btype = "FITMIN"
		ks = ksfit

	if qmle < q:
		ttype = "MLE"
		q = qmle

	if qfit < q:
		ttype = "FITMIN"
		q = qfit

	return {"best_body": btype, "best_tail": ttype}


def process_datasets(tag_file_map):

	tags = tag_file_map.keys()
	report_map = {}
	for tag in tags:
		data_file = tag_file_map[tag]
		x = util.read_data(data_file)
		x.sort()
		ec = util.ecdf(x)
		cc = util.ccdf(x)

		fit_map = compute_fits(x)
		insert_db_record(tag, fit_map)

		## Figure out best fit
		bfit = best_fits(fit_map)
		report_map[tag] = (bfit["best_body"], bfit["best_tail"])
		
		## Write files out to the directory
		util.write_data(data_file + "_ecdf", ec)
		util.write_data(data_file + "_ccdf", cc)

		ccpts = np.power(10, util.gen_points(math.log10(min(x)), math.log10(max(x)), 2000))	
		ecpts = ec[:,0]

		lmme = fit_map["MME"][0]
		lmle = fit_map["MLE"][0]
		lfit = fit_map["FITMIN"][0]

		mme_ec = np.array([ecpts, lmme.cdf(ecpts)]).transpose()
		mme_cc = np.array([ccpts, lmme.ccdf(ccpts)]).transpose()
		util.write_data(data_file + "_ecdf.lognmme", mme_ec)
		util.write_data(data_file + "_ccdf.lognmme", mme_cc)

		mle_ec = np.array([ecpts, lmle.cdf(ecpts)]).transpose()
		mle_cc = np.array([ccpts, lmle.ccdf(ccpts)]).transpose()
		util.write_data(data_file + "_ecdf.lognmle", mle_ec)
		util.write_data(data_file + "_ccdf.lognmle", mle_cc)

		fit_ec = np.array([ecpts, lfit.cdf(ecpts)]).transpose()
		fit_cc = np.array([ccpts, lfit.ccdf(ccpts)]).transpose()
		util.write_data(data_file + "_ecdf.lognfitmin", fit_ec)
		util.write_data(data_file + "_ccdf.lognfitmin", fit_cc)

	for k in report_map:
		print k + " BODY: " + report_map[k][0] + " TAIL: " + report_map[k][1]

	return report_map

def create_plots(tag_file_map, report_map):
	dset_list = (pdata.sim_dataset_list, pdata.web_dataset_list, pdata.azu_dataset_list, pdata.unc_dataset_list)
	for dset1 in dset_list:
		for dset in dset1:
			create_single_plot(tag_file_map, report_map, dset)

def create_single_plot(tag_file_map, report_map, dset):
	plt.interactive(False)
	plt.rcParams['font.size'] = 17.0

	dist_params = pdata.dist_map["LOGN"]
	ext = dist_params["ext"]
	typ = dset["type"]

	tag = dset["tag"]

	bfit = report_map[tag][0]
	tfit = report_map[tag][1]

	if bfit == tfit:
		l1 = dset["legend1"]
		l2 = "Body & tail: LOGN-" + bfit

		if typ == "cdf":
			p1 = util.read_data(tag_file_map[tag] + "_ecdf")
			p2 = util.read_data(tag_file_map[tag] + "_ecdf.logn" + bfit.lower())
			plt.plot(p1[:,0], p1[:,1], 'k-', label=l1)
			plt.plot(p2[:,0], p2[:,1], 'k--', label=l2)
		else:	
			p1 = util.read_data(tag_file_map[tag] + "_ccdf")
			p2 = util.read_data(tag_file_map[tag] + "_ccdf.logn" + bfit.lower())
			plt.loglog(p1[:,0], p1[:,1], 'k-', label=l1)
			plt.loglog(p2[:,0], p2[:,1], 'k--', label=l2)
	else:
		l1 = dset["legend1"]
		l2 = "Body: LOGN-" + bfit
		l3 = "Tail: LOGN-" + tfit

		if typ == "cdf":
			p1 = util.read_data(tag_file_map[tag] + "_ecdf")
			p2 = util.read_data(tag_file_map[tag] + "_ecdf.logn" + bfit.lower())
			p3 = util.read_data(tag_file_map[tag] + "_ecdf.logn" + tfit.lower())
			plt.plot(p1[:,0], p1[:,1], 'k-', label=l1)
			plt.plot(p2[:,0], p2[:,1], 'k-.', label=l2)
			plt.plot(p3[:,0], p3[:,1], 'k--', label=l3)
		else:
			p1 = util.read_data(tag_file_map[tag] + "_ccdf")
			p2 = util.read_data(tag_file_map[tag] + "_ccdf.logn" + bfit.lower())
			p3 = util.read_data(tag_file_map[tag] + "_ccdf.logn" + tfit.lower())
			plt.loglog(p1[:,0], p1[:,1], 'k-', label=l1)
			plt.loglog(p2[:,0], p2[:,1], 'k-.', label=l2)
			plt.loglog(p3[:,0], p3[:,1], 'k--', label=l3)
	
	loc = dset["loc"]

	if "xlim" in dset:
		plt.xlim(dset["xlim"])
	if "ylim" in dset:
		plt.ylim(dset["ylim"])
	if "xticks" in dset:
		plt.xticks(dset["xticks"])
	if "yticks" in dset:
		plt.yticks(dset["yticks"])
	plt.grid()
	plt.xlabel(dset["xlabel"])
	plt.ylabel(dset["ylabel"])
	plt.legend(loc=loc, frameon=False)

	eps_file = tag.lower() + "_" + typ + "_" + ext + ".eps"
	plot_path = os.path.join(os.getenv("HOME"), main_dir)
	plot_file = os.path.join(plot_path, eps_file)

	if os.access(plot_file, os.R_OK):
		os.remove(plot_file)

	plt.savefig(plot_file)
	plt.close()


def compute_fits(x):

		# MME fit
		print "\t Computing MME fit..."
		lmme = logn.Lognormal.fromFit(x,True)
		lmme_ks = lmme.ksmetric(points=x)
		lmme_q = lmme.fitmetric(points=x)

		# MLE fit
		print "\t Comptuing MLE fit..."
		lmle = logn.Lognormal.fromFit(x,False)
		lmle_ks = lmle.ksmetric(points=x)
		lmle_q = lmle.fitmetric(points=x)

		# Fitmin
		print "\t Computing FITMIN fit..."
		lfit = logn.Lognormal.fromFit(x,True,True)
		lfit_ks = lfit.ksmetric(points=x)
		lfit_q = lfit.fitmetric(points=x)

		return {"MME": (lmme, lmme_ks, lmme_q), "MLE": (lmle, lmle_ks, lmle_q), "FITMIN": (lfit, lfit_ks, lfit_q)}

def insert_db_record(unique_id, fit_map):
	q_del = "delete from logn_fits where unique_id = ? and type = ?"
	q_ins = "insert into logn_fits(unique_id, type, ks_fit, q_fit, mu, sigma) values (?, ?, ?, ?, ?, ?)"

	try:
		print "\t Inserting record for " + unique_id
		c = get_connection()

		print "\t\t Deleting existing record..."
		for ftype in fit_map.keys():
			print "\t\t Adding record for ", ftype
			(l,ks,q) = fit_map[ftype]
			c.execute(q_del, (unique_id, ftype))
			c.execute(q_ins, (unique_id, ftype, ks, q, l.mu(), l.sigma()))
			c.commit()
	except BaseException as be:
		c.rollback()
		raise (be)



def main():
	tag_file_map = prepare_directory()
	report_map = process_datasets(tag_file_map)
	create_plots(tag_file_map, report_map)

if __name__ == "__main__":
	main()

