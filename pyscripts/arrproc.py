#! /usr/bin/python

import datetime
import pytz
import os
import sys
import numpy
import util.sql as sql
import getopt

# Arrival process computation.
# 1st step 
# Compute the # of arrivals in interval (i). 
# 0:i-1,i:2i-1,.... (24 hour mark) per day

