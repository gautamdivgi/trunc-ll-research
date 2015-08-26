#! /usr/bin/python

import rpytools.sql as sql
import rpytools.util as util

def main():
	day_list = [13,14,15,16,17,18,19,20]
	sql_str = "select bytes from flows where day = "	
	unc = sql.RunSQL("unc.db")

	for d in day_list:
		fname = "flow_" + str(d)
		dsql_str = sql_str + str(d)
		
		print "Running query --> SQL: ", dsql_str
		f = unc.sqlq(dsql_str)

		print "Writing data --> file: ", fname
		util.write_data(fname, f)
		del(f)

if __name__ == "__main__":
	main()

