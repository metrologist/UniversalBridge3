# ACAL all for DMM3458A with GPIB #22
# copied from KJ ACAL all from pyvisa import *

"""20/02/23:
simplifie the rading and outputs with:
No copies of every reading, only means and sd saved
  reading of value in the ways of float(meter.read()[:-2]"""


import random as rd
import numpy as np
from auxiliary import *

"""Run this after daily ACAL by DMM3458ACAL.py
reassigned Teflon cable color code:
                    High                             Low
            Cable   SR_box      DMM    |     Cable   SR_box      DMM
Current     Black   (1)    (High 2w)   |     White   (4)        (Low 2w)
Voltage     Red     (2)    (High 4w)   |     Green   (3)        (Low 4w)

And (#) are the ternimals number of SR104 for both Resistor and Temperature side 
"""

# Use a breakpoint in the code line below to debug your script.
time.sleep(1)



"""test all good 27/01/23"""
def measureR():

    item = input('Item?:')


    result = []
    number_rdgs = 20
    for nums in range(number_rdgs):
        a = rd.randint(0,nums)
        print(f"reading{nums} has random {a}")
        result.append(a)
        print(result)

    prile('Result')
    prile("Time:", time.asctime(time.localtime()))
    rs_mean = np.average(result)
    prile(f"{item} reading are")
    prile("Resistance_mean:", rs_mean)
    rs_dev = np.std(result, ddof=1)
    prile("Resistance_stdevp:", rs_dev)
    prile("---------")

if __name__ == '__main__':
    print_hi('Resistance measurement')
    measureR()
"""test all good 27/01/23"""
