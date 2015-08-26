import math
import util
import scipy.optimize as opt
import numpy as np

"""
The Log-logistic distribution - the heavy tailed counter part of MODLAV or TRUNC-LL
"""

class LogLogisticConvergenceError(Exception):
	def __init__(self, mesg, values):
		self.__mesg = mesg
		self.__alpha = values[0]
		self.__beta = values[1]
	
	def __str__(self):
		prms = {"alpha": self.__alpha, "beta": self.__beta}
		return self.__mesg + " use the following parameters to verify manually - " + str(prms)
	
	def __repr__(self):
		prms = {"alpha": self.__alpha, "beta": self.__beta}
		return self.__mesg + " use the following parameters to verify manually - " + str(prms)

	def alpha(self):
		return self.__alpha

	def beta(self):
		return self.__beta

class LogLogistic:
	"""
	The log-logistic distribution
	"""
		
