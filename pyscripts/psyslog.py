#! /usr/bin/python

## Program to process syslog data from UNC
## The input is rows TS, DAY, AP, CLIENT, AP_OS, EVENT, REASON
## Output Rows DAY, CLIENT, AP, START, END, SLEN
## Process using the 802.11 b state machine
## Connect states are Associated, Authenticated, Re-associated
## Disconnect states are Roamed, Disassociated, Deauthenticated
## The original authors Papadopouli et. al describe visit and session lengths
## Visit lengths are AP specific
## Session lengths are the entire session
## We only look at Visits and call them sessions.

## Logic 
## Initialize client to an initial UNKNOWN state = -1
## Visit starts on when 2 events are received - Authenticated & Associated
## Visit ends when 2 events are received - Deauthenticated & Disassociated
## Deauth/Disassoc reason should be Successful or Sender leaving..., not Inactivity.
## Inactivity is an invalid visit - discard
## Re-assoc to same AP extends the visit
## Re-assoc to different AP starts a new visit and ends previous visit

from rpytools.sql import RunSQL
import sqlite3
import atexit

event_list = list()

seslen_conn = None

def close_connection():
	global seslen_conn
	if seslen_conn != None:
		try:
			seslen_conn.close()
		except BaseException as be:
			pass
	seslen_conn = None

def get_connection():
	global seslen_conn
	if seslen_conn == None:
		seslen_conn = sqlite3.connect("/home/gautam/dbs/syslog_final.db")
		atexit.register(close_connection)
	return seslen_conn

def insert_event_list():
	conn = get_connection()
	print "Deleting exsting values..."
	conn.execute("delete from seslen")
	conn.commit()
	qry = "insert into seslen(day, client, ap, start, end, len) values (?, ?, ?, ?, ?, ?)"
	try:
		for event in event_list:
			if event["valid"] == True:
				v = (event["day"], event["client"], event["ap"], event["sts"], event["ets"], event["ets"]-event["sts"])
				print "Inserting values: ", v
				conn.execute(qry, v)
		conn.commit()
	except BaseException as be:
		conn.rollback()
		print(be)


def getDayList():
	r = RunSQL("syslog_tmp.db")
	dayList = r.sqlq("select distinct day from syslog")
	return dayList

def getClientList(dayNum):
	qry = "select distinct client from syslog where client > 0 and day = " + str(dayNum)
	r = RunSQL("syslog_tmp.db")
	clientList = r.sqlq(qry)
	return clientList

def processClientVisits(dayNum, clientNum):
	TS=0
	AP=1
	EVENT=2
	REASON=3

	qry = "select ts, ap, event, reason from syslog where client = " + str(clientNum) + " and day = " + str(dayNum) + " order by ts,ap"
	r = RunSQL("syslog_tmp.db")
	l = r.sqlq(qry)

	current_ap = None
	event_map = dict()

	for l1 in l:
		event_ts = l1[TS]
		event_ap = l1[AP]
		event = l1[EVENT]
		event_reason = l1[REASON]

		emap_key = str(clientNum) + "-" + str(event_ap)
		if emap_key in event_map:
			# Exists
			if ( "deauthenticated" == event.lower() or "disassociated" == event.lower() ):
				if ( event_reason.lower().find("is leaving") > 0 or event_reason.lower().find("success") > 0 ):
					event_entry = event_map[emap_key]
					event_entry["ets"] = event_ts
					event_entry["valid"] = True
					event_list.append(event_entry)
				event_map.pop(emap_key)
		else:
			#First entry
			if ( "associated" == event.lower() or "reassociated" == event.lower() ):
				event_entry = dict()
				event_entry["day"] = dayNum
				event_entry["sts"] = event_ts
				event_entry["ets"] = None
				event_entry["valid"] = False
				event_entry["ap"] = event_ap
				event_entry["client"] = clientNum
				event_entry["event"] = event
				event_map[emap_key] = event_entry
			else:
				## Do nothing - invalid
				pass
		
	return event_list



if __name__ == "__main__":
	l1 = getDayList()

	for l11 in l1:
		print "Processing day: ", l11
		l2 = getClientList(l11)
		for l22 in l2:
			print "Processing client: ", l22
			processClientVisits(l11, l22)
	insert_event_list()


