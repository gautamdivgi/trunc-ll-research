#! /usr/bin/python

import sys
import rpytools.util as util
import rpytools.sql as sql
import numpy as np
import rpytools.modlav as ml
import math
import scipy.stats.mstats as ms

def main(dt):
	slen = {"catm": "select seslen from data_log where ucat_term='catm\n' and seslen>0 and seslen<18000 order by seslen", \
			  "catd": "select seslen from data_log where ucat_term='catd\n' and seslen>0 and seslen<18000 order by seslen", \
			  "cath": "select seslen from data_log where ucat_term='cath\n' and seslen>0 and seslen<18000 order by seslen", \
			  "all": "select seslen from data_log where seslen>0 and seslen<18000 order by seslen"}

	inb = {"catm": "select bin from data_log where ucat_term='catm\n' and bin>0 and seslen>0 and seslen<18000 order by bin", \
			  "catd": "select bin from data_log where ucat_term='catd\n' and bin>0 and seslen>0 and seslen<18000 order by bin", \
			  "cath": "select bin from data_log where ucat_term='cath\n' and bin>0 and seslen>0 and seslen<18000 order by bin", \
			  "all": "select bin from data_log where bin>0 and seslen>0 and seslen<18000 order by bin"}
	
	outb = {"catm": "select bout from data_log where ucat_term='catm\n' and bout>0 and seslen>0 and seslen<18000 order by bout", \
			  "catd": "select bout from data_log where ucat_term='catd\n' and bout>0 and seslen>0 and seslen<18000 order by bout", \
			  "cath": "select bout from data_log where ucat_term='cath\n' and bout>0 and seslen>0 and seslen<18000 order by bout", \
			  "all": "select bout from data_log where bout>0 and seslen>0 and seslen<18000 order by bout"}

	to_inb = {"all": "select bin from data_log where seslen >= 18000 and bin>0 order by bin"}

	to_outb = {"all": "select bout from data_log where seslen >= 18000 and bout>0 order by bout"}
	
	tslen = {"catm": "select sum(seslen) t from data_log where ucat_term='catm\n' and seslen>0 and seslen<18000 group by user order by t", \
			  "catd": "select sum(seslen) t from data_log where ucat_term='catd\n' and seslen>0 and seslen<18000 group by user order by t", \
			  "cath": "select sum(seslen) t from data_log where ucat_term='cath\n' and seslen>0 and seslen<18000 group by user order by t", \
			  "all": "select sum(seslen) t from data_log where seslen>0 and seslen<18000 group by user order by t"}

	tinb = {"catm": "select sum(bin) t from data_log where ucat_term='catm\n' and bin > 0 and seslen>0 and seslen<18000 group by user order by t", \
			  "catd": "select sum(bin) t from data_log where ucat_term='catd\n' and bin > 0 and seslen>0 and seslen<18000 group by user order by t", \
			  "cath": "select sum(bin) t from data_log where ucat_term='cath\n' and bin > 0 and seslen>0 and seslen<18000 group by user order by t", \
			  "all": "select sum(bin) t from data_log where bin > 0 and seslen>0 and seslen<18000 group by user order by t"}
	
	toutb = {"catm": "select sum(bout) t from data_log where ucat_term='catm\n' and bout>0 and seslen>0 and seslen<18000 group by user order by t", \
			  "catd": "select sum(bout) t from data_log where ucat_term='catd\n' and bout>0 and seslen>0 and seslen<18000 group by user order by t", \
			  "cath": "select sum(bout) t from data_log where ucat_term='cath\n' and bout>0 and seslen>0 and seslen<18000 group by user order by t", \
			  "all": "select sum(bout) t from data_log where bout>0 and seslen>0 and seslen<18000 group by user order by t"}

	dtmap = {"slen": slen, "inb": inb, "outb": outb, "to_inb": to_inb, "to_outb": to_outb, "tslen": tslen, "tinb": tinb, "toutb": toutb}

	if dt not in dtmap:
		raise NotImplementedError("Type - " + dt + " - is not implemented")
	
	qmap = dtmap[dt]
	
	s = sql.RunSQL("azure.db")
	for i in qmap.items():
		q = i[1]
		y = s.sqlq(q)
		x = np.array(y)
		x.sort() # just making sure

		df = i[0] + "_" + dt
		ccf = i[0] + "_ccdf"
		ecf = i[0] + "_ecdf"

		cc = util.ccdf(x)
		ec = util.ecdf(x)

		util.write_data(df, x)
		util.write_data(ccf, cc)
		util.write_data(ecf, ec)


		mle = ml.ModLav.fromFit(x,fit="mlefit")
		mme = ml.ModLav.fromFit(x,fit="mmefit")
		mle_mt = ml.ModLav.fromFit(x,fit="mlefit",mt=True)
		mme_mt = ml.ModLav.fromFit(x,fit="mmefit",mt=True)

		omle = ml.optfit(x,0.1*x.max(),10*x.max(),500,mlefit=True,mt=False);
		omle_mt = ml.optfit(x,0.1*x.max(),10*x.max(),500,mlefit=True,mt=True);
		omme = ml.optfit(x,0.1*x.max(),10*x.max(),500,mlefit=False,mt=False);
		omme_mt = ml.optfit(x,0.1*x.max(),10*x.max(),500,mlefit=False,mt=True);

		mle_opt = omle["fit"][0]
		xm_mle_opt = omle["fit"][1]

		mle_opt_mt = omle_mt["fit"][0]
		xm_mle_opt_mt = omle_mt["fit"][1]

		mme_opt = omme["fit"][0]
		xm_mme_opt = omme["fit"][1]

		mme_opt_mt = omme_mt["fit"][0]
		xm_mme_opt_mt = omme_mt["fit"][1]

		yyy = [("MLE", mle, x.max()), ("MME", mme, x.max()), ("MLE-MT", mle_mt, x.max()), ("MME-MT", mme_mt, x.max()), ("MLE-OPT", mle_opt, xm_mle_opt), ("MLE-OPT-MT", mle_opt_mt, xm_mle_opt_mt), ("MME-OPT", mme_opt, xm_mme_opt), ("MME-OPT-MT", mme_opt_mt, xm_mme_opt_mt)]
		
		n,amin,amax,mu,sigma = len(x), x.min(), x.max(), x.mean(), x.std()
		cv = sigma/mu
		q = ms.mquantiles(x, [0.1, 0.5, 0.9])
		op_str = []
		op_str.append("BASIC STATISTICS")
		op_str.append("----------------------------------------------------------------------")
		op_str.append("Size: " + str(n))
		op_str.append("Range: " + str(amin) + " - " + str(amax))
		op_str.append("Quantiles: 10% - " + str(q[0]) + " 50% - " + str(q[1]) + " 90% - " + str(q[2]))
		op_str.append("Mean: " + str(mu))
		op_str.append("Sigma: " + str(sigma))
		op_str.append("CV: " + str(cv))
		op_str.append("\n")

		for yy in yyy:
			typ = i[0]
			lbl = yy[0]
			m = yy[1]
			xmx = yy[2]

			op_str.append(lbl)
			op_str.append("----------------------------------------------------------------------")
			op_str.append("Modlav params: " + str(m))
			op_str.append("Xmax: " + str(xmx))
			op_str.append("Xmax/Max: " + str(xmx/amax))
			op_str.append("FIT metric: " + str(m.fitmetric(points=x)))
			op_str.append("K-S metric: " + str(m.ksmetric(points=x)))
			op_str.append("----------------------------------------------------------------------")
			op_str.append("\n")

			flbl = lbl.lower().replace("-", "_")
			fname_pfx = typ + "_" + flbl 

			lx = util.gen_points(math.log10(x.min()),math.log10(xmx),2000)
			ex = np.power(10, lx)

			mcc = m.ccdf(ex)
			mec = m.cdf(ec[:,0])

			fmcc = np.array([ex, mcc]).transpose()
			fmec = np.array([ec[:,0], mec]).transpose()

			util.write_data(fname_pfx+"_ccdf", fmcc)
			util.write_data(fname_pfx+"_ecdf", fmec)
	
		op1_str = []
		for s1 in op_str:
			op1_str.append(s1 + "\n")
		
		txf = open(typ+"_metric", "w+")
		txf.writelines(op1_str)
		txf.close()
