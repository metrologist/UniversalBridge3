"""Not in Service
31/01/2023
"""

# ACAL all for DMM3458A with GPIB #22
# copied from KJ ACAL all from pyvisa import *
import pyvisa
import time
from auxiliary import prile
"""Run An ACAL """

# Use a breakpoint in the code line below to debug your script.
def print_hi(name = 'DMM 3468A CAL'):
    # Press Ctrl+F8 to toggle the breakpoint.

    print(f'Hi, {name}')

def cal():
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
    prile("ACAL starting")
    start = time.time()
    meter.write('ACAL ALL')
    meter.timeout =5000
    finish = time.time()
    prile("ACAL finished")
    prile('Time taken = ', (finish - start) / 60.0, 'minutes')
    meter.write('TEMP?')
    prile('temperature =', meter.read()[:-2])
    prile(time.asctime(time.localtime())
    # prile("ACAL has done")
    # prile(time.ctime())

    # print(f'Hi, now it is, {time.ctime()}')
    # # print(f'Hi, now it is, {time.localtime()}')
    # print('Please wait for at least 5 mins before using the meter after ACAL, thanks' )
    # time.sleep(3)
    # print(f'Hi, now it is, {time.ctime()}')
    #
    #

    print(f'Hi, now it is, {time.ctime()}')
    # print(f'Hi, now it is, {time.localtime()}')
    print('Please wait for at least 5 mins before using the meter after ACAL, thanks' )
    time.sleep(3)
    print(f'Hi, now it is, {time.ctime()}')



    #
    print('Hi, now it is,' time.ctime())
    print('Please wait for at least 5 mins before using the meter after ACAL, thanks' )
    time.sleep(3)
    print('Hi, now it is,' time.ctime(), 'DMM is ready')



    #
    #
    #
    #
    # print(f'Hi, now it is, {time.ctime()}')
    # # print(f'Hi, now it is, {time.localtime()}')
    # print('Please wait for at least 5 mins before using the meter after ACAL, thanks' )
    # time.sleep(3)
    # print(f'Hi, now it is, {time.ctime()}')
    #



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi()
    cal()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
