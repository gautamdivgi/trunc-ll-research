import numpy as np
import rpytools.tpareto as tpr
import rpytools.lognormal as logn
import rpytools.modlav as ml
import rpytools.pareto as par
import rpytools.rangen as rng
import random
import math
import rpytools.util as util

class DFile:
	"""
	Distribution 1 for the simulation. 
	2 modes of generating distribution 1
	a. An unknown distribution - list of file sizes
	b. A known distribution
	"""

	def __init__(self, **kwargs):
		self.__min = 0.0
		if "minsiz" in kwargs:
			self.__min = float(kwargs["minsiz"])

		if "d" in kwargs:
			d = kwargs["d"]
			plist = kwargs["plist"]
			self.__r = rng.Rangen(d, plist)
			self.__type = "known"
		else:
			self.__list = kwargs["flist"]
			self.__type = "unknown"
		
	
	def random(self, n):
		if self.__type == "known":
			rvs =  self.__r.rvs(n)
		else:
			rvs = np.array(random.sample(self.__list, n))
		
		for i in xrange(n):
			if rvs[i] < self.__min:
				rvs[i] = self.__min
		
		return rvs

def recursive_model(**kwargs):
	"""
	Recursive forest file model simulator
	Params:
	file = data file to pick initial roots
	nroots = number of roots
	d1 = model for roots
	d1params = (param1, param2,...) parameters for d1
	d2 = model for children nodes
	d2params = (param1, param2, ...) parameters for d2
	g = probability of a new file
	nu = probability of a deletion
	n = number of iterations
	minsize = minimum file size
	"""

	sroots = None
	d1f = None
	d2f = None
	g = None
	nu = None
	minsize = 0.0
	
	nroots = kwargs["nroots"]
	if "minsize" in kwargs:
		minsize = kwargs["minsize"]

	if "file" in kwargs:
		fname = kwargs["file"]
		fl = util.read_data(fname)
		d1f = DFile(flist=fl, minsize=0.0)
	else:
		d1model = kwargs["d1"]
		d1params = kwargs["d1params"]
		d1f = DFile(d=d1model, plist=d1params, minsize=0.0)
	
	d2model = kwargs["d2"]
	d2params = kwargs["d2params"]
	d2f = DFile(d=d2model, plist=d2params)

	gf = rng.get_random() # random.Random()
	nf = rng.get_random() # random.Random()
	fpick = rng.get_random() # random.Random()
	g = kwargs["g"]
	nu = kwargs["nu"]
	n = kwargs["n"]

	sroots = d1f.random(nroots)
	simvs = []
	for sroot in sroots:
		s = {"size": sroot, "deleted": False, "mult_factor": 0.0, "depth": 0}
		simvs.append(s)
		
	for i in xrange(nroots, n+1):
		gvar = gf.random()
		if gvar <= g:
			a = d1f.random(1)
			sa = {"size": a, "deleted": False, "mult_factor": 0.0, "depth": 0}
			simvs.append(sa)
		else:
			idx = fpick.randint(0, len(simvs)-1) 
			nvar = nf.random()
			if nvar <= nu:
				simvs.pop(idx)
			else:
				mf = d2f.random(1)
				idx = fpick.randint(0, len(simvs)-1)
				pick = simvs[idx]

				ns = max(pick["size"]*mf[0], minsize)
				ndel = False
				nmf = pick["mult_factor"] * mf[0]
				ndepth = pick["depth"] + 1

				simvs.append({"size": ns, "deleted": ndel, "mult_factor": nmf, "depth": ndepth})

	sizev=[]	
	mfv=[]
	depthv=[]

	for simv	in simvs:
		sizev.append(simv["size"])
		mfv.append(simv["mult_factor"])
		depthv.append(simv["depth"])
	
	return (np.array(sizev), np.array(mfv), np.array(depthv))
