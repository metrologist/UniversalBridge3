"""
A scratch pad to play with equivalent circuits.
"""
from cmath import sqrt
# series and parallel equivalent circuits for a capacitor
# print('\n Measured parallel circuit values')
# w = 1e4  # angular frequency
# cp = 100e-12  # say 100 pF
# gp = 3e-10  # 0.3 nanosiemen
# print('parallel capacitnace =', cp)
# print('parallel conductance =', gp)
# print('tan delta =', gp/(w*cp))  # tan delta
# print('\n Calculated series circuit values')
# rp = 1 / gp
# rs = rp/(1 + (w * rp * cp)**2)
# print('series r =', rs)
# cs = (1 + (w * rp * cp)**2) / (w**2 * rp**2 * cp)
# print('series c =', cs)
# print('change in cap', (cs-cp) / cp * 100, '%')
#
# # check that series calculations are correct
# y1 = gp + 1j * w * cp
# y2 = 1/(rs - 1j / (w * cs))
# print('\n final check', y1, y2, y1 - y2)

# basic checks on calibration calculations using UBcalibration2014_for python.xlsx for values
G1 = 1e-5 * (1 + 12.9e-6)  # 100 kohm
C1 = 1e-9 * (1 + 143.1e-6)  # 1 nF
z2 = 1e5 * (1 - 7.5e-6)  # note that usually call this G2 as a conductance
w = 1e4  #angular frequency
# for Z mode range 5 row 57
alpha1 = 0.9999569
beta1 = -0.000055
za = 1 / (alpha1 * G1 + 1j * beta1 * w * C1)


#for Y mode range 5 row 57
alpha2 = 1.0000181
beta2 = 0.000054
zb = 1 / (alpha2 * G1 + 1j * beta2 * w * C1)

print(za)  # effective impedance connected to input of main amplifier
print(zb)  # effective impedance connected to input of main amplifier
print((sqrt(za * zb) / 1e5 - 1) * 1e6)  # just the YZ dial product ppm

f_p = sqrt(za * zb) / z2  # ratio of the RHS to LHS ratio factors ppm
print((f_p / 1 - 1) * 1e6)  # ppm

