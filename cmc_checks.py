# want to compare the various versions of the CMCs for the universal bridge
from ubridge3 import UNIVERSALBRIDGE
from GTC import ureal
from math import pi

# the UNIVERSALBRIDGE class has a method that should be the official MRA CMCs.
temperature = ureal(20, 0.5, 10, 'temperature')  # temperature at which bridge is being used
calfile = r'data_csv/ub_dict_nov_2020.csv'  # the file that contains practically all calibration and uncertainty information
# create the bridge object
ubridge = UNIVERSALBRIDGE(calfile, temperature)  # temperature put here as it might be in common with the UUT
# rdials = [0, 1000, 10000, 10000000]
# xdials = [0, 100, 1000, 1000000]
rdials = [0, 10000000]
xdials = [1000000]
check_range = '1Z'  # choose range to explore
frequency = 2.0e3  # choose frequency
# note that ubbridge.cmc returns a list of 2 for Y, but a list of 3 for Z
if check_range[1] == 'Y':
    for r in rdials:
        for x in xdials:
            result = ubridge.bridge_value(check_range, r, x, frequency, 1)
            print('result =', result)
            real_part = result.real
            reactive_part = result.imag / (2 * pi * frequency)
            cmc = ubridge.cmc_uncert(check_range, r, x, frequency)
            print('cmc =', cmc)
            # print(r, x, real_part, reactive_part, cmc )
            # create ureals with the cmc as the uncertainty
            cmc_real = ureal(real_part.x, cmc[0])
            cmc_imag = ureal(reactive_part.x, cmc[1])
            print(r, x, cmc[0] / real_part.u, cmc[1] / reactive_part.u)
            print(real_part, cmc_real, 'siemen')
            print(reactive_part, cmc_imag, 'farad')
            print('\n')

elif check_range[1] == 'Z':
    for r in rdials:
        for x in xdials:
            result = ubridge.bridge_value(check_range, r, x, frequency, 1)
            print('result =', result)
            real_part = result.real
            reactive_part = result.imag / (2 * pi * frequency)
            cmc = ubridge.cmc_uncert(check_range, r, x, frequency)
            print('cmc =', cmc)
            # print(r, x, real_part, reactive_part, cmc )
            # create ureals with the cmc as the uncertainty
            cmc_real = ureal(real_part.x, cmc[1])
            cmc_imag = ureal(reactive_part.x, cmc[2])
            print(r, x, cmc[0] / real_part.u, cmc[1] / real_part.u, cmc[2] / reactive_part.u)
            print(real_part, cmc_real, 'ohm')
            print(reactive_part, cmc_imag, 'henry')
            print('\n')

elif check_range[1] not in ['Y', 'Z']:
    print('range is neither Z nor Y !!! Check line 15.')





# for r in rdials:
#     for x in xdials:
#         result = ubridge.bridge_value(check_range, r, x, frequency, 1)
#         print('result =', result)
#         real_part = result.real
#         reactive_part = result.imag / (2 * pi * frequency)
#         cmc = ubridge.cmc_uncert(check_range, r, x, frequency)
#         print('cmc =', cmc)
#         # print(r, x, real_part, reactive_part, cmc )
#         # create ureals with the cmc as the uncertainty
#         cmc_real = ureal(real_part.x, cmc[1])
#         cmc_imag = ureal(reactive_part.x, cmc[2])
#         if check_range[1] == 'Y':
#             print(r, x, cmc[0] / real_part.u, cmc[1] / reactive_part.u)
#             print(real_part, cmc_real, 'siemen')
#             print(reactive_part, cmc_imag, 'farad')
#             print('\n')
#         else:
#             print(r, x, cmc[0] / real_part.u, cmc[1] / real_part.u, cmc[2] / reactive_part.u)
#             print(real_part, cmc_real, 'ohm')
#             print(reactive_part, cmc_imag, 'henry')
#             print('\n')