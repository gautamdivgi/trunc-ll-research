import matplotlib.pyplot as plt
import rpytools.util as util
import numpy as np
import math
import rpytools.modlav as ml

def catm_ccdf():
	try:
		plt.show()
	except:
		pass

	
	# These are already computed values.
	# The script is only to plot the data.
	# Please refer to the notes on how to re-compute.
	# xmax is the value from the optimization run for mme
	x = util.read_data("/home/gautam/research/modlav-plots/seslen/catm_ses")
	mle=ml.ModLav(0.9398,3003.4797,0.1488)
	mme=ml.ModLav(1.0,3243.2566,0.1894)
	xmax = 17123.2972

	cc = util.ccdf(x)

	lx=util.gen_points(math.log10(x.min()),math.log10(x.max()),2000)
	ex=np.power(lx,10)
	mlecc = mle.ccdf(ex)

	mme_lx=util.gen_points(math.log10(x.min()),math.log10(xmax),2000)
	mme_ex=np.power(mme_lx,10)
	mmecc = mme.ccdf(mme_ex)

	plt.loglog(cc[:,0],cc[:,1],'k-',label='Data',linestyle='steps')
	plt.loglog(ex,mlecc,'k--',label='MLE fit')
	plt.loglog(mme_ex,mmecc,'k-.',label='MME fit')
	plt.xlim((x.min(),x.max()*10))
	plt.ylim((1e-4,1.1))
	plt.grid()
	plt.ylabel("P(X > x)")
	plt.xlabel("Session length [seconds]")
	plt.legend(loc=3)

def catm_cdf():
	try:
		plt.show()
	except:
		pass

		
	# These are already computed values.
	# The script is only to plot the data.
	# Please refer to the notes on how to re-compute.
	# xmax is the value from the optimization run for mme
	x = util.read_data("/home/gautam/research/modlav-plots/seslen/catm_ses")
	mle=ml.ModLav(0.9398,3003.4797,0.1488)
	mme=ml.ModLav(1.0,3243.2566,0.1894)
	xmax = 17123.2972

	ec = util.ecdf(x)
	mleec = mle.cdf(ec[:,0])
	mmeec = mme.cdf(ec[:,0])

	plt.plot(ec[:,0],ec[:,1],'k-',label='Data',linestyle='steps')
	plt.plot(ec[:,0],mleec,'k--',label='MLE fit')
	plt.plot(ec[:,0],mmeec,'k-.',label='MME fit')
	plt.grid()
	plt.xlabel("Session length [seconds]")
	plt.ylabel("P(X <= x)")
	plt.ylim((0.0,1.0))
	plt.legend(loc=4)

def cath_ccdf():
	try:
		plt.show()
	except:
		pass

	# These are already computed values. Please look at the notes
	# on discussion as to why and how they were chosen. The CDF 
	# and CCDF values for the fitted distributions are different.
	# The reasoning for this is also in the notes.

	m2 = ml.ModLav(0.7438, 657.1194, 0.0191)
	m3 = ml.ModLav(0.7294, 644.6747, 0.0104)
	
	x = util.read_data("/home/gautam/research/modlav-plots/seslen/cath_ses")
	cc = util.read_data("/home/gautam/research/modlav-plots/seslen/cath_ccdf")

	plt.loglog(cc[:,0],cc[:,1],'k-',label='Data',linestyle='steps')
	lx=util.gen_points(math.log10(x.min()),math.log10(x.max()),2000)
	ex=np.power(lx,10)
	m2cc=m2.ccdf(ex)
	m3cc=m3.ccdf(ex)
	plt.loglog(ex,m3cc,'k--',label='MLE,MT, No OPT')
	plt.loglog(ex,m2cc,'k-.',label='MLE, MT, OPT')
	plt.grid()
	plt.xlim((1.0,1e5))
	plt.ylim((1e-4,1.1))
	plt.ylabel("P(X > x)")
	plt.xlabel("Session length [seconds]")
	plt.legend(loc=3)

def cath_ecdf():
	try:
		plt.show()
	except:
		pass

	m1 = ml.ModLav(0.9147, 659.8731, 0.0493)
	m3 = ml.ModLav(0.7294, 644.6747, 0.0104)
	
	x = util.read_data("/home/gautam/research/modlav-plots/seslen/cath_ses")
	ec = util.read_data("/home/gautam/research/modlav-plots/seslen/cath_ecdf")

	m1ec=m1.cdf(ec[:,0])
	m3ec=m3.cdf(ec[:,0])

	plt.plot(ec[:,0],ec[:,1],'k-',label='Data',linestyle='steps')
	plt.plot(ec[:,0],m3ec,'k--',label='MLE, MT, No OPT')
	plt.plot(ec[:,0],m1ec,'k-.',label='MLE, No MT, OPT')
	plt.ylim((0.0,1.0))
	plt.xlim((1.0,10000))
	plt.xlabel("Session length [seconds]")
	plt.ylabel("P(X <= x)")
	plt.grid()
	plt.legend(loc=4)


def all_ccdf():
	try:
		plt.show()
	except:
		pass

	m1 = ml.ModLav(1.0186, 1534.7651, 0.0892)
	m2 = ml.ModLav(1.0, 1539.8953, 0.0855)

	x = util.read_data("/home/gautam/research/modlav-plots/seslen/all_ses")
	cc = util.read_data("/home/gautam/research/modlav-plots/seslen/all_ccdf")

	m1cc = m1.ccdf(cc[:,0])
	m2cc = m2.ccdf(cc[:,1])

	plt.loglog(cc[:,0],cc[:,1],'k-',label='Data',linestyle='steps')
	plt.loglog(cc[:,0],m1cc,'k--',label='MLE fit')
	plt.loglog(cc[:,0],m2cc,'k-.',label='MME fit')
	plt.grid()
	plt.xlabel("Session length [seconds]")
	plt.ylabel("P(X > x)")
	plt.ylim((1e-5,1.1))
	plt.legend(loc=3)

def all_ecdf():
	try:
		plt.show()
	except:
		pass
	

	m1 = ml.ModLav(1.0186, 1534.7651, 0.0892)
	m2 = ml.ModLav(1.0, 1539.8953, 0.0855)

	x = util.read_data("/home/gautam/research/modlav-plots/seslen/all_ses")
	ec = util.read_data("/home/gautam/research/modlav-plots/seslen/all_ecdf")

	m1ec = m1.cdf(ec[:,0])
	m2ec = m2.cdf(ec[:,1])

	plt.plot(ec[:,0],ec[:,1],'k-',label='Data',linestyle='steps')
	plt.plot(ec[:,0],m1ec,'k--',label='MLE fit')
	plt.plot(ec[:,0],m2ec,'k-.',label='MME fit')
	plt.xlabel("Session length [seconds]")
	plt.ylabel("P(X <= x)")
	plt.ylim((0.0,1.0))
	plt.grid()
	plt.legend(loc=4)

