import rpytools.util as util
import datetime as dt
import rpytools.sql as sql
import math
import numpy as np

day_atimes = {"bo": 30.0, \
				  "70": 30.0, \
				  "71": 1.0, \
				  "73": 3.0, \
				  "75": 5.0}

hour_atimes = {"10": 1.0, \
					"30": 1.0, \
					"80": 10.0, \
					"81": 1.0, \
					"82": 2.0, \
					"83": 3.0, \
					"84": 4.0, \
					"85": 5.0, \
					"AU": 1.0, \
					"GR": 1.0, \
					"IP": 1.0, \
					"PP": 1.0, \
					"PS": 0.33}

prices = {"bo": 30.0, \
			 "10": 13.2, \
			 "30": 13.2, \
			 "70": 150.0, \
			 "71": 20.0, \
			 "73": 40.0, \
			 "75": 60.0, \
			 "80": 99.0, \
			 "81": 13.2, \
			 "82": 25.0, \
			 "83": 35.0, \
			 "84": 45.0, \
			 "85": 55.0, \
			 "AU": 6.0, \
			 "GR": 6.0, \
			 "IP": 6.0, \
			 "PP": 13.2, \
			 "PS": 5.0}

def get_data1(cat=None):
	if cat == None	:
		qry = "select user,ucat_term, sum(seslen),sum(bin+bout), min(arr_ts),max(arr_ts+seslen) from data_log where seslen <= 18100 group by user"
	else:
		qry = "select user,ucat_term, sum(seslen),sum(bin+bout),min(arr_ts),max(arr_ts+seslen) from data_log where seslen <= 18100 and ucat_term = '" + cat + "' group by user"
	
	# print qry
	s = sql.RunSQL("azure.db")
	x = s.sqlq(qry)
	
	fx = []
	for r in x:
		ifx = [r[0].strip(), r[1].strip(), float(r[2]), float(r[3]), float(r[4]), float(r[5])]
		fx.append(ifx)
	
	y = s.sqlq("select ucat,price from user_pfx")
	pmap = dict()
	for r1 in y:
		pmap[r1[0].strip()] = float(r1[1])	
	
	return (fx, pmap)

def get_data(cat=None):
	if cat == None	:
		qry = "select user,ucat_term, seslen,bin+bout, arr_ts from data_log group by user"
	else:
		qry = "select user,ucat_term,seslen,bin+bout, arr_ts, from data_log where ucat_term = '" + cat + "' group by user"

	s = sql.RunSQL("azure.db")
	x = s.sqlq(qry)

	acct_data = dict()
	for r in x:
		usr = r[0].strip()
		cat = r[1].strip()
		slen = float(r[2])
		b = float(r[3])
		ats = float(r[4])

		if usr not in acct_data:
			sa=[slen]
			ba=[b]
			atsa=[ats]

			acct_data[usr] = [cat, sa, ba, atsa]
		else:
			acct_data[usr][1].append(slen)
			acct_data[usr][2].append(b)
			acct_data[usr][3].append(ats)

	
	fx = []
	for item in acct_data.items():
		usr = item[0]
		val = item[1]

		cat = val[0]
		nslen = np.array(val[1])
		nb = np.array(val[2])
		nats = np.array(val[3])

		nslen.sort()
		nb.sort()
		nats.sort()

		ifx = [usr, cat, np.sum(nslen), np.sum(nb), nats.min(), nats.max()]
		fx.append(ifx)
	
	
	y = s.sqlq("select ucat,price from user_pfx")
	pmap = dict()
	for r1 in y:
		pmap[r1[0].strip()] = float(r1[1])	
	
	return (fx, pmap)

def eco_needs(cat = None):
	(x, pmap) = get_data1(cat)

	n = len(x)
	uname = []

	nrl = []
	
	for r in x:
		usr = r[0]
		cat = r[1]
		lT = float(r[2])
		bT = float(r[3])
		start = float(r[4])
		end = float(r[5])

		ufull = usr.split(' ')
		ucat = ufull[0]
		sprice = pmap[ucat]

		nrenew = 1.0

		if cat == "catm" or cat == "catd":
			atime = day_atimes[ucat]
			nrenew = math.ceil(math.ceil((end - start)/(3600.0*24.0))/atime)
			hu = 0.0
		else:
			atime = hour_atimes[ucat]
			nrenew = max(math.ceil((lT)/3600.0*atime), 1)
			hu = float(lT)/float(nrenew * atime * 3600.0)


		nrl.append([nrenew, bT, hu])
	
	return nrl
	

def acct_util(cat = None):
	
	
	(x, pmap) = get_data1(cat)

	n = len(x)
	uname = []
	tutil = []
	dutil = []

	for r in x:
		usr = r[0]
		cat = r[1]
		lT = float(r[2])
		bT = float(r[3])
		start = float(r[4])
		end = float(r[5])

		ufull = usr.split(' ')
		ucat = ufull[0]
		sprice = pmap[ucat]

		if cat == "catm" or cat == "catd":
			# print "M/D --> ", cat
			atime = day_atimes[ucat]
			pp = max(sprice*math.ceil(math.ceil((end - start)/(3600.0*24.0))/atime), sprice)
		else:
			# print"H -->", cat
			atime = hour_atimes[ucat]
			pp = max(sprice*math.ceil(lT/(3600.0*atime)), sprice)
		
		# print usr, cat, start, end, atime, sprice, lT, bT, pp
		if pp > 0:
			uname.append(usr)
			tutil.append(lT/(3600.0 * pp))
			dutil.append(bT/(1e6 * pp))
		else:
			uname.append(usr)
			tutil.append(0.0)
			dutil.append(0.0)
		
	return (uname, np.array(tutil), np.array(dutil))

def main():

	cats = [None, 'catm\n', 'catd\n', 'cath\n']

	for cat in cats:
		r = acct_util(cat)
		
		tuf = "tu_all.dat"
		duf = "du_all.dat"
		if cat != None:
			tuf = "tu_" + cat.strip() + ".dat"
			duf = "du_" + cat.strip() + ".dat"
		
		tu = r[1]
		du = r[2]
		# Need unsorted values
		if cat == None:
			tudu = np.zeros((len(tu),2))
			tudu[:,0] = tu
			tudu[:,1] = du
			util.write_data("tudu.dat", tudu)

		tu.sort()
		du.sort()

		ctu = util.ecdf(tu,zdisp=True)
		cdu = util.ecdf(du,zdisp=True)

		util.write_data(tuf, ctu)
		util.write_data(duf, cdu)
		

		pcat = "ALL"
		if cat != None:
			pcat = cat.strip()

		print "CATEGORY: ", pcat
		print "Time utilization"
		print "------------------------------------------------"
		util.pstats(tu)
		print
		print "Data utilization"
		print "------------------------------------------------"
		util.pstats(du)
		print
		print

if __name__ == "__main__":
	main()
