import rpytools.util as util
import rpytools.lognormal as logn
import rpytools.pareto as par
import rpytools.modlav as ml
import rpytools.tpareto as tpr
import rpytools.rangen as rng
import numpy as np
import sys
import os
import getopt


def get_root_from_data(data_file):
	"""
	Get a random root value from the points specified by the data file
	"""
	fp_df = os.path.join(os.environ["TRACE_DB_LOC"], data_file)
	vals = util.read_data(fp_df)
	n = len(vals)
	r = rng.get_random()
	i_rootv = r.randint(0, n-1)
	rootv = vals[i_rootv]
	return rootv

def run_sim(rootv, mname, params, n, minsz = 0.0):
	simvs = []
	simvs.append({"size": rootv, "mult_factor": 0.0, "depth": 0.0})

	rgen = rng.Rangen(mname, params)	
	rvs = rgen.rvs(n)

	r = rng.get_random()

	for i in xrange(n):
		l = len(simvs)
		fchosen = r.randint(0, l-1)
		s = simvs[fchosen]
		mf = rvs[i]

		ns = max(s["size"]*mf, minsz)
		nmf = s["mult_factor"]*mf
		ndepth = s["depth"] + 1

		nsv = {"size": ns, "mult_factor": nmf, "depth": ndepth}
		simvs.append(nsv)
	
	fsz=[]
	mfs=[]
	dp=[]

	for simv in simvs:
		fsz.append(simv["size"])
		mfs.append(simv["mult_factor"])
		dp.append(simv["depth"])

	return (np.array(fsz), np.array(mfs), np.array(dp))

def mult_file_model(**kwargs):
	"""
	Main function for the simulation.
	file = file name to source root value
	rootv = root value. 
	n = number of files to generate
	model = model name
	params = tuple of params
	minsize = min file size
	"""

	data_file = None
	n = None
	model_name = None
	plist = None
	minsize = 0.0

	if "file" in kwargs:
		data_file = kwargs["file"]

	if "rootv" in kwargs:
		root_value = float(kwargs["rootv"])

	if "n" in kwargs:
		n = kwargs["n"]
	
	if "model" in kwargs:
		model_name = kwargs["model"]
	
	if "params" in kwargs:
		plist = kwargs["params"]

	if data_file != None:
		root_value = get_root_from_data(data_file)
	
	if "minsize" in kwargs:
		minsize = kwargs["minsize"]
	
	print data_file
	print root_value
	print n
	print model_name
	print plist

	if root_value == None or n == None or model_name == None or plist == None:
		raise ValueError("mult_file_downey (file=filename|rootv=root value, n=number of iters, model=mult model, params=model params")

	simvs = run_sim(root_value, model_name, plist, n, minsize)
	return simvs
