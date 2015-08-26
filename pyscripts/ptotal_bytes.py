#! /usr/bin/python

from rpytools.sql import RunSQL
from rpytools.util import write_data

def process_data():
	days = [13,14,15,16,17,18,19,20]
	dirn="/Users/chimpu/research/ml_data/unc/"
	for day in days:
		print "Processing day - ", day
		(inb, outb) = process_single_day(day)
		fname_inb = dirn + "/inb/day_" + str(day)
		fname_outb = dirn + "/outb/day_" + str(day)
		write_data(fname_inb, inb)
		write_data(fname_outb, outb)
		print "Done writing records - ", len(inb)


def process_single_day(day):
	SES_CLIENT=0
	SES_AP=1
	SES_START=2
	SES_END=3

	SNMP_INB=0
	SNMP_OUTB=1
	seslen_qry = "select client,ap,start,end from seslen where day = " + str(day)
	rses = RunSQL("syslog_final.db")
	rsnmp = RunSQL("unc.db")
	sesres = rses.sqlq(seslen_qry)
	
	inb = list()
	outb = list()
	for single_ses in sesres:
		snmp_qry = "select sum(bytr), sum(byts) from snmp where client = " + str(single_ses[SES_CLIENT]) + " and ap = " + str(single_ses[SES_AP]) + " and ts >= " + str(single_ses[SES_START]) + " and ts <= " + str(single_ses[SES_END]) + " and day = " + str(day) + " group by client, ap"
		
		snmpres = rsnmp.sqlq(snmp_qry)
		if ( snmpres != None and len(snmpres) > 0  and snmpres[0][SNMP_INB] > 0 and snmpres[0][SNMP_OUTB] > 0 ):
			inb.append(snmpres[0][SNMP_INB])
			outb.append(snmpres[0][SNMP_OUTB])

	return (inb, outb)


if __name__ == "__main__":
	process_data()
