# ACAL all for DMM3458A with GPIB #22
# copied from KJ ACAL all from pyvisa import *
import random  as rm
import numpy as np
from auxiliary import *
"""Run An ACAL """

# Use a breakpoint in the code line below to debug your script.
time.sleep(1)
def measureR():

    result = []
    re_b = []
    number_rdgs = 120
    for reading in range(number_rdgs):
        a = rm.randint(0, reading)
        b = rm.randint(reading, number_rdgs)
        result.append(a)
        re_b.append(b)
        prile(reading, a)
        prile(reading, b)
    print(result, len(result))
    print(re_b, len(re_b))
    a_mean = np.average(result)
    prile ("mean:", a_mean)
    a_dev = np.std(result, ddof=1)
    prile("stdevp:", a_dev)
    b_mean = np.average(re_b)
    prile ("mean:", b_mean)
    b_dev = np.std(result, ddof=1)
    prile("stdevp:", b_dev)
    # prile("mean:", np.average(re_b)  ??
    # prile("stdevp:", np.std(re_b, ddof=1))  ??


if __name__ == '__main__':
    print_hi('check numpy module')
    measureR()