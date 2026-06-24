# from C:\Users\zhangm7\OneDrive - Victoria University of Wellington - STAFF
# \Documents\9 Programs\00 Thesis Programs\new res\Nov_shunt_only_pps_powered.py
import pyvisa as visa
from time import sleep
from datetime import datetime, date
from Print_file import prile
import numpy as np
import matplotlib.pyplot as plt
# setup instrument: 14 - 23
rm = visa.ResourceManager()
lcr = rm.open_resource('GPIB0::17::INSTR')
lcr.timeout = 30000
lcr.clear()
lcr.write("*CLS")
lcr.write(":FORMAT:ASCii:LONG ON")
prile("lcr name:", "KeySight E4980A")

# Request description of Resistor under test
Resistor_description = input('Resist name :')
prile('Name and description of Resistor under test: ', Resistor_description)
lcr.write("FETCH:DCR:RANG:?")
print("GPIB source:", lcr.read)
prile("GPIB source:", lcr.read)
# setup time of test: 27 - 30
now = datetime.now()
today = date.today()
current_time = now.strftime("%H:%M:%S")
prile(today, current_time)

# lists for plotting
plotf = []
plotrs = []   # Resistance
plotrsu = []  # Unc of Res
plotls = []   # Inductance
plotlsu = []  # unc of Ind


# setup the measurement
n = 16  # number of readings at each frequency

# Sets of Freq for burden
freq_list = [47, 53,  197, 203, 497, 503, 997, 1003, 1997, 2003]
# Wider Freq range for the LCR Freq resp.....[3k - 100k]
# freq_list = [47, 53, 97, 103, 147, 153, 197, 203, 247, 253, 297, 303, 347, 353, 397, 403, 447, 453, 497, 503, 650, 750,
#              850, 950, 1000, 1050, 1500, 2000, 3000, 5000, 8000, 10000, 20000, 30000, 50000, 80000, 100000]
#
prile("select the freq range", freq_list)


frequencies = []
for x in freq_list:
    frequencies.append(str(x))  # integer value raised to kHz
    plotf.append(x)  # for plotting against frequency

for f in frequencies:
    induc = []  # to accumulate inductance readings
    resis = []  # to accumulate Resistance readings
# if not reset the list here, the average of list is not the readings in the only frequency point
    lcr.write(":FREQ " + f)
    sleep(5)  # settle at new frequency/range
    for i in range(n):
        Ls, Rs, code = 'NA', 'NA', 'NA'
        try:
            lcr.write("FETCH?")
            Ls, Rs, code = lcr.read().split(',')
            induc.append(float(Ls))
            resis.append(float(Rs))
        except NameError:
            prile('some Visa error?')
        prile(float(f), float(Ls), float(Rs))
    lcr.write("*LRN?")  # will dump all the setting commands for the meter
    setup = lcr.read()
    prile('Freq', f, 'Rs', np.average(resis), np.std(resis, ddof=1), 'Ls', np.average(induc), np.std(induc, ddof=1))
    prile(setup)
    plotrs.append(np.average(resis))
    plotrsu.append(np.std(resis, ddof=1))
    plotls.append(np.average(induc))
    plotlsu.append(np.std(induc, ddof=1))

print('***************************************')
lcr.write("*LRN?")  # will dump all the setting commands for the meter
setup = lcr.read()
prile(setup)



now = datetime.now()
current_time = now.strftime("%H:%M:%S")
prile(today, current_time)
prile('---------run finished---------')  # leave space between capacitor results in csv file

print('frequency list', plotf)
print('Run finished')
lcr.close()
rm.close()

fig, ax1 = plt.subplots(figsize=(16, 8))
color = 'tab:blue'
ax1.set_xlabel('Frequency (Hz)')
ax1.set_ylabel('Resistance', color=color)
plt.errorbar(plotf, plotrs, plotrsu, color=color)
ax1.tick_params(axis='y', labelcolor=color)

plt.title('Resistance and Inductance')
ax2 = ax1.twinx()
color = 'tab:green'
ax2.set_ylabel('Inductance', color=color)  # we already handled the x-label with ax1
plt.errorbar(plotf, plotls, plotlsu, color=color)
ax2.tick_params(axis='y', labelcolor=color)
plt.tight_layout()

# show plot
plt.show()
#$ repeat all 3 power source by wayenKerr
#*****

