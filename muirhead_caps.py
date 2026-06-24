from GTC import ureal
import ubridge3 as ub
from calculate_imp import UUT

calfile = r'data_csv/ubdict_2325_1006.csv'
room_temperature = ureal(20, 0.5, 10,
                         'temperature')  # this should be the ambient temperature given in conditions
# create the bridge object
ubridge = ub.UNIVERSALBRIDGE(calfile,
                             room_temperature)  # temperature put here as it might be in common with the UUT
block_descriptor = [9, 24, 1, 15]  # this simply has to correctly match the spreadsheet.[9, 35, 1, 15]
cap_set = UUT(ubridge, r'spread_sheets/KJ_S22175.xlsx', 'pyUBreadings', block_descriptor, 'muir_capResults.xlsx', 'pyUBresults')
# cap_set = UUT(ubridge, r'spread_sheets/S22012.xlsx', 'pyUBreadings', block_descriptor, 'muir_capResults.xlsx', 'pyUBresults')
# note that a different temperature could be used for the UUT
cap_answers, cap_zeros = cap_set.calculate_values(room_temperature, ubridge)
# print('original basic value =', cap_answers)
cap_zero_corrected = cap_set.subtract_coax_zeros(cap_answers, cap_zeros)
# print('zero corrected =', cap_zero_corrected)  # only the values, no descriptive labels
cap_jig_corrected = cap_set.muirhead_zeros(cap_zero_corrected)  # removes the jig zero
for x in cap_jig_corrected:
    print(x[1] * 1e6)
tan_delta = cap_set.tandelta(cap_jig_corrected)
for x in tan_delta:
    print(x)

print(cap_set.datdict)

cmc_list = cap_set.cmc_check(ubridge)
cap_set.create_output(cap_zero_corrected, cmc_list)

a = cap_jig_corrected
# a = cap_set.muirhead_zeros(cap_zero_corrected)
print('a =', a)
for i in range(len(a)):
    print(a[i])

b = tan_delta
# b = cap_set.muirhead_tand(a)
for i in range(len(b)):
    print(repr(b[i]))
cap_set.muirhead_output(a, b)  # creates capResults.xlsx with tan delta done in GTC