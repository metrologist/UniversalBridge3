"""
Deals with the calibration of Muirhead tapped decade inductors.
A single frequency measurement.
"""
from GTC import ureal
from ubridge3 import UNIVERSALBRIDGE
from calculate_imp import UUT

calfile = r'data_csv\ub_dict_cal_23_24.csv'  # change to latest relevant version
room_temperature = ureal(20, 0.5, 10, 'temperature')  # this should be the ambient temperature given in conditions
# create the bridge object
my_ubridge = UNIVERSALBRIDGE(calfile, room_temperature)  # consider relevance of chosen temperature, 20.0 is usual

block_descriptor = [9, 30, 1, 15]  # this simply has to correctly match the spreadsheet.[9, 35, 1, 15]
z_set = UUT(my_ubridge, r'spread_sheets\InductorSet 2024 twist actual freq.xlsx', 'pyUBreadings', block_descriptor, 'indResults_TW.xlsx', 'pyUBresults')
# note that a different temperature could be used for the UUT
z_answers, z_zeros = z_set.calculate_values(room_temperature, my_ubridge)
# for twisted wire connection to inductors there are no coax zeros
z_zero_corrected = z_set.subtract_twist_zeros(z_answers)
cmc_list = z_set.cmc_check(my_ubridge)
z_set.create_output(z_zero_corrected, cmc_list)
