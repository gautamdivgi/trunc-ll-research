import math
import numpy as np
import rpytools.util as util
import rpytools.sql as sql

def chkskew_for_wday(r, w):
	qry = "select bin+bout, seslen from data_log where wday = '" + w + "' order by bin+bout desc"
	x = np.array(r.sqlq(qry))
	d=x[:,0]
	s=x[:,1]

	u = int(math.floor(len(d)*0.03))

	d3p = d[0:u-1]
	s3p = s[0:u-1]
	drest = d[u:len(d)-1]
	srest = s[u:len(s)-1]

	pct =d3p.sum()*100.0/d.sum()
	savg = np.mean(s3p)/3600.0

	pctrest = drest.sum()*100.0/d.sum()
	srestavg = np.mean(srest)/3600.0

	# print w, ":", pct, ":", savg, ":", pctrest, ":", srestavg
	# print w, ":", d.sum()/float(1e6), ":", d3p.sum()/float(1e6), ":", drest.sum()/float(1e6)
	print w, ":", np.mean(d)/float(1e6), ":",  np.mean(d3p)/float(1e6), ":", np.mean(drest)/float(1e6)

def main():
	r = sql.RunSQL("azure.db")
	wday=["sun","mon","tue","wed","thu","fri","sat"]
	
	for w in wday:
		chkskew_for_wday(r,w)


if __name__ == "__main__":
	main()
