#! /usr/bin/python

from rpytools.util import write_data
from rpytools.sql import RunSQL
from os import getenv

def get_day_list():
	return [13,14,15,16,17,18,19,20]

def get_output_dir(data_type):
	return getenv("HOME") + "/research/ml_data/unc/snmp/" + data_type

def create_seslen():
	dl = get_day_list()
	r = RunSQL("unc-proc.db")
	
	slen = list()
	inb = list()
	outb = list()

	for d in dl:
		q = "select seslen, bin, bout from sessions where day = " + str(d) + " and seslen > 0 and bin > 0 and bout > 0"
		print "Getting data for day - ", d
		slist = r.sqlq(q)
		n = len(slist)
		for i in xrange(n):
			slen.append(slist[i][0])
			inb.append(slist[i][1])
			outb.append(slist[i][2])
		
		fname = "day_" + str(d)
		slenf = get_output_dir("seslen") + "/" + fname
		inbf = get_output_dir("inb") + "/" + fname
		outbf = get_output_dir("outb") + "/" + fname
		
		print "Writing slen - " + slenf
		write_data(slenf, slen)

		print "Writing inb - " + inbf
		write_data(inbf, inb)

		print "Writing outb - " + outbf
		write_data(outbf, outb)
			

if __name__ == "__main__":
	create_seslen()
	

