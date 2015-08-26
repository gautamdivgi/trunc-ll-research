#! /usr/bin/python

from rpytools.sql import RunSQL
from rpytools.util import write_data

def process_data():
	days = [13,14,15,16,17,18,19,20]
	dirn="/Users/chimpu/research/ml_data/unc/"
	for day in days:
		print "Processing day - ", day
		fcount = process_single_day(day)
		fname = dirn + "/fcount/day_" + str(day)
		write_data(fname, fcount)
		print "Done writing records - ", len(fcount)


def process_single_day(day):
	SES_CLIENT=0
	SES_AP=1
	SES_START=2
	SES_END=3

	FLOWS_COUNT=0
	seslen_qry = "select client,ap,start,end from seslen where day = " + str(day)
	rses = RunSQL("syslog_final.db")
	rflows = RunSQL("unc.db")
	sesres = rses.sqlq(seslen_qry)
	
	fcount = list()
	for single_ses in sesres:
		flows_qry = "select count(*) from flows where client = " + str(single_ses[SES_CLIENT]) + " and ap = " + str(single_ses[SES_AP]) + " and ts >= " + str(single_ses[SES_START]) + " and ts <= " + str(single_ses[SES_END]) + " and day = " + str(day) + " group by client, ap"
		
		flowres = rflows.sqlq(flows_qry)
		if ( flowres != None and len(flowres) > 0 ):
			fcount.append(flowres[0])


	return fcount


if __name__ == "__main__":
	process_data()
