# Sql query execution

import sqlite3 as sq
import os
import sys

class RunSQL:
	
	def __init__(self, dbname):
		self.conn = sq.connect(os.getenv("TRACE_DB_LOC", "./") + "/" + dbname)

	def __del__(self):
		if self.conn != None:
			self.conn.close()

	def makelist(self, res):
		n = len(res)
		newres = [None]*n
		i = 0
		while i < n:
			# Multi-dimensional only if needed.
			if len(res[i]) > 1:
				newres[i] = list(res[i])
			else:
				newres[i] = res[i][0]
			i = i + 1
		return newres
	
	def sqlq(self, qry):
		cur = self.conn.cursor()
		cur.execute(qry)
		res = cur.fetchall()
		cur.close()

		return self.makelist(res)

if __name__ == "__main__":
	try:
		dbname = sys.argv[1]
		qry = sys.argv[2]

		sqlr = RunSQL(dbname)

		res = sqlr.sqlq(qry)
		print res	
	except BaseException as be:
		print "in be:"
		print str(be)
	except:
		print "Unknown error"
