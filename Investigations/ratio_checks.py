# simple tests as described in 'Equations Revisited'
from cmath import sqrt
from ratios import RATIOS

# left hand side of bridge
g1 = 1 / 99.99815e3  # siemen
c1 = 1000e-12 * (1 + 150e-6) # approx farad
z2 = 99.99869e3  # ohm
f = 1.59222e3  # Hz

print('15 April run')
ratio = RATIOS(g1, c1, z2)

# za in Z mode
alpha_a = 0.9999930
beta_a = 0.000365 - 0.001

# zb in Y mode
alpha_b = 0.9999927
beta_b = 0.000625

factor1, za, zb = ratio.a_b_test(alpha_a, beta_a, alpha_b, beta_b, f)
print('factor1 with no zero corrections', factor1, 'ppm' )
factor = 1 + factor1 / 1e6
factor2, za, zb = ratio.a_b_test(alpha_a, beta_a, alpha_b, beta_b, f, fp=factor)
print('factor2 check that factor1 corrects the ratio', factor2, 'ppm' )


# za in Z mode with zero corrections
alpha_a = alpha_a - (-0.0000076 - 0.00001)
beta_a = beta_a - (- 0.000001)

# zb in Y mode with zero corrections
alpha_b = alpha_b - (0.0000031)
beta_b = beta_b -0.000000

factor3, za, zb = ratio.a_b_test(alpha_a, beta_a, alpha_b, beta_b, f)
print('factor3 with zero corrections', factor3, 'ppm' )
factor = 1 + factor3 / 1e6
factor4, za, zb = ratio.a_b_test(alpha_a, beta_a, alpha_b, beta_b, f, fp=factor)
print('factor4 check that factor3 corrects the ratio', factor4, 'ppm' )

print('\n20 April run')  # ***********************************
# left hand side of bridge
g1 = 1 / 99.99818e3  # siemen
c1 = 1000e-12 * (1 + 150e-6) # approx farad
z2 = 99.99876e3  # ohm
f = 1.59277e3  # Hz

ratio = RATIOS(g1, c1, z2)  # class implementation of simple bridge circuit

# za in Z mode, first set of readings on the day
alpha_a = 0.9999980
beta_a = 0.000366 - 0.001

# zb in Y mode
alpha_b = 0.9999882
beta_b = 0.000625

factor1, za, zb = ratio.a_b_test(alpha_a, beta_a, alpha_b, beta_b, f)
print('factor1 with no zero corrections', factor1, 'ppm' )
factor = 1 + factor1 / 1e6
factor2, za, zb = ratio.a_b_test(alpha_a, beta_a, alpha_b, beta_b, f, fp=factor)
print('factor2 check that factor1 corrects the ratio', factor2, 'ppm' )


# za in Z mode with zero corrections
alpha_a = alpha_a - (0.0000080 - 0.00001)
beta_a = beta_a - (- 0.000001)

# zb in Y mode with zero corrections
alpha_b = alpha_b - (0.0000023)
beta_b = beta_b -0.000000

factor3 ,za ,zb = ratio.a_b_test(alpha_a, beta_a, alpha_b, beta_b, f)
print('factor3 with zero corrections', factor3, 'ppm' )
factor = 1 + factor3 / 1e6
factor4 = ratio.a_b_test(alpha_a, beta_a, alpha_b, beta_b, f, fp=factor)
print('factor4 check that factor3 corrects the ratio', factor4, 'ppm' )

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

factor1, za, zb = ratio.a_b_test(alpha_a, beta_a, alpha_b, beta_b, f)
print('factor1 with no zero corrections', factor1, 'ppm' )
factor = 1 + factor1 / 1e6
factor2, za ,zb = ratio.a_b_test(alpha_a, beta_a, alpha_b, beta_b, f, fp=factor)
print('factor2 check that factor1 corrects the ratio', factor2, 'ppm' )

# za in Z mode with zero corrections
alpha_a = alpha_a - (0.0000080 - 0.00001)
beta_a = beta_a - 0.000006

# zb in Y mode with zero corrections
alpha_b = alpha_b - (0.0000035)
beta_b = beta_b -0.000004

factor3, za, zb = ratio.a_b_test(alpha_a, beta_a, alpha_b, beta_b, f)
print('factor3 with zero corrections', factor3, 'ppm' )
factor = 1 + factor3 / 1e6
factor4, za, zb = ratio.a_b_test(alpha_a, beta_a, alpha_b, beta_b, f, fp=factor)
print('factor4 check that factor3 corrects the ratio', factor4, 'ppm' )

