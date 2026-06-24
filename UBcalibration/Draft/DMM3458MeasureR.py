# ACAL all for DMM3458A with GPIB #22
# copied from KJ ACAL all from pyvisa import *
# revalue on the difference in 2023
# Not for measuring anything else -- Noted @04/11/2024, as it's designed for comparison of
# two different measurement methods
import pyvisa
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
def measureR():
    rm = pyvisa.ResourceManager()
    print(rm.list_resources())
    meter = rm.open_resource('GPIB0::22::INSTR')
    meter.write('end 2')
    meter.write('ID?')
    prile(meter.read()[:-2])
    meter.write('LINE?')
    prile('mains frequency =', meter.read()[:-2])
    meter.write('TEMP?')
    prile('temperature =', meter.read()[:-2])
    prile("Reset before measurement starting")
    meter.write('RESET')
    time.sleep(5)

    meter.write('end 2')
    meter.write('NPLC20')
    meter.write('OHMF')

    resist_range = input ('Range?:')
    prile('Range?:', resist_range)

    item = input ('Item?:')
    prile('Item?:', item)

    meter.write('RANGE' + resist_range)
    meter.write('OCOMP ON')
    meter.write('TARM SYN')
    meter.write('LFREQ LINE')
    prile('Trail1', float(meter.read()[:-2]))
    time.sleep(2)
    prile('Trail2', float(meter.read()[:-2]))
    time.sleep(2)

    result = []
    re_b = []
    number_rdgs = 20
    for reading in range(number_rdgs):
        meter.write('LFREQ LINE')
        a = meter.read()
        b = float(meter.read()[:-2])

        a = float(a[:-2])
        result.append(a)
        re_b.append(b)
        prile(reading, a)
        prile(reading, b)

    meter.write('TARM AUTO')
    a_mean = np.average(result)
    prile("A_mean:", a_mean)
    a_dev = np.std(result, ddof=1)
    prile("A_stdevp:", a_dev)
    b_mean = np.average(re_b)
    prile("B_mean:", b_mean)
    b_dev = np.std(result, ddof=1)
    prile("B_stdevp:", b_dev)


    prile('Result')
    prile("Time:", time.asctime(time.localtime()))
    prile("A_mean:", np.average(result))
    prile("A_stdevp:", np.std(result, ddof=1))
    prile("B_mean:", np.average(re_b))
    prile("B_stdevp:", np.std(re_b, ddof=1))


if __name__ == '__main__':
    print_hi('Resistance measurement')
    measureR()
"""test all good 27/01/23"""