# Use KeySight E4980A to measure TS
# V2: To get the readings of R and L,
# To have more harmonics frequency to 10kHz------
# to have multiplots, take the reading of Rs and Ls
# Add the 47 and 53 Hz
# import libraries 7- 9
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
n = int(input("number of measurement?",))  # number of readings at each frequency

# freq_list = [47, 53, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600,
#              650, 700, 750, 800, 850, 900, 950, 1000, 2000, 3000, 5000, 8000, 10000] #full range
# freq_list = [20, 300, 400, 650, 950, 100, 500,] # short wider
# freq_list = [50, 100, 147, 153, 200, 250, 150] # short Narrow
freq_list = [47, 53, 97, 103, 147, 153, 197, 203, 247, 253, 297, 303, 347, 353, 397, 403, 447, 453, 497, 503, 600,
             700, 800, 900, 1000, 2000, 3000, 5000] # Full Freq off harmonics
# measuring resistor from 50 Hz to 10kHz.

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
    prile(f, 'Rs', np.average(resis), np.std(resis, ddof=1), 'Ls', np.average(induc), np.std(induc, ddof=1))
    prile(setup)
    plotrs.append(np.average(resis))
    plotrsu.append(np.std(resis, ddof=1))
    plotls.append(np.average(induc))
    plotlsu.append(np.std(induc, ddof=1))

prile('---------run finished---------')  # leave space between capacitor results in csv file

prile()
lcr.write("*LRN?")  # will dump all the setting commands for the meter
setup = lcr.read()
prile(setup)


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
