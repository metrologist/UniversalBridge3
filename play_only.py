from ubridge3 import UNIVERSALBRIDGE

import GTC as gtc
# x = gtc.ureal(0.0,0.1,5)
# y = gtc.ureal(0.0,0.2,10)
# a =  x*y
# print(a.u)
# b = gtc.function.mul2(x, y)
# print(b)
#
# ab =gtc.result(a*b, label='result')
# print(ab.label,ab)

calfile = r'data_csv\ub_dict_cal_2023.csv'  # change to latest relevant version
room_temperature = gtc.ureal(20, 0.5, 10, 'temperature')  # this should be the ambient temperature given in conditions
# create the bridge object
my_ubridge = UNIVERSALBRIDGE(calfile, room_temperature)  # consider relevance of chosen temperature, 20.0 is usual
answer1 = my_ubridge.bridge_value( '6Z', 1.0000102*1e7, -0.000636*1e6, 1.6e3, 0)
print('ubridge YZ for range 6')
print(answer1.real)
answer2 = my_ubridge.bridge_value( '6Y', 0.9999727*1e7, 0.000642*1e6, 1.6e3, 0)
print(answer2.real)
result = answer1.real * answer2.real
print((result-1)*1e6, 'ppm')

answer1 = my_ubridge.bridge_value( '5Z', 0.999968*1e7, -0.000056*1e6, 1.6e3, 0)
print('ubridge YZ for range 5 result')
print(answer1.real)
answer2 = my_ubridge.bridge_value( '5Y', 1.000020*1e7, 0.000057*1e6, 1.6e3, 0)
print(answer2.real)
result = answer1.real * answer2.real
print((result-1)*1e6, 'ppm')
