"""
Deals with the calibration of a 16074A set of impdedances, also including a pseudo inductor and open.
These are usually done at three frequencies.
"""
from GTC import ureal
from ubridge3 import UNIVERSALBRIDGE
from calculate_imp import UUT

calfile = r'ub_dict_nov_2020.csv'  # change to latest relevant version
room_temperature = ureal(20, 0.5, 10, 'temperature')  # this should be the ambient temperature given in conditions
# create the bridge object
my_ubridge = UNIVERSALBRIDGE(calfile, room_temperature)  # consider relevance of chosen temperature, 20.0 is usual
block_descriptor = [9, 63, 1, 15]  # this simply has to correctly match the spreadsheet.
# we could import a z_set and a y_set?
z_set = UUT(my_ubridge, 'rl.xlsx', 'pyUBreadings', block_descriptor, 'rl_Results.xlsx', 'pyUBresults')

print('\n','datadict')
for x in z_set.datdict:
    print(x)

# note that a different temperature could be used for the UUT
z_answers, z_zeros = z_set.calculate_values(room_temperature, my_ubridge)

print('\n', 'z_answers')
for x in z_answers:
    print(x)

print('\n', 'zeros')

for x in z_zeros:
    print(x)

z_zero_corrected = z_set.subtract_coax_zeros(z_answers, z_zeros)
cmc_list = z_set.cmc_check(my_ubridge)
z_set.create_output(z_zero_corrected, cmc_list)