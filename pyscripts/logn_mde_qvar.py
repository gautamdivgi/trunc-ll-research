import numpy as np
import scipy.optimize as opt
import scipy.special as spec
from math import pi as pi
from math import e as e
from math import sqrt
from collections import namedtuple
from rpytools.util import ecdf
from rpytools.lognormal import Lognormal


def k(a_i):
    return sqrt(2.0)*spec.erfinv(2.0*a_i - 1.0)

def e1(x_i, u):
    return np.log(x_i) - u

def e2(e1_i, s):
    return e1_i/(sqrt(2.0)*s)

def e3(e2_i):
    return np.power(e2_i, 2.0)

def F_inv(k_i, u, s):
    return np.exp(u + k_i*s)

def F_x(e2_i, u, s):
    return 0.5*(1.0 + spec.erf(e2_i))

def F(F_inv_i, F_x_i):
    return F_x_i/f_inv_i

def e4(F_inv_i, e3_i):
    return 1.0/(F_inv_i * np.exp(e3_i))

def e5(e4_i, s):
    return (1.0/(sqrt(2.0*pi)*s))*e4_i

def e6(e5_i, s):
    return e5_i/s

def dF_du(F_i, e5_i):
    return -F_i - e5_i

def dF_ds(k_i, F_i, e1_i, e6_i):
    return -k_i*F_i - e1_i*e6_i

def ddF_dsdu(k_i, F_i, e1_i, e3_i, e5_i, e6_i):
    return k_i*F_i + k_i*e5_i - e1_i*(2.0*e3_i - 1.0)*e6_i + e6_i

def d2F_du2(F_i, e3_i, e5_i):
    return F_i - (2.0*e3_i - 1.0)*e5_i + e5_i

def d2F_ds2(k_i, F_i, e1_i, e3_i, e4_i, e6_i, s):
    return np.power(k_i, 2.0)*F_i + k_i*e6_i + (sqrt(2.0)/(pi*(s**3.0)))*e1_i*e4_i - e1_i*e6_i*(e3_i/s - k_i)

## The above values are actually intermediate values
## If there is a structure for common values
## The common values should be only what the solvers and the jacobian need

def create_initial_values(u, s, cvals):
    x_i = cvals.x
    a_i = vals.a
    k_i = cvals.k

    e1_i = e1(x_i, u)
    e2_i = e2(e1_i, s)
    e3_i = e3(e2_i)
    F_inv_i = F_inv(k_i, u, s)
    F_x_i = F_x(e2_i, u, s)
    F_i = F(F_inv_i, F_x_i)
    e4_i = e4(F_inv_i, e3_i)
    e5_i = e5(e4_i, s)
    e6_i = e6(e5_i, s)
    dF_du_i = dF_du(F_i, e5_i)
    dF_ds_i = dF_ds(k_i, F_i, e1_i, e6_i)
    ddF_dsdu_i = ddF_dsdu(k_i, F_i, e1_i, e3_i, e5_i, e6_i)
    d2F_du2_i = d2F_du2(F_i, e3_i, e5_i)
    d2F_ds2_i = d2F_ds2(k_i, F_i, e1_i, e3_i, e4_i, e6_i, s)

    svals.F = F_i
    svals.dF_du = dF_du_i
    svals.dF_ds = dF_ds_i
    svals.ddF_dsdu = ddF_dsdu_i
    svals.d2F_du2 = d2F_du2_i
    svals.d2F_ds2 = d2F_ds2_i

def logn_solver(ivals, *args):
    u = ivals[0]
    s = ivals[1]

    cvals = args[0]
    create_initial_values(u, s, cvals)

    nu = np.sum(cvals.x2*cvals.dF_du - ((cvals.a2*cvals.dF_du)/np.power(cvals.F, 2.0)))/n
    ns = np.sum(cvals.x2*cvals.dF_ds - ((cvals.a2*cvals.dF_ds)/np.power(cvals.F, 2.0)))/n

    return [nu, ns]

def jacobian_11(cvals):
    t1 = cvals.x2*cvals.d2F_du2
    t2 = cvals.d2F_du2/np.power(cvals.F, 2.0)
    t3 = (2.0*np.power(cvals.dF_du, 2.0))/np.power(cvals.F, 3.0)

    jval = np.sum(t1 - cvals.a2*(t2-t3))/cvals.n
    return jval

def jacobian_12_21(cvals):
    t1 = cvals.x2*cvals.ddF_dsdu
    t2 = cvals.ddF_dsdu/np.power(cvals.F, 2.0)
    t3 = (2.0*cvals.dF_ds*cvals.dF_du)/np.power(cvals.F, 3.0)

    jval = np.sum(t1 - cvals.a2*(t2-t3))/cvals.n
    return jval

def jacobian_22(cvals):
    t1 = cvals.x2*cvals.d2F_ds2
    t2 = cvals.d2F_ds2/np.power(cvals.F, 2.0)
    t3 = (2.0*np.power(cvals.dF_ds, 2.0))/np.power(cvals.F, 3.0)

    jval = np.sum(t1 - cvals.a2*(t2-t3))/cvals.n
    return jval

def jacobian(ivals, *args):
    cvals = args[0]

    j11 = jacobian_11(cvals)
    j12 = jacobian_12_21(cvals)
    j21 = j12
    j22 = jacobian_22(cvals)

    return np.array([[j11, j12], [j21, j22]])


def solver_main(data_pts):
    ## Scrub the data points and remove 0 values

    ## Ideally we should get an np array
    ## But if not --
    dp = np.array(data_pts)
    dp_i = dp[np.where(dp > 0.0)]
    cdf_i = ecdf(dp_i, issorted=False)
    x_i = cdf_i[:, 0]
    a_i = cdf_i[:, 1]

    i_u, i_s = Lognormal.mmefit(dp_i)

    val_list = ['x', 'a', 'x2', 'a2', 'n', 'k', \
                'F', 'dF_du', 'dF_ds', \
                'ddF_dsdu', 'd2F_du2', 'd2F_ds2']
    svals = namedtuple('svals', val_list)
    cvals = svals(x=x_i,
                  a=a_i,
                  x2=np.power(x_i, 2.0), \
                  a2=np.power(a_i, 2.0), \
                  n=float(len(x_i)), \
                  k=k(a_i), \
                  F=None, \
                  dF_du=None, \
                  dF_ds=None, \
                  ddF_dsdu=None, \
                  d2F_du2=None, \
                  d2F_ds2=None)

    (fval, infodict, ier, msg) = opt.fsolve(logn_solver, \
                                            [i_u, i_s], \
                                            (cvals), \
                                            jacobian, \
                                            1, \
                                            0)
    if ier != 1:
        print "Failed to converge: ", msg
    print "u: ", fval[0]
    print "s: ", fval[1]
