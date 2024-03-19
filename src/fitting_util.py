
import numpy as np
from scipy.optimize import curve_fit, leastsq

# functions to try
functions = {
    'constant' : {'func': lambda p, x: np.array([p[0] for dx in x]), 'pinit': [50.] },
    'line': {'func': lambda p, x : np.array([(p[1] * dx) + p[0] for dx in x]),
             'pinit': [0.,1.]},
    'quadratic' : { 'func': lambda p, x: np.array([ (p[2] * dx * dx) + (p[1] * dx) + p[0] for dx in x]),
                  'pinit': [0.,1.,1.] },
    'step': {'func': lambda p, x: np.array([p[1] if dx <= p[0] else p[2] for dx in x]),
            'pinit': [5.,0.1,1.]},
    'gaussian' : {'func': lambda p, x: np.array(p[0]*np.exp(-np.power(x - p[1], 2)/(2*np.power(p[2], 2)))),
                  'pinit': [1.,5.,1.]},
}

def fit_leastsq(p0:list, datax:list, datay:np.array, fitfunc:object, y_err:list=[])->list:
    ''' LeastSquares fit with no y errors
    Usage : 
    pfit, perr = fit_leastsq(pstart, xdata, ydata, ff)
    '''

    if len(y_err) == len(datay):
        # our error function when we have errors
        errfunc = lambda p, x, y, err: (y - fitfunc(p, x)) / err
    else:
        errfunc = lambda p, x, y, err: y - fitfunc(p, x) 

    pfit, pcov, infodict, errmsg, success = \
        leastsq(errfunc, p0, args=(datax, datay, y_err), full_output=1, epsfcn=0.0001)

    redchisq = -1.
    if (len(datay) > len(p0)) and pcov is not None:

        # calculate reduced chisq
        redchisq = redchisqg(datay, fitfunc(pfit, datax), nparam=len(p0), sd=y_err)

        # multiply pcov by redchisq 
        pcov = pcov * redchisq

    else:
        pcov = np.inf

    error = [] 
    for i in range(len(pfit)):
        try:
          error.append(np.absolute(pcov[i][i])**0.5)
        except:
          error.append( 0.00 )

    pfit_leastsq = pfit
    perr_leastsq = np.array(error) 

    return pfit_leastsq, perr_leastsq, redchisq


def fit_probability (pfit:list, redchisq:float)->float:
    from scipy.stats import chisqprob
    deg = len(pfit)
    chisq = redchisq * deg
    return chisqprob(chisq, deg) 


def redchisqg(ydata:np.array, ymod:np.array, nparam:int, sd:list=[]):  
    """  
    Returns the reduced chi-square error statistic for an arbitrary model,   
    chisq/nu, where nu is the number of degrees of freedom. If individual   
    standard deviations (array sd) are supplied, then the chi-square error   
    statistic is computed as the sum of squared errors divided by the standard   
    deviations. See http://en.wikipedia.org/wiki/Goodness_of_fit for reference.  
   
    ydata,ymod,sd assumed to be Numpy arrays. n is an integer.  
   
    Usage:  
    >>> chisq=redchisqg(ydata,ymod,n,sd)  
    where  
       ydata : data  
       ymod : model evaluated at the same x points as ydata  
       n : number of free parameters in the model  
       sd : "standard deviation", e.g. uncertainties in ydata  

    """  
    # Chi-square statistic  
    if len(sd) > 0:  
        chisq=np.sum(((ydata-ymod)/sd)**2 ) 
    else:
        chisq=np.sum((ydata-ymod)**2) 
             
    # Number of degrees of freedom   
    deg=ydata.size-nparam
        
    return chisq/deg 

