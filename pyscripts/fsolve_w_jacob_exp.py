import numpy as np
import scipy.optimize as opt

'''
f1(x,y) = x^2 + y^2 - 50 = 0
f2(x,y) = xy - 25 = 0
J = [[2x, 2y]; [x y]]

Solve using fsolve
'''

def jacobian(params, *args):
	x = params[0]
	y = params[1]

	if args != None:
		some_dict = args[0]	
		print "Truth: ", some_dict["truth"]
		if "new_truth" in some_dict:
			print "New Truth: ", some_dict["new_truth"]

		some_dict["new_truth"] = False

	return np.array([[2*x, 2*y], [x, y]])

def func(params, *args):
	x = params[0]
	y = params[1]
	return np.array([x**2 + y**2 - 50, x*y - 25])

def solver_main():
	other_args = {"truth": True}
	(fval, infodict, ier, mesg) = opt.fsolve(func, [0,0], (other_args), jacobian, 1, 0)
	
	print "Fval: ", fval

if __name__ == "__main__":
	solver_main()
