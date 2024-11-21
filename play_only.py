from ubridge3 import UNIVERSALBRIDGE
import GTC as gtc

# dc values from UB_veri24_KJxlsx
v100k = 100003.2304
v10k = 10000.3152
e1kr10 = 999.9542
v100 = 100.014949

calfile = r'data_csv\ub_dict_cal_2023.csv'  # change to latest relevant version
room_temperature = gtc.ureal(20, 0.5, 10, 'temperature')  # this should be the ambient temperature given in conditions
# create the bridge object
my_ubridge = UNIVERSALBRIDGE(calfile, room_temperature)  # consider relevance of chosen temperature, 20.0 is usual

# 100 kohm
answer1 = my_ubridge.bridge_value( '6Z', 1.0000102*1e7, -0.000636*1e6, 1.6e3, 0)
print('ubridge YZ for range 6', 'v100k')
print(answer1.real)
answer2 = my_ubridge.bridge_value( '6Y', 0.9999727*1e7, 0.000642*1e6, 1.6e3, 0)
print(answer2.real)
result = answer1.real * answer2.real
print((result-1)*1e6, 'ppm')
acdc = (answer1.real / v100k - 1) * 1e6
print(acdc, 'ppm ac-dc error')
print()

# 10 kohm
answer1 = my_ubridge.bridge_value( '5Z', 0.999968*1e7, -0.000056*1e6, 1.6e3, 0)
print('ubridge YZ for range 5 result', 'v10k')
print(answer1.real)
answer2 = my_ubridge.bridge_value( '5Y', 1.000020*1e7, 0.000057*1e6, 1.6e3, 0)
print(answer2.real)
result = answer1.real * answer2.real
print((result-1)*1e6, 'ppm')
acdc = (answer1.real / v10k - 1) * 1e6
print(acdc, 'ppm ac-dc error')
print()

# 1 kohm
answer1 = my_ubridge.bridge_value( '4Z', 0.999878*1e7, 0.000202*1e6, 1.6e3, 0)
print('ubridge YZ for range 4 result', 'e1kr10')
print(answer1.real)
answer2 = my_ubridge.bridge_value( '4Y', 1.000103*1e7, -0.000199*1e6, 1.6e3, 0)
print(answer2.real)
result = answer1.real * answer2.real
print((result-1)*1e6, 'ppm')
acdc = (answer1.real / e1kr10 - 1) * 1e6
print(acdc, 'ppm ac-dc error')
print()

# 100 ohm
answer1 = my_ubridge.bridge_value( '3Z', 1.0000781*1e7, 0.000025*1e6, 1.6e3, 0)
print('ubridge YZ for range 3 result', 'v100')
print(answer1.real)
answer2 = my_ubridge.bridge_value( '3Y', 0.9999133*1e7, -0.000015*1e6, 1.6e3, 0)
print(answer2.real)
result = answer1.real * answer2.real
print((result-1)*1e6, 'ppm')
acdc = (answer1.real / v100 - 1) * 1e6
print(acdc, 'ppm ac-dc error')