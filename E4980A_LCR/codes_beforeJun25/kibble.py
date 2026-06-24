# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import pyvisa as visa
from time import sleep
from datetime import datetime, date
from Print_file import prile
import numpy as np
import matplotlib.pyplot as plt

class READING:
    def __int__(self):
        pass
    def ser_indandrest(self):
        rm = visa.ResourceManager()
        lcr = rm.open_resource('GPIB0::17::INSTR')
        lcr.timeout = 30000
        lcr.clear()
        lcr.write("*CLS")
        lcr.write(":FORMAT:ASCii:LONG ON")
        prile("lcr name:", "KeySight E4980A")
        lcr.write(":DISP:CCL")  # clears on screen error messages

        # Request description of Resistor under test
        Resistor_description = input('Cable name :')
        prile('Name and description of Resistor under test: ', Resistor_description)
        lcr.write("FETC:SMON:IAC?")
        print('IAC =', lcr.read())
        lcr.write("FETC:SMON:VAC?")
        print('VAC =', lcr.read())
        # lcr.write("FETC:FREQ?")
        # print('FREQ =', lcr.read())
        # print("Range:", gpibrange)
        # prile("Range", gpibrange)
        # setup time of test: 27 - 30

        now = datetime.now()
        today = date.today()
        current_time = now.strftime("%H:%M:%S")
        prile(today, current_time)

        # lists for plotting
        plotf = []
        plotrs = []  # Resistance
        plotrsu = []  # Unc of Res
        plotls = []  # Inductance
        plotlsu = []  # unc of Ind

        # setup the measurement
        n = 16  # number of readings at each frequency

        # Sets of Freq for cable
        freq_list = [20, 25, 30, 40, 53, 60, 65, 80, 90, 95, 103, 105, 107, 110, 112, 115, 120, 122, 125, 127, 130, 132, 135, 137, 140, 142, 145, 150, 153, 155, 160, 165, 170, 172, 175, 180, 185, 200, 220, 240, 400, 800, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 10000, 12000, 14000, 16000, 16500, 17000, 17500, 18000, 18500, 19000, 19500, 20000, 20500, 21000, 22000, 24000, 25000, 30000, 40000, 50000, 60000, 70000, 80000, 90000, 100000, 200000]
        #
        prile("select the freq range", freq_list)

        frequencies = []
        for x in freq_list:
            frequencies.append(str(x))  # integer value raised to kHz
            plotf.append(x)  # for plotting against frequency

        for f in frequencies:
            induc = []  # to accumulate inductance readings
            resis = []  # to accumulate Resistance readings
            current = []
            voltage = []
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
                    lcr.write("FETC:SMON:IAC?")
                    current.append(float(lcr.read()))
                    lcr.write("FETC:SMON:VAC?")
                    voltage.append(float(lcr.read()))
                except NameError:
                    prile('some Visa error?')
                prile(float(f), float(Ls), float(Rs), current[i], voltage[i])
            lcr.write("*LRN?")  # will dump all the setting commands for the meter
            setup = lcr.read()
            prile('Freq', f, 'Rs', np.average(resis), np.std(resis, ddof=1), 'Ls', np.average(induc),
                  np.std(induc, ddof=1))
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
        # dump plottable data
        prile('Frequency', 'Resistance','uR','Inductance','uL')
        for i in range(len(plotf)):
            prile(plotf[i], plotrs[i], plotrsu[i], plotls[i], plotlsu[i])

        pass
    pass



if __name__ == '__main__':
    rdg = READING()
    rdg.ser_indandrest()

