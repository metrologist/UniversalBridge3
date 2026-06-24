# https://en.wikipedia.org/wiki/Proximity_effect_(electromagnetism)
# Dowell method for determination of losses
import cmath

rdc = 600  # ohm dc
m = 10/2  # number of layers
w = 1e4 * 1.05  # angular frequency
ro = 1.6e-8 # ohm m (copper conductivity)
mu0 = 4 * cmath.pi * 1e-7  # permeability
Nl = 10  # number of turns per layer
a = 1e-3  # m (width of square conductor)
b = 20e-3  #m (width of the winding window
h = 1e-3 # m (height of the square conductor

eta = Nl * a / b
alpha = cmath.sqrt((1j * w * mu0 * eta / ro))
D = 2 * alpha * h * cmath.tanh(alpha * h / 2)
M = alpha * h * cmath.cosh(alpha * h) / cmath.sinh(alpha * h)

rac = rdc * (M.real + (m**2 -1) * D.real/3)

print(rac)