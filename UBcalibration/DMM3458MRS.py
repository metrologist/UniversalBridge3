# ACAL all for DMM3458A with GPIB #22
# Use OHM commands not OHMF command for the resistance reading
# gpib 23 and NPLC=200 updated on10/06/2026
# copied from KJ ACAL all from pyvisa import *
# used for Resistance measurement @04/11/2024
# NOTE: The Ohm range selection is activated only adfter the measurement starts after DMM panel's overload message.
"""20/02/23:
simplified the reading and outputs with:
No copies of every reading, only means and sd saved
  reading of value in the ways of float(meter.read()[:-2]
  set the measurement samples number n 100
  stop watch for 20 reading  .77 mins
  3 readings  0.22 mins
  100 readings 3.38min

   Change the outputs format in order to save transfer time by excel"""


import pyvisa
import time
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
# corrected the syntax errors due to missing space in commands: 'NPLC*' and 'RANGE*'
time.sleep(1)


def measureR():
    rm = pyvisa.ResourceManager()
    print(rm.list_resources())
    meter = rm.open_resource('GPIB0::23::INSTR') #23 for #664; sn: 5149;
    meter.write('end 2')
    id, line = meter.write('ID?'), meter.read()[:-2]
    item = input('Item?:')
    prile(f'Resistor {item} me]asured by {line} with ID number {id}')
    meter.write('LINE?')
    prile('mains frequency =', meter.read()[:-2])
    meter.write('TEMP?')
    prile('temperature =', meter.read()[:-2])
    print("Reset before measurement starting")
    meter.write('RESET')
    time.sleep(5)
    meter.write('end 2')
    meter.write('NPLC 30')
    meter.write('OHMF')
    resist_range = input('Range?:')
    start = time.time()
    prile('Range?:', resist_range, 'Item?:', item)
    meter.write('RANGE ' + resist_range,)
    meter.write('OCOMP ON')
    meter.write('TARM SYN')
    meter.write('LFREQ LINE')
    trail_01 = float(meter.read()[:-2])
    time.sleep(2)
    trail_02 = float(meter.read()[:-2])
    prile('Trail1', trail_01 ,'Trail2', trail_02)
    time.sleep(2)

    result = []
    number_rdgs = 100
    for nums in range(number_rdgs):
        meter.write('LFREQ LINE')
        a = float(meter.read()[:-2])
        result.append(a)
    meter.write('TARM AUTO')

    prile('at', f'{time.asctime(time.localtime())}', f'{item}', 'reading is:')
    rs_mean = np.average(result)
    prile("Resistance_mean:", rs_mean)
    rs_dev = np.std(result, ddof=1)
    prile("Resistance_stdevp:", rs_dev)
    finish = time.time()
    prile('Time taken = ', (finish - start) / 60.0, 'minutes')
    prile('----------------')


if __name__ == '__main__':
    print('Resistance measurement')
    while True:
        taking_reading = input('Start to measure a resistor? yes to confirm, others to quit')
        if taking_reading.lower() != 'yes':
            prile('end of the measurement')
            break
        else:
            measureR()
        continue
"""test all good 27/01/23"""
