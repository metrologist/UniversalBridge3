# taking reading of Cp and Rp from E4980A and save readings to csv files
# 12/09/22 measure the Canford Audio Cables
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
Resistor_description = input('Cable name :')
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
plotRp = []   # Resistance
plotRpu = []  # Unc of Res
plotCp = []   # Inductance
plotCpu = []  # unc of Ind


# setup the measurement
n = 16  # number of readings at each frequency

# Sets of Freq for burden
freq_list = [50, 100, 200, 300, 500, 800, 1000, 1591.5494309189535, 2000, 3000, 5000]
#
prile("select the freq range", freq_list)


frequencies = []
for x in freq_list:
    frequencies.append(str(x))  # integer value raised to kHz
    plotf.append(x)  # for plotting against frequency

for f in frequencies:
    capac = []  # to accumulate capacitance readings
    resis = []  # to accumulate Resistance readings
# if not reset the list here, the average of list is not the readings in the only frequency point
    lcr.write(":FREQ " + f)
    sleep(5)  # settle at new frequency/range
    for i in range(n):
        Cp, Rp, code = 'NA', 'NA', 'NA'
        try:
            lcr.write("FETCH?")
            Cp, Rp, code = lcr.read().split(',')
            capac.append(float(Cp))
            resis.append(float(Rp))
        except NameError:
            prile('some Visa error?')
        prile(float(f), float(Cp), float(Rp))
    lcr.write("*LRN?")  # will dump all the setting commands for the meter
    setup = lcr.read()
    prile('Freq', f, 'Rp', np.average(resis), np.std(resis, ddof=1), 'Cp', np.average(capac), np.std(capac, ddof=1))
    prile(setup)
    plotRp.append(np.average(resis))
    plotRpu.append(np.std(resis, ddof=1))
    plotCp.append(np.average(capac))
    plotCpu.append(np.std(capac, ddof=1))

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
plt.errorbar(plotf, plotRp, plotRpu, color=color)
ax1.tick_params(axis='y', labelcolor=color)

plt.title('Resistance and Capacitance')
ax2 = ax1.twinx()
color = 'tab:green'
ax2.set_ylabel('Capacitance', color=color)  # we already handled the x-label with ax1
plt.errorbar(plotf, plotCp, plotCpu, color=color)
ax2.tick_params(axis='y', labelcolor=color)
plt.tight_layout()

# show plot
plt.show()
#$ repeat all 3 power source by wayenKerr
#*****

