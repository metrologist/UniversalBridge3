# reads the csv file produced by MeasureR.py
import csv
import os

class CSVDATA():
    def __init__(self, csvpath):
        """

        a class to read the csv file produced by MeasureR.py
        :param csvpath: just the file name, noting that the output method does not allow a folder name...
        """
        self.csvpath = csvpath
        self.data = []
        self.summary = []
        self.std_smry = []  # just the internal UB resistors

    def read_all(self):
        """

        reads the csv and creates a list of lists in self.data
        :return:
        """
        with open(self.csvpath, newline='') as csvfile:  # format must be correct
            reader = csv.reader(csvfile)
            for row in reader:
                self.data.append(row)

    def extract_summary(self):
        """

        :return:
        """
        if len(self.data) >= 1:
            # print('go')
            self.read_all()
            # for x in data_in.data:
            #     print(x)
            print('\n Extract lines')
            line = []
            for x in data_in.data:
                for y in x:
                    if 'reading is:' in y:  # find
                        line.append(x[1])
                    elif 'Resistor' in y:
                        line.append(y)
                    elif 'Resistance_mean:' in y:
                        line.append(float(x[1]))
                    elif 'Resistance_stdevp:' in y:
                        line.append(float(x[1]))
                if len(line) == 4:
                    self.summary.append(line)
                    line = []
        else:
            print('no go')

    def output(self):
        outfile = 'out_' + self.csvpath
        with open(outfile, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for x in self.summary:
                writer.writerow(x)
            if len(self.std_smry) > 1:
                for x in self.std_smry:
                    # print(x)
                    writer.writerow(x)


    def for_internal(self):
        internal_ref = []
        resistor_names = ['sens_sr104', 'sr104', 'ep100k', 'esp100k', 'er10_100k', 'es100k', 'g1', 'g2', 'R4A', 'R4C']
        name_select = {'SR04TS': 'sens_sr104', 'SN:109006': 'sr104', '100k Parallel': 'ep100k',
                       '100k Series Parallel': 'esp100k', '100k R10 only': 'er10_100k', '100k R1-R10': 'es100k',
                       'G1': 'g1',
                       'G2': 'g2', 'R4A': 'R4A', 'R2B': 'R4B', 'R4C': 'R4C'}
        for y in self.summary:
            line = []
            for x in name_select.keys():
                if x in y[0]:
                    line.append(name_select[x])
                    for z in y:
                        line.append(z)
                    internal_ref.append(line)
                    self.std_smry.append(line)
        return(internal_ref)


if __name__ == '__main__':
    input_csv = "E3458A_Res_2026-06-11.csv"
    data_in = CSVDATA(input_csv)
    data_in.read_all()
    data_in.extract_summary()
    # data_in.output()
    print('\n')
    references = data_in.for_internal()
    data_in.output()
    # for y in references:
    #     print(y)






    """
    spreadsheet names
    Sensor    SR104
    SR104
    SR104
    R4A
    Sensor    SR104
    SR104
    100    k
    esi    parallel    100    k
    esi    series - para    100    k
    esi    R10    100    k
    esi    series
    R4B
    G1
    R2
    R4C
    """
    """
    Resistor    Fluke    8508    A - 7000    K    Four - wire    shorting    PCB    410590 - A    me]asured    by    HP3458A    with ID number 5
    Resistor SR104 StdR (SN:109006)  me]asured    by    HP3458A    with ID number 5
    Resistor SR04TS(temperature Sensor) me]asured by HP3458A with ID number 5
    Resistor SR1010--100k Parallel with PC 101 (SN:937003) me]asured    by    HP3458A    with ID number 5
    Resistor SR1010--100k Series Parallel with PC 102( as above SN:937003) me]asured    by    HP3458A    with ID number 5
    Resistor SR1010--100k R10 only (SN:937003) me]asured    by    HP3458A    with ID number 5
    Resistor SR1010--100k R1-R10 inSeries (SN:937003) me]asured    by    HP3458A    with ID number 5
    Resistor SR1010_1k parallel_R1-R10 with Pc 101 (SN:923001) me]asured    by    HP3458A    with ID number 5
    Resistor SR1010_1k series parallel_R1-R9 with PC 102(SN:923001) me]asured    by    HP3458A    with ID number 5
    Resistor SR1010_1k R10 only (SN:923001) me]asured    by    HP3458A    with ID number 5
    Resistor SR1010_1k series R1-R10(SN:923001) me]asured    by    HP3458A    with ID number 5
    Resistor UB BNC BPO coax zero me]asured by HP3458A with ID number 5
    Resistor Vishay 100 (RHK02) me]asured by HP3458A with ID number 5
    Resistor Vishay 10k (UBCAL10k)  me]asured by HP3458A with ID number 5
    Resistor Vishay 100 (RHK02)-right me]asured by HP3458A with ID number 5
    Resistor 1e4 me]asured by HP3458A with ID number 5
    Resistor Vishay 10k (UBCAL10k)-right me]asured by HP3458A with ID number 5
    Resistor Vishay 10k (UBCAL10k) me]asured by HP3458A with ID number 5
    Resistor Vishay 100k  me]asured by HP3458A with ID number 5
    Resistor UB G1 me]asured by HP3458A with ID number 5
    Resistor UB G2 me]asured by HP3458A with ID number 5
    Resistor UB R4A me]asured by HP3458A with ID number 5
    Resistor UB R2B me]asured by HP3458A with ID number 5
    Resistor UB R4C me]asured by HP3458A with ID number 5
    Resistor coaxial zero me]asured by HP3458A with ID number 5
    Resistor Fluke 8508A-7000K Four-wire shorting PCB 410590-A me]asured by HP3458A with ID number 5
    Resistor SR104 StdR (SN:109006)  me]asured    by    HP3458A    with ID number 5
    Resistor SR04TS(temperature Sensor) me]asured by HP3458A with ID number 5
    Resistor SR1010--100k Parallel with PC 101 (SN:937003) me]asured    by    HP3458A    with ID number 5
    Resistor SR1010--100k Series Parallel with PC 102( as above SN:937003) me]asured    by    HP3458A    with ID number 5
    Resistor SR1010--100k R10 only (SN:937003) me]asured    by    HP3458A    with ID number 5
    Resistor SR1010--100k R1-R10 inSeries (SN:937003) me]asured    by    HP3458A    with ID number 5
    Resistor SR1010_1k parallel_R1-R10 with Pc 101 (SN:923001) me]asured    by    HP3458A    with ID number 5
    Resistor SR1010_1k series parallel_R1-R9 with PC 102(SN:923001) me]asured    by    HP3458A    with ID number 5
    Resistor SR1010_1k R10 only (SN:923001) me]asured    by    HP3458A    with ID number 5
    Resistor SR1010_1k series R1-R10(SN:923001) me]asured    by    HP3458A    with ID number 5
    Resistor UB BNC BPO coax zero me]asured by HP3458A with ID number 5
    Resistor Vishay 100 (RHK02) me]asured by HP3458A with ID number 5
    Resistor Vishay 10k (UBCAL10k)  me]asured by HP3458A with ID number 5
    Resistor Vishay 100 (RHK02)-right me]asured by HP3458A with ID number 5
    Resistor 1e4 me]asured by HP3458A with ID number 5
    Resistor Vishay 10k (UBCAL10k)-right me]asured by HP3458A with ID number 5
    Resistor Vishay 10k (UBCAL10k) me]asured by HP3458A with ID number 5
    Resistor Vishay 100k  me]asured by HP3458A with ID number 5
    Resistor UB G1 me]asured by HP3458A with ID number 5
    Resistor UB G2 me]asured by HP3458A with ID number 5
    Resistor UB R4A me]asured by HP3458A with ID number 5
    Resistor UB R2B me]asured by HP3458A with ID number 5
    Resistor UB R4C me]asured by HP3458A with ID number 5
    Resistor coaxial zero me]asured by HP3458A with ID number 5
    """
