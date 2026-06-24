import numpy as np
from scipy.special import ber, bei, berp, beip  # Kelvin functions and their derivatives


# Function to calculate AC resistance
def ac_resistance(R0, r, delta):
    """
    Calculate AC resistance using the exact formula with Kelvin functions.

    Parameters:
        R0 (float): DC resistance of the wire.
        r (float): Radius of the wire.
        delta (float): Skin depth.

    Returns:
        float: AC resistance.
    """
    x = r / delta  # Ratio of radius to skin depth

    # Compute Kelvin functions and their derivatives
    ber_x = ber(x)
    bei_x = bei(x)
    ber_prime_x = berp(x)
    bei_prime_x = beip(x)

    # Compute the AC resistance
    numerator = ber_x * bei_prime_x - bei_x * ber_prime_x
    denominator = ber_prime_x ** 2 + bei_prime_x ** 2
    Rac = R0 * (x / 2) * (numerator / denominator)

    return Rac

# Example usage
if __name__ == "__main__":
    # Parameters
    R0 = 600 #5.34e-3  # DC resistance in ohms
    r = 0.000190492/2 * 10 # 1e-3  # Radius of the wire in meters
    delta = 0.00164535 # 1e-3  # Skin depth in meters

    # Calculate AC resistance
    Rac = ac_resistance(R0, r, delta)
    print(f"AC Resistance: {Rac:.6f} ohms")