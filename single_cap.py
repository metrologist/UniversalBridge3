"""
Deals with the calibration of a single capacitor with a zero. The zero is labelled coax zero, but this could be a
lead zero if the capacitor is not defined coaxially. Note that this does not take series resistance as an uncertainty
contribution to tan delta. We would need to artificially add a box_zero and Cuzero and use.subtract_box_zeros  rather
than .subtract_coax_zeros in line 19.
"""
from GTC import ureal
from ubridge3 import UNIVERSALBRIDGE
from calculate_imp import UUT

calfile = r'ubdict_apr_2021.csv'  # change to latest relevant version
room_temperature = ureal(20, 0.5, 10, 'temperature')  # this should be the ambient temperature given in conditions
# create the bridge object
my_ubridge = UNIVERSALBRIDGE(calfile, room_temperature)  # consider relevance of chosen temperature, 20.0 is usual
block_descriptor = [9, 10, 1, 15]  # this simply has to correctly match the spreadsheet.
cap_set = UUT(my_ubridge, 'SingleCap.xlsx', 'pyUBreadings', block_descriptor, 'SingleCap_Results.xlsx', 'pyUBresults')
# note that a different temperature could be used for the UUT
cap_answers, cap_zeros = cap_set.calculate_values(room_temperature, my_ubridge)
cap_zero_corrected = cap_set.subtract_coax_zeros(cap_answers, cap_zeros)
b = cap_set.cap_tand(cap_zero_corrected)  # adds a GTC calculation of tan delta
cmc_list = cap_set.cmc_check(my_ubridge)
cap_set.create_output(b, cmc_list)