#! /usr/bin/python

from os import getenv
from rpytools.util import write_data
from rpytools.util import remove_outliers
from rpytools.sql import RunSQL
import numpy as np

def get_day_list():
	return [13,14,15,16,17,18,19,20]

def get_output_dir(data_type):
	return getenv("HOME") + "/research/ml_data/unc/" + data_type

## Inter-arrival across sessions
def create_ses_inter():
	dl = get_day_list()
	r = RunSQL("unc.db")
	
	for d in dl:
		q = "select ts from flows where day = " + str(d) + " and term > 1 order by ts"
		print "Running query for day - ", str(d)
		ts = np.array(r.sqlq(q))
		n = len(ts)
		its = ts[1:n] - ts[0:n-1]
		nits = its[np.where(its > 0)]
		fname = get_output_dir("interses") + "/day_" + str(d)
		print "Writing to file - ", fname
		write_data(fname, nits)

## Ses count and inter-arrival between sessions
def create_ses_count_inter():
	dl = get_day_list()
	r = RunSQL("unc.db")
	r1 = RunSQL("syslog_final.db")

	for d in dl:
		print "Processing day - ", d
		q1 = "select client, ap, start, end from seslen where day = " + str(d)
		l1 = r1.sqlq(q1)

		fcount = list()
		sesinter = list()

		for ses in l1:
			start_ts = ses[2]
			end_ts = ses[3]
			client = ses[0]
			ap = ses[1]

			q = "select ts from flows" + \
				 " where day = " + str(d) + \
				 " and ts >= " + str(start_ts) + \
				 " and ts <= " + str(end_ts) + \
				 " and client = " + str(client) + \
				 " and ap = " + str(ap) + \
				 " order by ts"
			l = r.sqlq(q)
			if ( l != None and len(l) > 0 ):
				fcount.append(len(l))
				n = len(l)
				npl = np.array(l)
				inpl = (npl[1:n] - npl[0:n-1])
				inpl1 = inpl[np.where(inpl>0)]
				if ( len(inpl1) > 0 ):
					sesinter.extend(inpl1.tolist())
		ifname = get_output_dir("intrases") + "/day_" + str(d)
		cfname = get_output_dir("fcount") + "/day_" + str(d)

		print "Writing file - ", ifname
		write_data(ifname, sesinter)

		print "Writing file - ", cfname
		write_data(cfname, fcount)
				
					
if __name__ == "__main__":
	create_ses_inter()
	create_ses_count_inter()
