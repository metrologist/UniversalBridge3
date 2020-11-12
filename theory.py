"""
A scratch pad to play with equivalent circuits.
"""
# series and parallel equivalent circuits for a capacitor
print('\n Measured parallel circuit values')
w = 1e4  # angular frequency
cp = 100e-12  # say 100 pF
gp = 3e-10  # 0.3 nanosiemen
print('parallel capacitnace =', cp)
print('parallel conductance =', gp)
print('tan delta =', gp/(w*cp))  # tan delta
print('\n Calculated series circuit values')
rp = 1 / gp
rs = rp/(1 + (w * rp * cp)**2)
print('series r =', rs)
cs = (1 + (w * rp * cp)**2) / (w**2 * rp**2 * cp)
print('series c =', cs)
print('change in cap', (cs-cp) / cp * 100, '%')

# check that series calculations are correct
y1 = gp + 1j * w * cp
y2 = 1/(rs - 1j / (w * cs))
print('\n final check', y1, y2, y1 - y2)