from rpytools.util import dice
from rpytools.util import write_data
from rpytools.util import read_data
from rpytools.util import remove_outliers
from rpytools.similarity import new_similarity_invcdf
from scipy.stats import moment
import numpy as np
import sys
import math
import multiprocessing as mp
from multiprocessing import Pool

CAT_Y_AXIS = [("all",3), ("catm", 2), ("catd", 1), ("cath", 0)]
CAT_X_AXIS = [("all",0), ("catm", 1), ("catd", 2), ("cath", 3)]
CAT = ["all", "catm", "catd", "cath"]
METRICS = [ \
				("tu_g", "Time utilization"), \
				("du_g", "Data utilization"), \
				("ioratio_g", "Inbound to outbound traffic ratio"), \
				("slen_g", "Session length"), \
				("stbin_g", "Inbound session traffic"), \
				("stbout_g", "Outbound session traffic"), \
				("sttotal_g", "Total session traffic"), \
				## ("tpd_g", "Traffic per day - Global metric"), \
				("tpd_i", "Traffic per day - Individual metric"), \
				("trbin_g", "Inbound traffic rate per session"), \
				("trbout_g", "Outbound traffic rate per session"), \
				## ("uact_g", "Active days per user - Global metric"), \
				("uact_i", "Active days per user - Individual metric"), \
				## ("upd_g", "Users per day - Global metric"), \
				("upd_i", "Users per day - Individual metric") \
			]

mtype = None

def simple_ks(x, y):
	(x12,f1,f2) = comb_cdf(x,y)
	return 1.0 - np.max(np.abs(f1-f2))

def cdf_dice_metric(x, y):
	x.sort()
	y.sort()
	(x12,f1,f2) = comb_cdf(x,y,issorted=True)
	return dice(f1,f2)

def central_moment(x, Ex, n):
	nx = float(len(x))
	
	t1 = x - Ex
	t2 = np.power(t1, n)
	t3 = t2/nx
	
	t4 = math.pow(np.sum(t3), 1/float(n))

	return t4

def moment_dice_metric(x, y, **kwargs):
	""" kwargs: fourthmoment - True/False. False by detault """

	nx = float(len(x))
	ny = float(len(y))

	Exi = x.mean()
	sigmaxi = math.pow(moment(x, 2), 1/2.0)  #central_moment(x, Exi, 2)
	sxi = math.pow(abs(moment(x, 3)), 1/3.0) #central_moment(x, Exi, 3)
	kxi = math.pow(moment(x,4), 1/4.0) #central_moment(x, Exi, 4)

	Eyi = y.mean()
	sigmayi = math.pow(moment(y, 2), 1/2.0) #central_moment(y, Eyi, 2)
	syi = math.pow(abs(moment(y, 3)), 1/3.0) #central_moment(y, Eyi, 3)
	kyi = math.pow(moment(y, 4), 1/4.0) #central_moment(y, Eyi, 4)
	
	fourthmoment = False
	if "fourthmoment" in kwargs:
		fourthmoment = kwargs["fourthmoment"]
	
	if fourthmoment == True:
		fx1 = np.array([Exi, sigmaxi, sxi, kxi])
		fy1 = np.array([Eyi, sigmayi, syi, kyi])
	else:
		fx1 = np.array([Exi, sigmaxi, sxi])
		fy1 = np.array([Eyi, sigmayi, syi])
	return dice(fx1, fy1)

def newmetsx(fx1, fx2):
	if fx1 == 0 and fx2 == 0:
		return 1.0
	else:
		return min(fx1,fx2)/max(fx1,fx2)

def newmetric(x1, x2):
	(x12,f1,f2) = comb_cdf(x1,x2)

	i = 0
	x1 = x12.min()
	xn = x12.max()
	n = len(x12)

	xi1 = x12[1:n]
	xi = x12[0:n-1]

	nx = n-1
	
	tsx = 0.0
	while i < nx:
		tsx+= newmetsx(f1[i], f2[i])*(xi1[i] - xi[i])
		i+= 1
	
	sx = (x1 + tsx) / float(xn)
	return sx


