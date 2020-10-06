"""
Deals with measurements of a set of four terminal-pair inductors corrected with for the measured value of a
coaxial zero at each range.
"""
from GTC import ureal
from ubridge3 import UNIVERSALBRIDGE
from calculate_imp import UUT

calfile = r'ubdict_dec_2019.csv'
room_temperature = ureal(20, 0.5, 10, 'temperature')  # this should be the ambient temperature given in conditions
# create the bridge object
my_ubridge = UNIVERSALBRIDGE(calfile, room_temperature)  # consider relevance of chosen temperature
block_descriptor = [9, 30, 1, 15]  # this simply has to correctly match the spreadsheet.
z_set = UUT(my_ubridge, 'sullivan_test.xlsx', 'pyUBreadings', block_descriptor, 'sullivan_Results.xlsx', 'pyUBresults')
# note that a different temperature could be used for the UUT
z_answers, z_zeros = z_set.calculate_values(room_temperature, my_ubridge)
# for twisted wire connection to inductors there are no coax zeros
z_zero_corrected = z_set.subtract_coax_zeros(z_answers, z_zeros)
cmc_list = z_set.cmc_check(my_ubridge)
z_set.create_output(z_zero_corrected, cmc_list)

# Can also print the budget for individual lines
#     cap_set.inspect_budget(4, cap_zero_corrected)
z_set.inspect_budget(8, z_zero_corrected)
