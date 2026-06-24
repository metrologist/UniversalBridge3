# ACAL all for DMM3458A with GPIB #22
# copied from KJ ACAL all from pyvisa import *
import pyvisa
import time
from auxiliary import *

"""Run An ACAL """


# Use a breakpoint in the code line below to debug your script.
def cal():
    rm = pyvisa.ResourceManager()
    print(rm.list_resources())
    meter = rm.open_resource('GPIB0::23::INSTR')
    meter.write('end 2')
    meter.write('ID?')
    prile(meter.read()[:-2])
    meter.write('LINE?')
    prile('mains frequency =', meter.read()[:-2])
    meter.write('TEMP?')
    prile('temperature =', meter.read()[:-2])
    prile("ACAL starting")
    start = time.time()
    meter.timeout = 360000

    meter.write('ACAL')
    finish = time.time()
    prile("ACAL finished")
    prile('Time taken = ', (finish - start) / 60.0, 'minutes')
    meter.write('TEMP?')
    prile('temperature =', meter.read()[:-2])
    prile('Cal done')
    meter.close()


if __name__ == '__main__':
    print_hi('Auto Calibration')
    cal()
    before_DMM_in_use()

# works fine, tried in 27/01/2023 : 14:16
# Run 31/01/2023 08:16 Okay
