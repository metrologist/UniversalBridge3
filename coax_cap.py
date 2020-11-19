"""
Deals with the calibration of four terminal_pair 16380 set of capacitors. Expect some use of AH2700 measurements to be
processed in the spreadsheet.
"""
from GTC import ureal
from ubridge3 import UNIVERSALBRIDGE
from calculate_imp import UUT

calfile = r'ub_dict_nov_2020.csv'  # change to latest relevant version
room_temperature = ureal(20, 0.5, 10, 'temperature')  # this should be the ambient temperature given in conditions
# create the bridge object
my_ubridge = UNIVERSALBRIDGE(calfile, room_temperature)  # consider relevance of chosen temperature, 20.0 is usual
block_descriptor = [9, 24, 1, 15]  # this simply has to correctly match the spreadsheet.
cap_set = UUT(my_ubridge, 'CoaxCap.xlsx', 'pyUBreadings', block_descriptor, 'coaxCap_Results.xlsx', 'pyUBresults')
# note that a different temperature could be used for the UUT
cap_answers, cap_zeros = cap_set.calculate_values(room_temperature, my_ubridge)
cap_zero_corrected = cap_set.subtract_coax_zeros(cap_answers, cap_zeros)
b = cap_set.cap_tand(cap_zero_corrected)  # adds a GTC calculation of tan delta
cmc_list = cap_set.cmc_check(my_ubridge)
cap_set.create_output(b, cmc_list)