print('\n23 April run at 1.6 kHz for a 100 k rotation measurement')  # ***********************************
# note that this requires two versions of the bridge as r4 gets swapped out.
# left hand side of bridge with usual r4b
g1 = 1 / 99.99822e3  # siemen
c1 = 1000e-12 * (1 + 150e-6) # approx farad
z2 = 99.99876e3  # ohm
v_100k = 100.00264e3
r4b = 99.99949e3

ratio1 = RATIOS(g1, c1, z2)
ratio2 = RATIOS(g1, c1, v_100k)

f = 1.59197e3  # Hz

# za in Z mode
alpha_a = 1.0000001
beta_a = 0.000365 - 0.001

# zb in Y mode
alpha_b = 0.9999864
beta_b = 0.000625

factor1, za, zb = ratio1.a_b_test(alpha_a, beta_a, alpha_b, beta_b, f)
print('factor1 with no zero corrections', factor1, 'ppm' )
factor = 1 + factor1 / 1e6



factor2, za, zb = ratio1.a_b_test(alpha_a, beta_a, alpha_b, beta_b, f, fp=factor)
print('factor2 check that factor1 corrects the ratio', factor2, 'ppm' )



# za in Z mode with zero corrections
alpha_a = alpha_a - (0.0000089 - 0.00001)
beta_a = beta_a - (-0.000001)

# zb in Y mode with zero corrections
alpha_b = alpha_b - (0.0000032)
beta_b = beta_b -0.000000

factor3, za1, zb1 = ratio1.a_b_test(alpha_a, beta_a, alpha_b, beta_b, f)
print('factor3 with zero corrections', factor3, 'ppm' )
factor = 1 + factor3 / 1e6

z_uut_z = ratio1.uut_imp(za1, r4b, 'Z')
print('zuut_z =', z_uut_z, 'ohm')

z_uut_y = ratio1.uut_imp(zb1, r4b, 'Y')
print('zuut_y =', z_uut_y, 'ohm')
print((z_uut_z/z_uut_y - 1) * 1e6, 'ppm')

factor4, zc, zd = ratio1.a_b_test(alpha_a, beta_a, alpha_b, beta_b, f, fp=factor)
print('factor4 check that factor3 corrects the ratio', factor4, 'ppm' )

print('\n23 April run at 1.6 kHz with v-100k swapped with r4b')  # ****************************************
# zc in Z mode
alpha_a = 1.0000622 - 0.0001
beta_a = 0.000647

# zd in Y mode
alpha_b = 1.0000247
beta_b = 0.000342 - 0.001

factor1, zc, zd = ratio2.a_b_test(alpha_a, beta_a, alpha_b, beta_b, f)
print('factor1 with no zero corrections', factor1, 'ppm' )
factor = 1 + factor1 / 1e6
factor2, zc, zd = ratio2.a_b_test(alpha_a, beta_a, alpha_b, beta_b, f, fp=factor)
print('factor2 check that factor1 corrects the ratio', factor2, 'ppm' )

# zc in Z mode with zero corrections
alpha_a = alpha_a - (0.0000089 - 0.00001)
beta_a = beta_a - (-0.000001)

# zd in Y mode with zero corrections
alpha_b = alpha_b - (0.0000089 - 0.00001)
beta_b = beta_b - (-0.000001)

factor3, zc1, zd1 = ratio2.a_b_test(alpha_a, beta_a, alpha_b, beta_b, f)
print('factor3 with zero corrections', factor3, 'ppm' )
factor = 1 + factor3 / 1e6
factor4, zc, zd = ratio2.a_b_test(alpha_a, beta_a, alpha_b, beta_b, f, fp=factor)
print('factor4 check that factor3 corrects the ratio', factor4, 'ppm' )

z_uut_z = ratio2.uut_imp(zc1, r4b, 'Z')
print('zuut_z =', z_uut_z, 'ohm')

z_uut_y = ratio2.uut_imp(zd1, r4b, 'Y')
print('zuut_y =', z_uut_y, 'ohm')
print((z_uut_z/z_uut_y - 1) * 1e6, 'ppm')

fz = sqrt(za1 * zc1) / z2
fy = sqrt(zb1 * zd1) / z2
ff = sqrt(fz * fy)
print((fz-1) * 1e6, 'Fz')
print((fy-1) * 1e6, 'Fy')
print((ff-1) * 1e6, 'Ff')
