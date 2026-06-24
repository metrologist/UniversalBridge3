# simple tests as described in 'Equations Revisited'
from cmath import sqrt
from ratios import RATIOS

# left hand side of bridge
g1 = 1 / 99.99815e3  # siemen
c1 = 1000e-12 * (1 + 150e-6) # approx farad
z2 = 99.99869e3  # ohm
f = 1.59222e3  # Hz
r4b = 99.99949e3 +1j * 1e4 * 600e-6  # not measured for this 15 April run

print('15 April run')
ratio = RATIOS(g1, c1, z2, r4b)

# za in Z mode
alpha_a = 0.9999930
beta_a = 0.000365 - 0.001

# zb in Y mode
alpha_b = 0.9999927
beta_b = 0.000625

# za in Z mode with zero corrections
alpha_a = alpha_a - (-0.0000076 - 0.00001)
beta_a = beta_a - (- 0.000001)

# zb in Y mode with zero corrections
alpha_b = alpha_b - (0.0000031)
beta_b = beta_b -0.000000

factor3, za, zb = ratio.a_b_test(alpha_a, beta_a, alpha_b, beta_b, f)
print('factor3 with zero corrections', factor3, 'ppm' )

print('\n20 April run')  # ***********************************
# left hand side of bridge
g1 = 1 / 99.99818e3  # siemen
c1 = 1000e-12 * (1 + 150e-6) # approx farad
z2 = 99.99876e3  # ohm
f = 1.59277e3  # Hz

ratio = RATIOS(g1, c1, z2, r4b)  # class implementation of simple bridge circuit

# za in Z mode, first set of readings on the day
alpha_a = 0.9999980
beta_a = 0.000366 - 0.001

# zb in Y mode
alpha_b = 0.9999882
beta_b = 0.000625

# za in Z mode with zero corrections
alpha_a = alpha_a - (0.0000080 - 0.00001)
beta_a = beta_a - (- 0.000001)

# zb in Y mode with zero corrections
alpha_b = alpha_b - (0.0000023)
beta_b = beta_b -0.000000

factor3 ,za ,zb = ratio.a_b_test(alpha_a, beta_a, alpha_b, beta_b, f)
print('factor3 with zero corrections', factor3, 'ppm' )

# Change frequency
# left hand side of bridge
print('\n20 April run at 160 Hz')  # ***********************************
f = 160.501  # Hz

# za in Z mode, first set of readings on the day
alpha_a = 1.0000139
beta_a = 0.000325 - 0.001

# zb in Y mode
alpha_b = 0.9999783
beta_b = 0.000628

# za in Z mode with zero corrections
alpha_a = alpha_a - (0.0000080 - 0.00001)
beta_a = beta_a - 0.000006

# zb in Y mode with zero corrections
alpha_b = alpha_b - (0.0000035)
beta_b = beta_b -0.000004

factor3, za, zb = ratio.a_b_test(alpha_a, beta_a, alpha_b, beta_b, f)
print('factor3 with zero corrections', factor3, 'ppm' )

print('\n23 April run at 1.6 kHz for a 100 k rotation measurement')  # ***********************************
# note that this requires two versions of the bridge as r4 gets swapped out.
# left hand side of bridge with usual r4b
g1 = 1 / 99.99822e3  # siemen
c1 = 1000e-12 * (1 + 150e-6) # approx farad
z2 = 99.99876e3  # ohm
v_100k = 100.00264e3
r4b = 99.99949e3

ratio1 = RATIOS(g1, c1, z2, r4b)
ratio2 = RATIOS(g1, c1, z2, v_100k)

f = 1.59197e3  # Hz

# za in Z mode
alpha_a = 1.0000001
beta_a = 0.000365 - 0.001

# zb in Y mode
alpha_b = 0.9999864
beta_b = 0.000625

# za in Z mode with zero corrections
alpha_a = alpha_a - (0.0000089 - 0.00001)
beta_a = beta_a - (-0.000001)

# zb in Y mode with zero corrections
alpha_b = alpha_b - (0.0000032)
beta_b = beta_b -0.000000

factor3, za1, zb1 = ratio1.a_b_test(alpha_a, beta_a, alpha_b, beta_b, f)
print('factor3 with zero corrections', factor3, 'ppm' )
factor = 1 + factor3 / 1e6

z_uut_z = ratio1.uut_imp(za1, 'Z')
print('zuut_z =', z_uut_z, 'ohm')

z_uut_y = ratio1.uut_imp(zb1, 'Y')
print('zuut_y =', z_uut_y, 'ohm')
print((z_uut_z/z_uut_y - 1) * 1e6, 'ppm')

