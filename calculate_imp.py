"""
calculate_imp.py calculates immittances of components measured with the Universal Impedance Bridge
"""
import ubridge3 as ub
# import GTC as gtc
from GTC import ureal
from GTC.function import mul2
from GTC.reporting import k_factor, budget
from math import pi, isnan
import excel3


class UUT(object):
    """
    A set of immittances that will be calibrated using the Universal Bridge. Bridge readings, environmental conditions
    and sensitivity coefficients are gathered in a spreadsheet. Calculated calibration results will be returned also in
    a spreadsheet for preparing a full report.
    """

    def __init__(self, bridge, input_workbook, target_in_sheet, block_descriptor, output_workbook, target_out_sheet):
        self.bridge = bridge
        self.input_workbook = input_workbook
        self.block_descriptor = block_descriptor  # this simply has to correctly match the spreadsheet.[9, 35, 1, 15]
        self.output_workbook = output_workbook
        self.target_in_sheet = target_in_sheet
        self.target_out_sheet = target_out_sheet
        self.data_block, self.datdict, self.excel_obj = self.get_measurement_data()

    def get_measurement_data(self):
        #  get component measurement data from a spread sheet
        this_uut = excel3.CALCULATOR(self.input_workbook, self.output_workbook)
        my_copy_data = this_uut.getdata_block(self.target_in_sheet, self.block_descriptor)
        thisdict = []  # need a list of dictionaries
        for x in my_copy_data:
            #  put each 'column' value into a dictionary for clarity
            thisdict.append(
                {'item': x[0], 'nom_freq': x[1], 'ubrange': x[2], 'xdial': x[3], 'rdial': x[4], 'frequency': x[5],
                 'temperature': x[6], 'tempu': x[7], 'tempdf': x[8], 'uuttempcox': x[9], 'uuttempcoxu': x[10],
                 'uuttempcoxdf': x[11], 'uuttempcor': x[12], 'uuttempcoru': x[13], 'uuttempcordf': x[14]})
        return my_copy_data, thisdict, this_uut

    def calculate_values(self, room_temperature, this_ubridge):
        y = []
        yzero = []
        for x in self.datdict:
            this_label = x['item'] + str(x['nom_freq']) + x['ubrange']  # str so e.g. 1k and 1000 both are strings
            answer = this_ubridge.bridge_value(x['ubrange'], x['rdial'], x['xdial'], x['frequency'], 1,
                                               new_label=this_label)
            #  next multiply the ubrdige values by factors relating to the uut
            if x['item'] != 'coax zero':  # no uncertainty in the coax zero uut
                uuttemp = ureal(x['temperature'], x['tempu'], x['tempdf'],
                                    'uuttemp' + x['item'])
                rtempco = ureal(x['uuttempcor'], x['uuttempcoru'], x['uuttempcordf'],
                                    'rtempco' + x['item'])
                r_value = answer.real * (1 + mul2(rtempco, uuttemp - room_temperature))
                xtempco = ureal(x['uuttempcox'], x['uuttempcoxu'], x['uuttempcoxdf'],
                                    'xtempco' + x['item'])
                x_value = answer.imag / (2 * pi * x['frequency']) * (
                        1 + mul2(xtempco, uuttemp - room_temperature))
            else:
                assert x['item'] == 'coax zero', "label not 'coax zero' when it should be"
                r_value = answer.real
                x_value = answer.imag / (2 * pi * x['frequency'])

            # create lists of the ubridge values
            y.append(
                (x['item'], x['ubrange'], str(x['nom_freq']), r_value,
                 x_value))  # all tuples of R-L or G-C, including coax zeros
            if x[
                'item'] == 'coax zero':  # a list of just the coax zeros is also created, duplicating the entry in the full list
                yzero.append((x['ubrange'], str(x['nom_freq']), r_value, x_value))
        return y, yzero

    def subtract_coax_zeros(self, all_items, zeros):
        y_corrected = []  # zero corrected values
        for x in all_items:  # all_items is full list of answers
            for zero in zeros:  # zeros is the list of coax zeros
                if zero[1] == x[2]:  # find a zero of the same nominal frequency
                    if zero[0] == x[1]:  # find if the zero is also the correct range
                        zero_corrected = (x[3] - zero[2], x[4] - zero[3])  # correct r and x values
                        if x[
                            0] == 'coax zero':  # check that the zeros cancel, just in case there is a duplicate coax zero
                            assert zero_corrected[0].x == 0, 'zero is not cancelling when subtracted from itself'
                            assert zero_corrected[1].x == 0, 'zero is not cancelling when subtracted from itself'
                        y_corrected.append(zero_corrected)
        # if no matching coax zero was found then y_corrected will be missing the item
        assert len(y_corrected) == len(all_items), "value missing a matching coax zero"
        return y_corrected

    def subtract_twist_zeros(self, all_items):
        z_corrected = []  # zero corrected values
        for i in range(len(all_items)):
            # print(all_items[i])
            if i<11:
                z_corrected.append((all_items[i][3] - all_items[0][3], all_items[i][4] - all_items[0][4]))
            else:
                z_corrected.append((all_items[i][3] - all_items[11][3], all_items[i][4] - all_items[11][4]))
        return(z_corrected)

    def cmc_check(self, this_ubridge):
        cmcs = []  # for the list of cmcs
        for x in self.datdict:
            cmc = this_ubridge.cmc_uncert(x['ubrange'], x['rdial'], x['xdial'], x['frequency'])
            cmcs.append(cmc)
        return cmcs

    def cmc_replace(self, cmcs, calculated):
        pass

    def create_output(self, y_corrected, cmcs):
        # now put all info in spreadsheet
        for i in range(len(y_corrected)):
            rpart = y_corrected[i][0]
            xpart = y_corrected[i][1]
            # first calculate coverage factors
            if isnan(rpart.df):  # avoiding the coax zeros with no uncertainty
                kr = 0
            else:
                kr = k_factor(rpart.df)
            if isnan(xpart.df):
                kx = 0
            else:
                kx = k_factor(xpart.df)
            # then expanded unertainties
            xU = xpart.u * kx
            rU = rpart.u * kr
            self.data_block[i].append(xpart.x)
            self.data_block[i].append(xU)  # expanded uncertainty
            self.data_block[i].append(kx)
            self.data_block[i].append(rpart.x)
            self.data_block[i].append(rU)  # expanded uncertainty
            self.data_block[i].append(kr)
            # then compare with CMCs
            # first decide on which r CMC to use
            # note this test only applies to Z ranges
            check_mode = self.data_block[i][2][1]
            if check_mode == 'Z':
                self.data_block[i].append(cmcs[i][2])  # for now, add the CMCs in a column to test in excel
                self.data_block[i].append(cmcs[i][1])
            elif check_mode == 'Y':
                self.data_block[i].append(cmcs[i][1])  # for now, add the CMCs in a column to test in excel
                self.data_block[i].append(cmcs[i][0])
            else:
                print('oops, range is neither Y nor Z !!!')  # this should be detected much earlier               
            # put the block, with final answers added, into the output spreadsheet
        self.excel_obj.makeworkbook(self.data_block, self.target_out_sheet)
        return

    def inspect_budget(self, line_no, results):
        # Can also look at the budget for individual lines
        print('Budget for', self.data_block[line_no][0], self.data_block[line_no][1])
        item = results[line_no]
        print(repr(item[0]))
        for l, u in budget(item[0], trim=0):
            print(l, '\t\t\t', u)
        print()
        print(repr(item[1]))
        for l, u in budget(item[1], trim=0):
            print(l, '\t\t\t', u)
        print()
        return