def comb_cdf(x1, x2, **kwargs):
	""" Compute the combined CDF """
	""" x12 = x1 U x2, f1 = F1(x12), f2 = F2(x12) """
	""" Input """
	""" x1: Array of double """
	""" x2: Array of double """
	""" **kwargs: issorted - True or False. Default is False """
	""" Return: (x12, f1, f2) """

	isSortedVal = False
	
	mtype = "dice"
	n1 = float(len(x1))
	n2 = float(len(x2))

	if "issorted" in kwargs:
		isSortedVal = kwargs["issorted"]

	if isSortedVal == False:
		x1.sort()
		x2.sort()
	
	x12max = min(x1.max(), x2.max())
	sx12 = set(x1).union(set(x2))
	px12 = np.array(list(sx12))
	px12.sort()
	x12 = remove_outliers(px12,0.0, x12max)
	n12 = len(x12)

	f1 = np.zeros(n12)
	f2 = np.zeros(n12)

	i = 0
	while i < n12:
		xij = x12[i]

		idx1 = np.argwhere(x1 <= xij)
		if ( len(idx1) > 0 ):
			f1[i] = (idx1.max()+1)/(n1 + 1.0)
		else:
			f1[i] = 0.0

		idx2 = np.argwhere(x2 <= xij)
		if ( len(idx2) > 0 ):
			f2[i] = (idx2.max()+1)/(n2 + 1.0)
		else:
			f2[i] = 0.0
		i+= 1
	
	return (x12,f1,f2)

def sim_mat(x,y):
	""" mtype: cdd, ks, dm3, dm4 """
	""" cdd: combined CDF dice """
	""" ks: combined CDF K-S """
	""" dm3: dice with 3 moments, 1 moment and 2 central moments """
	""" dm4: dice with 4 moments, 1 moment and 3 central moments """

	global mtype	
	sim_idx = float('NaN')
	try:
		if mtype == None or mtype == "ks":
			sim_idx = simple_ks(x,y)
		elif mtype == "cdd":
			sim_idx = cdf_dice_metric(x,y)
		elif mtype == "dm3":
			sim_idx = moment_dice_metric(x,y)
		elif mtype == "dm4":
			sim_idx = moment_dice_metric(x,y,fourthmoment=True)
		elif mtype == "nm":
			sim_idx = newmetric(x,y)
		elif mtype == "invcdf":
			sim_idx = new_similarity_invcdf(x,y)

		return sim_idx
	except BaseException, be:
		print "Exception -> ", be
		return float('NaN')
	
def dice_matrix(mtup):
	print mtup
	global CAT
	mname = mtup[0]
	fa = str(mname) + "." + CAT[0]
	fm = str(mname) + "." + CAT[1]
	fd = str(mname) + "." + CAT[2]
	fh = str(mname) + "." + CAT[3]

	a = read_data(fa)
	m = read_data(fm)
	d = read_data(fd)
	h = read_data(fh)

	am = sim_mat(a,m)
	ad = sim_mat(a,d)
	ah = sim_mat(a,h)

	md = sim_mat(m,d)
	mh = sim_mat(m,h)

	dh = sim_mat(d,h)

	simmat = np.zeros([4,4])

	simmat[0,0] = ah
	simmat[0,1] = ad
	simmat[0,2] = am

	simmat[1,0] = mh
	simmat[1,1] = md

	simmat[2,0] = dh
	
	print simmat
	return (mtup, simmat)

def parsimidx(metric_type):
	global mtype
	global METRICS

	mtype = metric_type
	local_metrics = METRICS
	ncpus = mp.cpu_count()
	proc_pool = Pool(ncpus)
	results = proc_pool.map(dice_matrix, local_metrics)
	totr = np.zeros([4,4])
	n = 0

	for result in results:
		print_simmat(result[0], result[1])
		totr+= result[1]
		n+= 1
	
	tup = ("ALL", "Combined metrics")
	print_simmat(tup, totr/float(n))

def print_simmat(mtup, simmat):
	desc = mtup[1]

	print "---------------------" + desc + "-------------------------"
	print
	print "ALL  |"
	print "-------------------------------------"
	print "CATM |  {0:1.3f} |".format(simmat[0,2])
	print "-------------------------------------"
	print "CATD |  {0:1.3f} | {1:1.3f} |".format(simmat[0,1],simmat[1,1])
	print "-------------------------------------"
	print "CATH |  {0:1.3f} | {1:1.3f} | {2:1.3f} |".format(simmat[0,0],simmat[1,0],simmat[2,0])
	print "-------------------------------------"
	print "     |  ALL     CATM    CATD    CATH"
	sys.stdout.flush()

def main():
	mattyp = sys.argv[1]
	print "Type: ", mattyp
	parsimidx(mattyp)

if __name__ == "__main__":
	main()