print('\n23 April run at 1.6 kHz with v-100k swapped with r4b')  # ****************************************
# zc in Z mode
alpha_a = 1.0000622 - 0.0001
beta_a = 0.000647

# zd in Y mode
alpha_b = 1.0000247
beta_b = 0.000342 - 0.001

# zc in Z mode with zero corrections
alpha_a = alpha_a - (0.0000001 - 0.000001)
beta_a = beta_a - (-0.000001)

# zd in Y mode with zero corrections
alpha_b = alpha_b - 0.000030
beta_b = beta_b - 0.000000

factor3, zc1, zd1 = ratio2.a_b_test(alpha_a, beta_a, alpha_b, beta_b, f)
print('factor3 with zero corrections', factor3, 'ppm' )

z_uut_z = ratio2.uut_imp(zc1, 'Z')
print('zuut_z =', z_uut_z, 'ohm', 'r4b', r4b, 'ohm')

z_uut_y = ratio2.uut_imp(zd1, 'Y')
print('zuut_y =', z_uut_y, 'ohm')
print((z_uut_z/z_uut_y - 1) * 1e6, 'ppm')

fz = sqrt(za1 * zc1) / z2
fy = sqrt(zb1 * zd1) / z2
ff = sqrt(fz * fy)
print((fz-1) * 1e6, 'Fz')
print((fy-1) * 1e6, 'Fy')
print((ff-1) * 1e6, 'Ff')

# repeat on 28 April 2026
g1 = 1 / 99.99821e3  # siemen
c1 = 1000e-12 * (1 + 150e-6) # approx farad
z2 = 99.99879e3  # ohm
v_100k = 100.00253e3 - 1j* 1e4 *5.77e-3
r4b = 99.99949e3 +1j * 1e4 * 600e-6  # add LCR inductance

ratio3 = RATIOS(g1, c1, z2, r4b)  # bridge with its internal reference resistors
ratio4 = RATIOS(g1, c1, z2, v_100k)  # bridge with r4b replaced by v_100k

f = 1.59163e3  # Hz

# za in Z mode, zero corrected
alpha_a = 1.0000003 - 0.000001 -(0.0000089 - 0.00001)
beta_a = 0.000366 - 0.001
print((alpha_a - 1) * 1e6, beta_a * 1e6)

# zb in Y mode, zero corrected
alpha_b = 1.0000861 -0.0001 - 0.0000024
beta_b = 0.000624 - (0.000343 -0.001)
print((alpha_b - 1) * 1e6, beta_b * 1e6)

factor5, za1, zb1 = ratio3.a_b_test(alpha_a, beta_a, alpha_b, beta_b, f)
print('factor5 with zero corrections', factor5, 'ppm' )
factor5 = 1 + factor5 / 1e6

z_uut_z = ratio3.uut_imp(za1, 'Z')
print('zuut_z =', z_uut_z, 'ohm')

z_uut_y = ratio3.uut_imp(zb1, 'Y')
print('zuut_y =', z_uut_y, 'ohm')

print((z_uut_z/z_uut_y - 1) * 1e6, 'ppm')

print('\n 28 April')
# za in Z mode, zero corrected
alpha_a = 1.0000003 - 0.000001 -(0.0000089 - 0.00001)
beta_a = 0.000366 - 0.001 -(0.000009- 0.00001)
print((alpha_a - 1) * 1e6, beta_a * 1e6)

# zb in Y mode, zero corrected
alpha_b = 1.0000861 -0.0001 - 0.0000024
beta_b = 0.000624 - 0.000000
print((alpha_b - 1) * 1e6, beta_b * 1e6)

factor5, za1, zb1 = ratio3.a_b_test(alpha_a, beta_a, alpha_b, beta_b, f)
print('factor5 with zero corrections', factor5, 'ppm' )
factor5 = 1 + factor5 / 1e6

z_uut_z = ratio3.uut_imp(za1, 'Z')
print('z_uut_z =', z_uut_z, 'ohm', (z_uut_z/1e5 - 1) *1e6, 'ppm')

z_uut_y = ratio3.uut_imp(zb1, 'Y')
print('z_uut_y =', z_uut_y, 'ohm', (z_uut_y/1e5 - 1) *1e6, 'ppm')

print((z_uut_z/z_uut_y - 1) * 1e6, 'ppm')

print('\n now with v-100k internal to UB')
# za in  mode, zero corrected
alpha_a = 1.0000616 - 0.0001 -(0.0000089 - 0.00001)
beta_a = 0.000647 - (0.000009- 0.00001)
print((alpha_a - 1) * 1e6, beta_a * 1e6)

