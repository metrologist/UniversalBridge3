"""
Deals with the calibration of resistors in the Arnold test set.
A single frequency measurement.
"""
from GTC import ureal
from ubridge3 import UNIVERSALBRIDGE
from calculate_imp import UUT

calfile = r'data_csv/ub_dict_cal_2023.csv'  # change to latest relevant version
room_temperature = ureal(20, 0.5, 10, 'temperature')  # this should be the ambient temperature given in conditions
# create the bridge object
my_ubridge = UNIVERSALBRIDGE(calfile, room_temperature)  # consider relevance of chosen temperature, 20.0 is usual

block_descriptor = [9, 16, 1, 15]  # this simply has to correctly match the spreadsheet.[9, 35, 1, 15]
z_set = UUT(my_ubridge, r'spread_sheets\S_arnold_support_2023.xlsx', 'pyUBreadings', block_descriptor, r'spread_sheets\arnold_results.xlsx', 'pyUBresults')
# note that a different temperature could be used for the UUT
z_answers, z_zeros = z_set.calculate_values(room_temperature, my_ubridge)
z_zero_corrected = z_set.subtract_coax_zeros(z_answers, z_zeros)
cmc_list = z_set.cmc_check(my_ubridge)
z_set.create_output(z_zero_corrected, cmc_list)