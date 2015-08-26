import rpytools.util as util
import rpytools.sql as sql
import numpy as np
import os

IA_FILE = "/home/gautam/dbs/flow_ia"
COUNT_FILE = "/home/gautam/dbs/flow_count"

TS = 0
AP = 1
CL = 2
SLEN = 3


def flow_ia_count(ap = None):
	ps = sql.RunSQL("unc-proc.db")
	pf = sql.RunSQL("unc.db")
	
	if ap == None:
		qry = "select * from sessions"
	else:
		qry = "select * from sessions where ap = " + str(int(ap))
	
	ses1 = ps.sqlq(qry)
	seslist = np.array(ses1)
	
	counts = []
	ia = []
	
	qry = "select ts from flows where client = %%client%% and ap = %%ap%% and ts >= %%sts%% and ts <= %%ets%%"

	for ses in seslist:
		sts = ses[TS]
		ets = ses[TS] + ses[SLEN] + 300
		client = ses[CL]
		sap = ses[AP]

		this_q = qry.replace("%%client%%",str(client)).replace("%%ap%%",str(sap)).replace("%%sts%%",str(sts)).replace("%%ets%%",str(ets))
		flows1 = pf.sqlq(this_q)

		if len(flows1) == 0:
			pass
		else:	
			flows = np.array(flows1)
			n = len(flows)
			counts.append(n)
			if n > 1:
				this_ia = flows[1:n]-flows[0:n-1]
				for each_ia in this_ia:
					ia.append(each_ia)
		
	return (counts, ia)





