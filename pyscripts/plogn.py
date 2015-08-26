#! /usr/bin/python

from rpytools.sql import RunSQL
import sys

def vtex(value):
	if value > 10.0:
		return "%.6g"%value
	elif value > 1.0:
		return "%.5g"%value
	else:
		return "%.4g"%value

def main(args):
	r2 = RunSQL("logn_fits.db")

	unique_id = args[0].upper()

	r2q = "select type, mu, sigma from logn_fits where unique_id='" + unique_id + "'"

	rs = r2.sqlq(r2q)
	txstr = "$%MLE-MU%$ & $%MLE-SIG%$ & $%MME-MU%$ & $%MME-SIG%$ & $%FITMIN-MU%$ & $%FITMIN-SIG%$ \\tabularnewline"
	for rss in rs:
		print "LOGN-" + rss[0]
		print "\t mu: " + vtex(rss[1])
		print "\t sigma: " + vtex(rss[2])
		replace_str_mu = "%"+rss[0]+"-MU%"
		replace_str_sig = "%"+rss[0]+"-SIG%"
		txstr = txstr.replace(replace_str_mu, vtex(rss[1]))
		txstr = txstr.replace(replace_str_sig, vtex(rss[2]))
	print txstr

if __name__ == "__main__":
	main(sys.argv[1:])
