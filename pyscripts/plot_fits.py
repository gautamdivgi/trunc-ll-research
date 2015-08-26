from matplotlib import pyplot as plt
import rpytools.plotdata as pdata
from rpytools.util import read_data
from rpytools.sql import RunSQL
import os
import shutil

def get_dataset_info(tag):
	q = "select filename from datasets where unique_id = '" + tag + "'"
	r = RunSQL("files_and_analysis.db")
	rs = r.sqlq(q)
	filename = rs[0].replace("/home/gautam", os.getenv("HOME"))
	return {"dir": os.path.dirname(filename), "file": os.path.basename(filename)}

def validate_data_files(dset_file, dset_type):
	if dset_type == "cdf":
		tag = pdata.cdf_tag
	elif dset_type == "ccdf":
		tag = pdata.ccdf_tag
	else:
		tag = ""
		validation = False
		print "\t Invalid tag", dset_type
	
	file_map = dict()
	dset_dir = dset_file["dir"]
	name = dset_file["file"] + tag

	file_name = os.path.join(dset_dir, name)

	validation = True
	validation = validation & os.access(file_name, os.F_OK)
	file_map["emp_" + dset_type] = file_name
	print "\t Validating - " + file_name, validation

	for dist in pdata.dist_map:
		ext = pdata.dist_map[dist]["ext"]
		dist_file = file_name + "." + ext

		validation = validation & os.access(dist_file, os.F_OK)
		file_map[ext + "_" + dset_type] = dist_file
		print "\t\t Validating - " + dist_file, validation

	return (validation, file_map)

def prepare_file(file_name):
	"""
	Create directory if it does not exist
	Remove file if it exists
	"""
	dir = os.path.dirname(file_name)
	if ( os.access(dir, os.F_OK) == False ):
		print "\t Creating dir", dir
		os.mkdir(dir)
	else:
		if ( os.access(file_name, os.F_OK) == True ):
			print "\t\t Removing file", file_name
			os.remove(file_name)

def plot_data(dist, fset, dset, qset):
	plt.interactive(False)
	plt.rcParams['font.size'] = 17.0

	dist_params = pdata.dist_map[dist]
	ext = dist_params["ext"]
	typ = dset["type"]

	emp_key = "emp_" + typ
	emp_file = fset[emp_key]
	dist_key = ext + "_" + typ
	dist_file = fset[dist_key]

	p1 = read_data(emp_file)
	p2 = read_data(dist_file)

	xlabel = dset["xlabel"]
	ylabel = dset["ylabel"]
	l1 = dset["legend1"]
	l2 = dset["legend2"].replace(pdata.dist_replace_string, dist_params["legend"])
	loc = dset["loc"]

	if ( typ == "cdf" ):
		plt.plot(p1[:,0], p1[:,1], 'k-', label=l1)
		plt.plot(p2[:,0], p2[:,1], 'k--', label=l2)
	else:
		plt.loglog(p1[:,0], p1[:,1], 'k-', label=l1)
		plt.loglog(p2[:,0], p2[:,1], 'k--', label=l2)

	if "xlim" in dset:
		plt.xlim(dset["xlim"])
	if "ylim" in dset:
		plt.ylim(dset["ylim"])
	if "xticks" in dset:
		plt.xticks(dset["xticks"])
	if "yticks" in dset:
		plt.yticks(dset["yticks"])
	plt.grid()
	plt.xlabel(xlabel)
	plt.ylabel(ylabel)
	plt.legend(loc=loc, frameon=False)

	dir = qset["dir"]
	fname = qset["file"]

	eps_file = dset["tag"].lower() + "_" + typ + "_" + ext + ".eps"
	plot_dir = os.path.join(dir, pdata.plot_dir)
	image_file = os.path.join(plot_dir, eps_file)

	prepare_file(image_file)

	plt.savefig(image_file)
	print "\t Created plot", image_file
	plt.close()

def plot_main():
	for dset in pdata.dataset_list:
		f = get_dataset_info(dset["tag"])
		validation_results = validate_data_files(f, dset["type"])
		is_valid = validation_results[0]
		file_set = validation_results[1]
		if ( is_valid == True ):
			for dist in pdata.dist_map:
				plot_data(dist, file_set, dset, f)
		else:
			print "Invalid data - ", f

if __name__ == "__main__":
	plot_main()



