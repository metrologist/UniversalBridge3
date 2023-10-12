from GTC import ureal
from math import pi
from ubridge3 import UNIVERSALBRIDGE
from excel3 import CALCULATOR
from math import sqrt


class RESISTANCE(object):
    """
    Calibration of the universal bridge essentially relies on calibrating the value of the internal resistors at dc with
    the assumption of negligible ac-dc difference of the resistors. The Thompson resistors are of known phase angle and
    are used to estimate the phase defect in the bridge, in essence the correction required to UB measurements of
    resistor capacitance or inductance. An external set of resistors is also calibrated at dc and used to confirm the
    accuracy of all the ranges.
    Methods for using a Hamon resistance box with a resistance meter to establish the dc values of resistors are in this
    class together with some methods for gathering data from an Excel spreadsheet.
    Note that all resistance values are in ohm regardless of whether the standard is labelled G or R.
    """
    def __init__(self, calfile, datafile, outputfile):
        """

        :param calfile:  a csv file that has previous calibration constants for the ub
        :param datafile: excel workbook that contains the dmm and ub manual measurements
        :param outputfile: an excel workbook that will contain the calculated outputs
        """
        # note that UNIVERSALBRIDGE is being created for access to its range managing methods
        # the calibration file and temperature are required for the instantiation only ... could update this approach
        room_temperature = ureal(20, 0.5, 10,'temperature')  # this should be the ambient temperature given in conditions
        self.ub = UNIVERSALBRIDGE(calfile, room_temperature)
        self.input_data = CALCULATOR(datafile, outputfile)

    def dc_resistance_data(self, sheet, block):
        dc_data = {}
        data = self.input_data.getdata_block(sheet, block)
        for x in data:
            dc_data[x[0]] = ureal(x[1], x[2], x[3], label=x[0])  # each resistance value as a ureal
        return dc_data

    def thompson_data(self, sheet, block):
        t_data = {}
        data = self.input_data.getdata_block(sheet, block)
        for x in data:
            t_data[x[0]] = (x[1], x[2], x[3])  # each thompson reading as a tuple f(a, b, cap)
        return t_data

    def z_data(self, sheet, block):
        z_data = {}
        data = self.input_data.getdata_block(sheet, block)
        for x in data:
            z_data[x[0]] = (x[1], x[2])  # each zero value as a tuple
        return z_data

    def acr_data(self, sheet, block):
        acrdata = {}
        data = self.input_data.getdata_block(sheet, block)
        for x in data:
            acrdata[x[0]] = (x[1], x[2], x[3], x[4], x[5], x[6])  # each resistor reading as a tuple (Ya, Yb, Za, Zb, range, freq)
        return acrdata

    def ind_data(self, sheet, block):
        inddata = {}
        data = self.input_data.getdata_block(sheet, block)
        for x in data:
            inddata[x[0]] = (x[1], x[2], x[3], x[4], x[5], x[6])  # each inductor reading as a tuple (Za, Zb, zero a, zero b, range, freq)
        return inddata

    def cap_data(self, sheet, block):
        capddata = {}
        data = self.input_data.getdata_block(sheet, block)
        for x in data:
            capddata[x[0]] = (x[1], x[2], x[3], x[4], x[5], x[6])  # each capacitor reading as a tuple (Ya, Yb, zero a, zero b, range, freq)
        return capddata

    def meter_corrn(self, r1, r2):
        """

        :param r1: true value of resistor
        :param r2: meter reading for resistor
        :return: correction to meter reading in ohm
        """
        return r1 - r2


    def temp_sr104(self, sens):
        """
        uses the value of the sensor resistor to calculate the correction that needs to be applied to the 20 degree value
        of SR104
        :param sens: value of the sense resistor
        :return: correction in ohm
        """
        temp = sens * 9.99999228000003*0.01-977  # from SR104 lid values
        print('sr104 temperature', temp)
        return 10000*(0.342 * (temp - 20.0) - 0.027 * (temp - 20.0) ** 2) * 1e-6  # or 0.18 alpha and-0.027 beta

    def series_parallel(self, r1, r2, r3):
        """
        Gives the correction to the series parallel value with 9 resistor in term of the parallel value of all 10 resistors.
        Formula taken from the SR1010 handbook, page 2-13, d9av - d10av =0.1(d9av - d10). See page 24 of MSLT.E.023.07
        :param r1: the true value of the resistance box in parallel (all 10)
        :param r2: the measured value of the resistance box in series-parallel with 9 resistors
        :param r3: the measured value of the 10th resistor not used in s-p, measured with the same meter as r2
        :return:
        """
        return 10 * r1 + 0.1 * (r2 - r3)

    def phase_error(self, z, y, z_zero, y_zero, freq, rnge):
        """
        uses the known parallel capacitance of a Thompson phase angle standard
        and L = -C * R ** 2 /(1 + (w *  C * R) ** 2) give the expected inductance from the known capacitance

        :param z: the a, b readings in z mode and the known capacitance in pF
        :param y: the a, b readings in y mode and the known capacitance in pF
        :param z_zero: z_zero: the a, b readings for a zero in z mode
        :param y_zero: y_zero: the a, b readings for z zero in y mode
        :param freq: frequency in Hz at which the measurements were made
        :param rnge: integer range value [1..7]
        :return: range number, frequency in Hz, capacitance correction, inductance correction, both in ppm
        """
        rz = str(rnge) + 'Z'
        ry = str(rnge) + 'Y'
        fsr = self.ub.unit_scale(rz)[1] * self.ub.rdialmax  # full scale resistance in ohm
        fsc = self.ub.unit_scale(ry)[0] * self.ub.xdialmax  # full scale capacitance in farad
        fsl = self.ub.unit_scale(rz)[0] * self.ub.xdialmax  # full scale inductance in henry
        imp = (z[0] - z_zero[0], z[1] - z_zero[1])  # tuple of zero-corrected dial readings
        adm = (y[0] - y_zero[0], y[1] - y_zero[1])  # tuple of zero-corrected dial readings
        cap = z[2] * 1e-12  # parallel capacitance in farad, the standards are labelled in pF
        r = imp[1] * fsr  # measured resistance in ohm, without correction for reference values
        l = -cap * (r * imp[1]) ** 2/(1 + (2 * pi * freq * cap * r) ** 2)  # inductance from thompson capacitance
        cap_cor = cap - adm[0] * fsc
        ind_cor = l - imp[0] * fsl
        return rnge, freq, cap_cor, ind_cor, cap_cor / fsc * 1e6, ind_cor / fsl * 1e6

    def report(self, _dcr, _thomp, _gain_fact, _acr_ub, _ind_ub, _cap_ub):
        hroutput = []  # a list of rows with each row being a list
        hroutput.append(['DC calibration of resistors'])
        hroutput.append(['Name', 'Value', 'Uncertainty'])
        hroutput.append(['', 'ohm', 'ohm'])
        for x in _dcr:
            row_list = []
            row_list.append(x)
            row_list.append(_dcr[x].x)
            row_list.append(_dcr[x].u)
            hroutput.append(row_list)
        hroutput.append([''])
        hroutput.append(['Phase angle corrections from Thompson set'])
        hroutput.append(['Label', 'Range', 'Freq/Hz', 'F', 'H', 'ppm C', 'ppm L'])
        for x in _thomp:
            row_list = []
            row_list.append(x)
            for y in _thomp[x]:
                row_list.append(y)
            hroutput.append(row_list)
        hroutput.append([''])
        hroutput.append(['Gain Factor'])
        hroutput.append(['Range', 'prod / ppm', 'factor / ppm', 'Freq / Hz'])
        for x in _gain_fact:
            row_list = []
            for y in _gain_fact[x]:
                row_list.append(y)
            hroutput.append(row_list)
        hroutput.append([''])
        hroutput.append(['UB measured values'])
        hroutput.append(['Label', 'G / siemen', 'R / ohm'])
        for x in _acr_ub:
            row_list = [x]
            for y in _acr_ub[x]:
                row_list.append(y.x.real)  # not displaying imaginary component or uncertainty
            hroutput.append(row_list)

        # The inductor and capacitor sets were also measured
        hroutput.append([''])
        hroutput.append(['Inductor set'])
        hroutput.append(['Label', 'L / henry', 'R / ohm'])
        for x in _ind_ub:
            row_list = [x]
            for y in _ind_ub[x]:
                row_list.append(y.x)
            hroutput.append(row_list)

        hroutput.append([''])
        hroutput.append(['Capacitor set'])
        hroutput.append(['Label', 'C / farad', 'G / siemen'])
        for x in _cap_ub:
            row_list = [x]
            for y in _cap_ub[x]:
                row_list.append(y.x)
            hroutput.append(row_list)

        # put the 'human readable' output into an excel sheet
        self.input_data.makeworkbook(hroutput, 'test_results')