if __name__ == "__main__":
    calfile = r'ubdict_nov_2017.csv'
    room_temperature = ureal(20, 0.5, 10, 'temperature')  # this should be the ambient temperature given in conditions
    # create the bridge object
    my_ubridge = ub.UNIVERSALBRIDGE(calfile, room_temperature)  # consider relevanc of chosen temperature
    block_descriptor = [9, 30, 1, 15]  # this simply has to correctly match the spreadsheet.[9, 35, 1, 15]
    z_set = UUT(my_ubridge, 'InductorSet.xlsx', 'pyUBreadings', block_descriptor, 'indResults.xlsx', 'pyUBresults')
    # note that a different temperature could be used for the UUT
    z_answers, z_zeros = z_set.calculate_values(room_temperature, my_ubridge)
    # for twisted wire connection to inductors there are no coax zeros
    z_zero_corrected = z_set.subtract_twist_zeros(z_answers)
    cmc_list = z_set.cmc_check(my_ubridge)
    z_set.create_output(z_zero_corrected, cmc_list)

    """
    # Can also print the budget for individual lines
    #     cap_set.inspect_budget(4, cap_zero_corrected)
    cap_set.inspect_budget(12, cap_zero_corrected)

    print(' ')
    print('Some checks for the 16074A')
    induct_dial = 0
    res_dial = 0
    check_frequency = 53
    quick_check = my_ubridge.bridge_value('7Y', res_dial, induct_dial, check_frequency, 1)
    print(repr(quick_check))
    print(repr(quick_check.imag / (2 * pi * check_frequency)))
    check_cmc = my_ubridge.cmc_uncert('7Y', res_dial, induct_dial, check_frequency)
    print(repr(check_cmc))
    print('end of checks')
    print(' ')

    print('printing cap_answers')
    for i in range(len(cap_answers)):
        print(repr(cap_answers[i]))
    print()
    print("answer = my_ubridge.bridge_value('6Y', -187, 999731, 1.6e3, 1)")
    my_f = 1e3
    answer = my_ubridge.bridge_value('6Y', -187, 999731, my_f, 1)
    print(repr(answer.real))
    print(repr(answer.imag / (2 * pi * my_f)))
    for l, u in budget(answer, trim=0): print(l, u)
    print()
    """
