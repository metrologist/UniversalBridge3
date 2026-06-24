# simple tests as described in 'Equations Revisited'
from math import pi
from cmath import sqrt

class RATIOS(object):
    def __init__(self, gg1, cc1, z2, r4):
        """

        :param gg1: conductance of G1 (inverse resistance, siemen)
        :param cc1: capacitance in pF of C1
        :param z2: impedance of Z2 (resistance, ohm)
        :param r4: impedance of r4 (depends on range)
        """
        self.g1 = gg1
        self.c1 = cc1
        self.z2 = z2
        self.r4 = r4

    def z_dial(self, alpha, beta, f):
        """

        returns the effective impedance created by the dial settings, equation (1)
        :param alpha: resistive dial (7 digits)
        :param beta: reactive dial (6 digits)
        :param f: frequency in Hz
        :return: effective impedance created by the dial settings
        """
        z = 1 / (alpha * self.g1 + 1j * 2 * pi * f * beta * self.c1)
        return z

    def ratio_factors(self, z_first, z_second):
        """

        :param z_first: za
        :param z_second: zb
        :return: ratio of F over P in ppm, equation (5) or FZ/P (8) or FY/P (10)
        """
        f_over_p = sqrt(z_first * z_second) / self.z2
        ppm = (f_over_p - 1) * 1e6
        return ppm

    def a_b_test(self, alph_a, bet_a, alph_b, bet_b, f, **kwargs):
        """

        equation (5), with a cross-check that the calculated fp is correct
        :param alph_a: dial for Z mode
        :param bet_a: dial for Z mode
        :param alph_b: dial for Y mode
        :param bet_b: dial for Y mode
        :param f: frequency in Hz
        :param kwargs: 'fp' is the correction factor, defaults to 1.0
        :return: f_p correction factor, and za and zb for follow on calculations
        """
        fp = 1.0  # default not using a ratio correction factor
        for k, val in kwargs.items():
            if k == 'fp':
                fp = val
        za = self.z_dial(alph_a, bet_a, f) / fp
        zb = self.z_dial(alph_b, bet_b, f) / fp
        f_p = self.ratio_factors(za, zb)  # in ppm
        return f_p, za, zb

    def uut_imp(self, dialz, mode):
        """
        returns impedance of UUT whether in Y or Z mode
        :param dialz: as calculated by z_dial
        :param r4: the impedance of r4 (a, b, or c depending on range)
        :param mode: either 'Y' or 'Z'
        :return: impedance of uut
        """
        if mode == 'Z':
            uut = (self.z2 / dialz) * self.r4  # equation (2) with F=P=1
        elif mode == 'Y':
            uut = (dialz / self.z2) * self.r4  # equation (3) with P=F=1
        else:
            uut = 'bridge mode not given'
        return uut