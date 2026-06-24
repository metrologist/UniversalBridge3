
# for L/R readings at one frequency point ONLY
# Removed the plots
# Modified this program to take the reading of very dials of the inductors and list all readings in a spreadsheet
# with the output format of "name of the unit", "condition of the measurement", "dial", "L" and "R"


import pyvisa as visa
from time import sleep
from datetime import datetime, date
import csv
import numpy as np

# Setup instrument: 14 - 23
rm = visa.ResourceManager()
lcr = rm.open_resource('GPIB0::17::INSTR')
lcr.timeout = 30000
lcr.clear()
lcr.write("*CLS")
lcr.write(":FORMAT:ASCii:LONG ON")

# Request description of the inductor under test
DUT_description = input('Enter DUT name with description: "Location and probe type": ')
# Prepare output file with the date of measurement
today = str(date.today())
output_file = 'E4980A_LR_' + today + '_with_' + DUT_description + '.csv'
with open(output_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    # Writing header
    writer.writerow(["DUT", "Measurement Condition", "frequency", "Dial", "L", "L_Std", "R", "R_Std"])

# Setup test time
now = datetime.now()
today = date.today()
current_time = now.strftime("%H:%M:%S")

print("Test date:", today)
print("Test time:", current_time)


# Configuration parameters
n = 9  # Number of readings per frequency
# freq_list = [1591.5494309189535]  # one Frequency point (in 10k Omega)
freq_list = [1591.5494309189535, 1671.126902464901]
dials = ["Dial 0", "Dial 1", "Dial 2", "Dial 3", "Dial 4", "Dial 5", "Dial 6", "Dial 7", "Dial 8", "Dial 9", "Dial 10"]

# Loop for each dial
for dial in dials:
    next_dail_ready = input(f'dial to the right position:{dial}, get ready for the next."YES?"?')
    if next_dail_ready.lower() != 'yes':
        print('end of the measurement')
        break
    else:
        # temp = input('DUT Temperature is')
        temp = "20.50 as setting"
        condition = f"Temperature at {dial} is {temp}"
        # Loop for each frequency
        for f in freq_list:
            induc = []  # To accumulate inductance (L) readings
            resis = []  # To accumulate resistance (R) readings
            lcr.write(":FREQ " + str(f))
            sleep(5)  # Allow settling time at new frequency/range

            # Take multiple readings
            for i in range(n):
                try:
                    lcr.write("FETCH?")
                    Ls, Rs, _ = lcr.read().split(',')
                    induc.append(float(Ls))
                    resis.append(float(Rs))
                except Exception as e:
                    print(f"Error during measurement: {e}")

            # Calculate averages and write results
            avg_L = np.average(induc)
            dev_L = np.std(induc, ddof=1)
            avg_R = np.average(resis)
            dev_R = np.std(resis, ddof=1)
            print(f"Frequency: {f} Hz, Avg L: {avg_L}, Std L: {dev_L}")
            print(f"Frequency: {f} Hz, Avg R: {avg_R}, Std R: {dev_R}")
            sleep(3)
            print(f"current frequency:{f} done")
            # Save results in CSV
            with open(output_file, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([DUT_description, condition, f, dial, avg_L, dev_L, avg_R, dev_R])
print("\nMeasurement finished. Results saved to", output_file)
now_1 = datetime.now()
current_time_1 = now_1.strftime("%H:%M:%S")
print("Finish time:", current_time_1)
total_time = (now_1 - now) / 60
print(f"---total time used {total_time}")
print("---")

lcr.close()
rm.close()