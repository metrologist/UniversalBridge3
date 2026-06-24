# ACAL all for DMM3458A with GPIB #22
# copied from KJ ACAL all from pyvisa import *
import pyvisa
import time
from auxiliary import prile
"""Run An ACAL """

rm = pyvisa.ResourceManager()
print(rm.list_resources())
meter = rm.open_resource('GPIB0::22::INSTR')
meter.write('END ALWAYS')
meter.write('ID?')
prile(meter.read()[:-2])
meter.write('LINE?')
prile('mains frequency =', meter.read()[:-2])
meter.write('TEMP?')
prile('temperature =', meter.read()[:-2])
prile("ACAL starting")
start = time.time()

meter.timeout = 36000
finish = time.time()
meter.write('ACAL')
print('ACAL finished')
# print('Time taken = ', (finish - start) / 60.0, 'minutes')
# meter.write('TEMP?')
# print('temperature =', meter.read()[:-2])