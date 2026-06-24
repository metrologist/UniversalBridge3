#Total distortion calculation. (Not related to impedance measurements!)
from GTC import ureal, sqrt

vharm = [13.50282,4.50092,2.700564,1.928924,1.500306,1.227522,1.038648,0.900153,0.794269,0.710665,0.642991,0.587080,
0.540122,0.500128,0.465627,0.435833,0.409031,0.385421,0.364657,0.345970]

# uharm = [0.00069,0.00016,0.00011,0.000097,0.000068,0.000059,0.000053,0.000042,0.000034,0.000031,0.000029,0.000027,
# 0.000025,0.000024,0.000026,0.000670,0.000450,0.000680,0.000860,0.000880]  # uncertainty of source

uharm = [0.006355,0.002475,0.002205,0.002089,0.002025,0.001984,0.001956,0.001935,0.001919,0.001907,0.003793,
0.003776,0.003762,0.00375,0.00374,0.003731,0.003723,0.003716,0.003709,0.003704]  # uncertainty of meter
harm = []  # list of ureals of the rms value of each harmonic voltage

for i in range(len(vharm)):
    harm.append(ureal(vharm[i], uharm[i],label=i))  # note expanded uncertainties being used

print('fundamental squared', repr(harm[0]**2))
sumsq = 0  # rms sum of harmonics without the fundamental
print(harm[0])  # this is the fundamental
for i in range(1, len(harm)):  # excluding the fundamental
    print(harm[i])
    sumsq += harm[i]**2
harmamp = sqrt(sumsq)  # this should incorporate all the uncertainties leading to the rms sum of the harmonics
print('square of harmonics',repr(sumsq))
print('amplitude of harmonics', repr(harmamp))

thd = harmamp / harm[0]  # sum of the harmonics divided by the fundamental
print('THD =', thd)
thd_percent = thd * 100
print('THD% =', thd_percent.x, '%')
print('absolute uncertainty in thd =', thd.u,'%')
print('relative % uncertainty in thd =', thd_percent.u / thd_percent.x * 100, '%')

# basic example not using anything from above
a = ureal(1,0.2)
b = ureal(1.5, 0.3)
c = sqrt(a**2 + b**2)
d = a**2 + b**2
print(repr(c))
print(repr(d))
print(repr(a**2))
print(repr(b**2))