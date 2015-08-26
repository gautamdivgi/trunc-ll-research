from rpytools.util import dice
from rpytools.util import write_data
from rpytools.util import read_data
import numpy as np
import sys

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
				("tpd_g", "Traffic per day - Global metric"), \
				("tpd_i", "Traffic per day - Individual metric"), \
				("trbin_g", "Inbound traffic rate per session"), \
				("trbout_g", "Outbound traffic rate per session"), \
				("uact_g", "Active days per user - Global metric"), \
				("uact_i", "Active days per user - Individual metric"), \
				("upd_g", "Users per day - Global metric"), \
				("upd_i", "Users per day - Individual metric") \
			]

def dice_matrix(mname):
	global CAT
	fa = str(mname) + "." + CAT[0]
	fm = str(mname) + "." + CAT[1]
	fd = str(mname) + "." + CAT[2]
	fh = str(mname) + "." + CAT[3]

	a = read_data(fa)
	m = read_data(fm)
	d = read_data(fd)
	h = read_data(fh)

	a.sort()
	m.sort()
	d.sort()
	h.sort()

	am = dice(a,m,issorted=True)
	ad = dice(a,d,issorted=True)
	ah = dice(a,h,issorted=True)

	md = dice(m,d,issorted=True)
	mh = dice(m,h,issorted=True)

	dh = dice(d,h,issorted=True)

	simmat = np.zeros([4,4])

	simmat[0,0] = ah
	simmat[0,1] = ad
	simmat[0,2] = am

	simmat[1,0] = mh
	simmat[1,1] = md

	simmat[2,0] = dh

	return simmat

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
	global METRICS
	tsimmat = np.zeros([4,4])
	n = 0.0
	for mtup in METRICS:
		simmat = dice_matrix(mtup[0])
		tsimmat+= simmat
		print_simmat(mtup, simmat)
		print
		print
		print
		n+= 1.0
	
	tup = ("ALL", "Combined metrics")
	print_simmat(tup, tsimmat/float(n))

if __name__ == "__main__":
	main()