# zb in Y mode, zero corrected
alpha_b = 1.0000236 - 0.0000024
beta_b = 0.000343 - 0.001 - 0.000000
print((alpha_b - 1) * 1e6, beta_b * 1e6)

factor6, za1, zb1 = ratio4.a_b_test(alpha_a, beta_a, alpha_b, beta_b, f)
print('factor5 with zero corrections', factor5, 'ppm' )
factor6 = 1 + factor6 / 1e6

z_uut_z = ratio4.uut_imp(za1, 'Z')
print('z_uut_z =', z_uut_z, 'ohm', (z_uut_z/1e5 - 1) *1e6, 'ppm')

z_uut_y = ratio4.uut_imp(zb1, 'Y')
print('z_uut_y =', z_uut_y, 'ohm', (z_uut_y/1e5 - 1) *1e6, 'ppm')

print((z_uut_z/z_uut_y - 1) * 1e6, 'ppm')

# *************************************************************
# repeat on 28 May 2026
print('\n repeat on 28 May 2026')
g1 = 1 / 99.99826e3  # siemen
c1 = 1000e-12 * (1 + 150e-6) # approx farad
z2 = 99.99881e3  # ohm
v_100k = 100.00265e3 - 1j* 1e4 *5.77e-3
r4b = 99.99950e3 +1j * 1e4 * 600e-6  # add LCR inductance

ratio5 = RATIOS(g1, c1, z2, r4b)  # bridge with its internal reference resistors
ratio6 = RATIOS(g1, c1, z2, v_100k)  # bridge with r4b replaced by v_100k

f = 1.59221e3  # Hz

# za in Z mode, zero corrected
alpha_a = 1.0000026 -(0.0000077 - 0.00001)
beta_a = 0.000366 - 0.001 - (0.000007 - 0.00001)
print((alpha_a - 1) * 1e6, beta_a * 1e6)

# zb in Y mode, zero corrected
alpha_b = 1.0000826 -0.0001 - 0.0000021
beta_b = 0.000624 - 0
print((alpha_b - 1) * 1e6, beta_b * 1e6)

factor6, za1, zb1 = ratio5.a_b_test(alpha_a, beta_a, alpha_b, beta_b, f)
print('factor6 with zero corrections', factor6, 'ppm' )
factor6 = 1 + factor6 / 1e6

z_uut_z = ratio5.uut_imp(za1, 'Z')
print('zuut_z =', z_uut_z, 'ohm')

z_uut_y = ratio5.uut_imp(zb1, 'Y')
print('zuut_y =', z_uut_y, 'ohm')

print((z_uut_z/z_uut_y - 1) * 1e6, 'ppm')

print('\n 28 May now with R4B swapped')

# za in  Z mode, zero corrected
alpha_a = 1.0000654 - 0.0001 -(0.0000077 - 0.00001)
beta_a = 0.000647 - (0.000007 - 0.00001)
print((alpha_a - 1) * 1e6, beta_a * 1e6)

# zb in Y mode, zero corrected
alpha_b = 1.0000205 - 0.00001 - 0.0000021
beta_b = 0.000344 - 0.001 - 0.000000
print((alpha_b - 1) * 1e6, beta_b * 1e6)

factor7, za1, zb1 = ratio6.a_b_test(alpha_a, beta_a, alpha_b, beta_b, f)
print('factor7 with zero corrections', factor7, 'ppm' )
factor7 = 1 + factor7 / 1e6

z_uut_z = ratio6.uut_imp(za1, 'Z')
print('z_uut_z =', z_uut_z, 'ohm', (z_uut_z/1e5 - 1) *1e6, 'ppm')

z_uut_y = ratio6.uut_imp(zb1, 'Y')
print('z_uut_y =', z_uut_y, 'ohm', (z_uut_y/1e5 - 1) *1e6, 'ppm')

print((z_uut_z/z_uut_y - 1) * 1e6, 'ppm')

print('\n Thompson check')
alpha_a = 0.9997602 -(0.0000077 - 0.00001)
beta_a = -0.000029 - (0.000007 - 0.00001)
z_d = ratio5.z_dial(alpha_a, beta_a, f)
z_uut_z = ratio5.uut_imp(z_d, 'Z')
print('Thomson @15:51 =', z_uut_z)

print('\n Thompson check')
alpha_a = 0.9997637 -(0.0000077 - 0.00001)
beta_a = -0.000029 - (0.000007 - 0.00001)
z_d = ratio5.z_dial(alpha_a, beta_a, f)
z_uut_z = ratio5.uut_imp(z_d, 'Z')
print('Thomson @14:55 =', z_uut_z)