if __name__ == "__main__":
    # set up for RESISTANCE class
    cal_file = r'data_csv/ub_dict_nov_2020.csv'
    data_file = r'spread_sheets/UBcalibrationJuly2014_for python.xlsx'
    output_file = r'spread_sheets/test_out2.xlsx'
    calc = RESISTANCE(cal_file, data_file, output_file)
    # collect all data
    radata = calc.dc_resistance_data('csv_data', [3, 14, 1, 4])
    zdata = calc.z_data('csv_data', [16, 43, 1, 4])
    rbdata = calc.dc_resistance_data('csv_data', [64, 78, 1, 4])
    rcdata = calc.dc_resistance_data('csv_data', [81, 85, 1, 4])
    acrdata = calc.acr_data('csv_data', [88, 101, 1, 7])
    tpdata = calc.thompson_data('csv_data', [46, 61, 1, 4])
    zero_acrdata = calc.acr_data('csv_data', [104, 117, 1, 7])  # ub zeros for acrdata
    inddata = calc.ind_data('csv_data', [120, 124, 1, 7])  # ub measurements of inductors (including zeros)
    capdata = calc.cap_data('csv_data', [127, 135, 1, 7])  # ub measurements of capacitors
    # dictionaries for key results
    key_dcr = {}  # true values of dc resistors
    key_thomp = {}  # phase corrections from Thompson resistors
    key_gain_fact = {}  # estimates of gain factor error
    key_acr_ub = {}  # calculated ub values of the resistors
    key_ind_ub = {}  # calculated ub values of the inductors
    key_cap_ub = {}  # calculated ub values of the capacitors

    # dc build up to measure internal resistance standards of universal bridge
    sr104_corrn = calc.temp_sr104(radata['sens_sr104'])
    true_sr104_t = radata['true_sr104_20'] + sr104_corrn  # true value of SR104 at the measured temperature
    dmm_corrn_10k = calc.meter_corrn(true_sr104_t, radata['sr104'])  # correction for the meter at 10 kohm
    true_ep_100k = radata['ep_100k'] + dmm_corrn_10k
    true_esp_100k = calc.series_parallel(true_ep_100k, radata['esp_100k'], radata['er10_100k'])
    dmm_corrn_100k = calc.meter_corrn(true_esp_100k, radata['esp_100k'])  # correction for the meter at 100 kohm
    true_es_100k = 100 * true_ep_100k  # assume perfect Hamon ratio
    dmm_corrn_1M = calc.meter_corrn(true_es_100k, radata['es_100k'])
    true_g1 = radata['g1'] + dmm_corrn_100k
    print('G1', true_g1, (true_g1/1e5 - 1) * 1e6)
    true_g2 = radata['g2'] + dmm_corrn_100k
    print('G2', true_g2, (true_g2/1e5 - 1) * 1e6)
    true_r4a = radata['r4a'] + dmm_corrn_10k
    print('R4A', true_r4a, (true_r4a/1e4 - 1) * 1e6)
    true_r4b = radata['r4b'] + dmm_corrn_100k
    print('R4B', true_r4b, (true_r4b/1e5 - 1) * 1e6)
    true_r4c = radata['r4c'] + dmm_corrn_1M
    print('R4C', true_r4c, (true_r4c/1e6 - 1) * 1e6)

    key_dcr['true_sr104_t'] = true_sr104_t
    key_dcr['true_ep_100k'] = true_ep_100k
    key_dcr['true_esp_100k'] = true_esp_100k
    key_dcr['true_es_100k'] = true_es_100k
    key_dcr['true_g1'] = true_g1
    key_dcr['true_g2'] = true_g2
    key_dcr['true_r4a'] = true_r4a
    key_dcr['true_r4b'] = true_r4b
    key_dcr['true_r4c'] = true_r4c

   # thompson phase angle standards
    thomp_6a = calc.phase_error(tpdata['thomp_100k_4_z_1592'], tpdata['thomp_100k_4_y_1592'], zdata['zero6z_1592'], zdata['zero6y_1592'], 1592, 6)
    thomp_6b = calc.phase_error(tpdata['thomp_100k_4_z_160'], tpdata['thomp_100k_4_y_160'], zdata['zero6z_160'], zdata['zero6y_160'], 160, 6)
    thomp_5a = calc.phase_error(tpdata['thomp_10k_4_z_1592'], tpdata['thomp_10k_4_y_1592'], zdata['zero5z_1592'], zdata['zero5y_1592'], 1592, 5)
    thomp_5b = calc.phase_error(tpdata['thomp_10k_4_z_160'], tpdata['thomp_10k_4_y_160'], zdata['zero5z_160'], zdata['zero5y_160'], 160, 5)
    thomp_4a = calc.phase_error(tpdata['thomp_1k_4_z_1592'], tpdata['thomp_1k_4_y_1592'], zdata['zero4z_1592'], zdata['zero4y_1592'], 1592, 4)
    thomp_4b = calc.phase_error(tpdata['thomp_1k_4_z_160'], tpdata['thomp_1k_4_y_160'], zdata['zero4z_160'], zdata['zero4y_160'], 160, 4)
    thomp_3a = calc.phase_error(tpdata['thomp_100_2_z_1592'], tpdata['thomp_100_2_y_1592'], zdata['zero3z_1592'], zdata['zero3y_1592'], 1592, 3)
    thomp_3b = calc.phase_error(tpdata['thomp_100_2_z_160'], tpdata['thomp_100_2_y_160'], zdata['zero3z_160'], zdata['zero3y_160'], 160, 3)

    key_thomp['thomp_6a'] = thomp_6a
    key_thomp['thomp_6b'] = thomp_6b
    key_thomp['thomp_5a'] = thomp_5a
    key_thomp['thomp_5b'] = thomp_5b
    key_thomp['thomp_4a'] = thomp_4a
    key_thomp['thomp_4b'] = thomp_4b
    key_thomp['thomp_3a'] = thomp_3a
    key_thomp['thomp_3b'] = thomp_3b

    # dc measurements of external resistors to be measured by the universal bridge
    sr104_corrnb = calc.temp_sr104(rbdata['sens_sr104b'])
    true_sr104b_t = radata['true_sr104_20'] + sr104_corrnb  # true value of SR104 at the measured temperature
    dmm_corrnb_10k = calc.meter_corrn(true_sr104b_t, rbdata['sr104b'])  # correction for the meter at 10 kohm
    true_es_1k = rbdata['es_1k'] + dmm_corrnb_10k
    true_esp_1k = calc.series_parallel(true_es_1k / 100, rbdata['esp_1k'], rbdata['er10_1k'])  # /100 as using series value
    dmm_corrnb_1k = calc.meter_corrn(true_esp_1k, rbdata['esp_1k'])  # correction for the meter at 1 kohm
    true_er1_1k = rbdata['er1_1k'] + dmm_corrnb_1k
    true_es_100 = rbdata['es_100'] + dmm_corrnb_1k
    true_ep_1k = true_es_1k / 100
    dmm_corrnb_100 = calc.meter_corrn(true_ep_1k, rbdata['ep_1k'])
    true_er1_100 = rbdata['er1_100'] + dmm_corrnb_100
    true_ep_100 = true_es_100 / 100
    dmm_corrnb_10 = calc.meter_corrn(true_ep_100, rbdata['ep_100'])
    true_er1_10 = rbdata['er1_10'] + dmm_corrnb_10
    true_es_10 = rbdata['es_10'] + dmm_corrnb_100
    true_v_100k = rbdata['v_100k'] + dmm_corrn_100k  # note that this was taken from data set a analysis
    true_v_10k = rbdata['v_10k'] + dmm_corrnb_10k
    true_v_100 = rbdata['v_100'] + dmm_corrnb_100
    sr104_corrnc = calc.temp_sr104(rcdata['sens_sr104c'])
    true_sr104c_t = radata['true_sr104_20'] + sr104_corrnc  # true value of SR104 at the measured temperature
    dmm_corrnc_10k = calc.meter_corrn(true_sr104c_t, rcdata['sr104c'])  # correction for the meter at 10 kohm
    true_epc_100k = rcdata['ep_100k'] + dmm_corrnc_10k
    true_esc_100k = 100 * true_epc_100k
    dmm_corrn_1M = calc.meter_corrn(true_esc_100k, rcdata['es_100k'])
    true_v_1M = rcdata['v_1M'] + dmm_corrn_1M

    key_dcr['true_sr104b_t'] = true_sr104b_t
    key_dcr['true_es_1k'] = true_es_1k
    key_dcr['true_esp_1k'] = true_esp_1k
    key_dcr['true_er1_1k'] = true_er1_1k
    key_dcr['true_es_100'] = true_es_100
    key_dcr['true_ep_1k'] = true_ep_1k
    key_dcr['true_ep_100'] = true_ep_100
    key_dcr['true_er1_100'] = true_er1_100
    key_dcr['true_er1_10'] = true_er1_10
    key_dcr['true_es_10'] = true_es_10
    key_dcr['true_v_100k'] = true_v_100k
    key_dcr['true_v_10k'] = true_v_10k
    key_dcr['true_v_100'] = true_v_100
    key_dcr['true_sr104c_t'] = true_sr104c_t
    key_dcr['true_epc_100k'] = true_epc_100k
    key_dcr['true_esc_100k'] = true_esc_100k
    key_dcr['true_v_1M'] = true_v_1M

    g1_g2 = (true_g1.x/true_g2.x - 1) * 1e6  # g1/g2 in ppm

    # ac measurements of external resistors
    # first the ratio factor
    for x in acrdata:
        by_bz = (sqrt(acrdata[x][1] * acrdata[x][3])/1 - 1)*1e6  # sqrt of the multiplied dials in ppm
        key_gain_fact[x] = (acrdata[x][4], by_bz, by_bz - g1_g2, acrdata[x][5])  # range and square root of multiplied dials

    # To proceed further we need to create a calibration file using the latest values of the internal standards.
    # For now this is best created manually. This provides a check of dc resistance against the UB values.
    # This uses cal constants calculated in the first part, but as stored in the calfile...i.e. no GTC link.
    # Use readings from dictionary acr_data and compare with dc results in the key_dcr dictionary.
    calfile = r'ub_dict_cal_test.csv'
    room_temperature = ureal(20, 0.5, 10, 'temperature')  # this should be the ambient temperature given in conditions
    ub = UNIVERSALBRIDGE(calfile, room_temperature)
    for x in acrdata:  # calculate the impedance and admittance
        ub_rangey = str(acrdata[x][4]) + 'Y'
        ub_rangez = str(acrdata[x][4]) + 'Z'
        f = acrdata[x][5]
        # need to subtract zeros!
        answerz = ub.bridge_value(ub_rangez, acrdata[x][3]*1e7, acrdata[x][2]*1e6, f, 1)
        answery = ub.bridge_value(ub_rangey, acrdata[x][1]*1e7, acrdata[x][0]*1e6, f, 1)
        key_acr_ub[x] = [answery, answerz]

    # a set of inductors is measured
    for x in inddata:
        rangez = inddata[x][4]
        f = inddata[x][5]
        a = (inddata[x][0] - inddata[x][2]) * 1e6  # zero corrected as integer rather than decimal dial
        b = (inddata[x][1] - inddata[x][3]) * 1e7  # zero corrected
        z = ub.bridge_value(rangez, b, a, f, 1)
        l = z.imag / (2 * pi * f)
        r = z.real
        key_ind_ub[x] = (l, r)

    # a set of capacitors is measured
    for x in capdata:
        rangey = capdata[x][4]
        f = capdata[x][5]
        a = (capdata[x][0] - capdata[x][2]) * 1e6  # zero corrected as integer rather than decimal dial
        b = (capdata[x][1] - capdata[x][3]) * 1e7  # zero corrected
        y = ub.bridge_value(rangey, b, a, f, 1)
        c = y.imag / (2 * pi * f)
        g = y.real
        key_cap_ub[x] = (c, g)

    # Summarise calculations in excel report
    calc.report(key_dcr, key_thomp, key_gain_fact, key_acr_ub, key_ind_ub, key_cap_ub)
