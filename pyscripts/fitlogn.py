import numpy as np
from rpytools.util import read_data
from rpytools.lognormal import Lognormal
from rpytools.util import ccdf
from rpytools.util import ecdf
import sys

def usage():
	print "fitlogn.py file1 file2 ..."


def fitlogn(dataf):
	x=np.array(read_data(dataf))
	x.sort()

	l1 = Lognormal.fromFit(x)
	l2 = Lognormal.fromFit(x,mmefit=False)

	ec = ecdf(x)
	cc = ccdf(x)

	q1 = l1.fitmetric(cdf=ec)
	q2 = l2.fitmetric(cdf=ec)

	print "File: " + dataf
	if q1 <= q2:
		print "Type: MME"
		print "Lognormal: " + str(l1)
		print "FIT: ", q1
		print "K-S: ", l1.ksmetric(cdf=ec)
	else:
		print "Type: MLE"
		print "Lognormal: " + str(l2)
		print "FIT: ", q2
		print "K-S: ", l2.ksmetric(cdf=ec)

def main():
	if len(sys.argv) < 2:
		usage()
		sys.exit(2)

	n = len(sys.argv)
	for i in xrange(1,n):
		print "-------------------------------------------------------------------------"
		print "processing " + sys.argv[i] + " ... "
		fitlogn(sys.argv[i])
		print "-------------------------------------------------------------------------"
		print


if __name__ == "__main__":
	main()
