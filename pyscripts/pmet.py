#! /usr/bin/python

from rpytools.sql import RunSQL
import sys

def kstex(value):
	return "%.3g"%value

def qprint(value):
	return "%.2e"%value

def qtex(value):
	y = "%.2e"%value
	z = y.split("e")
	return "$" + z[0] + " \\times 10^{" + str(int(z[1])) + "}" + "$"

def main(args):
	r1 = RunSQL("files_and_analysis.db")
	r2 = RunSQL("logn_fits.db")

	unique_id = args[0].upper()
	distribution = args[1].upper()

	r1q = "select type, ks_fit, q_fit from fits where unique_id='" + unique_id + "' and distribution='" + distribution + "'"
	r2q = "select type, ks_fit, q_fit from logn_fits where unique_id='" + unique_id + "'"

	if "LOGN" == distribution:
		# Do something
		rs = r2.sqlq(r2q)
		for rss in rs:
			print distribution + "-" + rss[0] + "-" + "KS: " + kstex(rss[1])
			print distribution + "-" + rss[0] + "-" + "FIT:" + qprint(rss[2]) + " " +  qtex(rss[2])
	else:
		# Do something
		rs = r1.sqlq(r1q)
		rss = rs[0]
		print distribution + "-" + rss[0] + "-" + "KS: " + kstex(rss[1])
		print distribution + "-" + rss[0] + "-" + "FIT:" + qprint(rss[2]) + " " +  qtex(rss[2])


if __name__ == "__main__":
	main(sys.argv[1:])
