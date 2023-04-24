from ubcal import RESISTANCE
from GTC import ureal
from ubridge3 import UNIVERSALBRIDGE
from math import sqrt, pi


# set up for RESISTANCE class
cal_file = r'ub_dict_nov_2020.csv'
data_file = r'UBcalibrationApril2023.xlsx'
output_file = r'out_2023.xlsx'
calc = RESISTANCE(cal_file, data_file, output_file)
# collect all data
radata = calc.dc_resistance_data('csv_data', [3, 14, 1, 4])  # set 'a' of dc resistance measurements
zdata = calc.z_data('csv_data', [16, 43, 1, 4])  # ub zeros for thompson resistors
rbdata = calc.dc_resistance_data('csv_data', [64, 78, 1, 4])  # set 'b' of dc resistance measurements
rcdata = calc.dc_resistance_data('csv_data', [81, 85, 1, 4])  # set 'c' of dc resistance measurements
acrdata = calc.acr_data('csv_data', [88, 101, 1, 7])  # ub measurements of the resistors
tpdata = calc.thompson_data('csv_data', [46, 61, 1, 4])  # ub measurements of the thompson phase angle standards
zero_acrdata = calc.acr_data('csv_data', [104, 117, 1, 7])  # ub zeros for acrdata
inddata = calc.ind_data('csv_data', [133, 137, 1, 7])  # ub measurements of inductors (including zeros)
capdata = calc.cap_data('csv_data', [140, 148, 1, 7])  # ub measurements of capacitors

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
print('G1', true_g1, (true_g1 / 1e5 - 1) * 1e6)
true_g2 = radata['g2'] + dmm_corrn_100k
print('G2', true_g2, (true_g2 / 1e5 - 1) * 1e6)
true_r4a = radata['r4a'] + dmm_corrn_10k
print('R4A', true_r4a, (true_r4a / 1e4 - 1) * 1e6)
true_r4b = radata['r4b'] + dmm_corrn_100k
print('R4B', true_r4b, (true_r4b / 1e5 - 1) * 1e6)
true_r4c = radata['r4c'] + dmm_corrn_1M
print('R4C', true_r4c, (true_r4c / 1e6 - 1) * 1e6)

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
thomp_6a = calc.phase_error(tpdata['thomp_100k_4_z_1592'], tpdata['thomp_100k_4_y_1592'], zdata['zero6z_1592'],
                            zdata['zero6y_1592'], 1592, 6)
# thomp_6b = calc.phase_error(tpdata['thomp_100k_4_z_160'], tpdata['thomp_100k_4_y_160'], zdata['zero6z_160'],
#                             zdata['zero6y_160'], 160, 6)
thomp_5a = calc.phase_error(tpdata['thomp_10k_4_z_1592'], tpdata['thomp_10k_4_y_1592'], zdata['zero5z_1592'],
                            zdata['zero5y_1592'], 1592, 5)
# thomp_5b = calc.phase_error(tpdata['thomp_10k_4_z_160'], tpdata['thomp_10k_4_y_160'], zdata['zero5z_160'],
#                             zdata['zero5y_160'], 160, 5)
thomp_4a = calc.phase_error(tpdata['thomp_1k_4_z_1592'], tpdata['thomp_1k_4_y_1592'], zdata['zero4z_1592'],
                            zdata['zero4y_1592'], 1592, 4)
# thomp_4b = calc.phase_error(tpdata['thomp_1k_4_z_160'], tpdata['thomp_1k_4_y_160'], zdata['zero4z_160'],
#                             zdata['zero4y_160'], 160, 4)
thomp_3a = calc.phase_error(tpdata['thomp_100_2_z_1592'], tpdata['thomp_100_2_y_1592'], zdata['zero3z_1592'],
                            zdata['zero3y_1592'], 1592, 3)
# thomp_3b = calc.phase_error(tpdata['thomp_100_2_z_160'], tpdata['thomp_100_2_y_160'], zdata['zero3z_160'],
#                             zdata['zero3y_160'], 160, 3)

key_thomp['thomp_6a'] = thomp_6a
# key_thomp['thomp_6b'] = thomp_6b
key_thomp['thomp_5a'] = thomp_5a
# key_thomp['thomp_5b'] = thomp_5b
key_thomp['thomp_4a'] = thomp_4a
# key_thomp['thomp_4b'] = thomp_4b
key_thomp['thomp_3a'] = thomp_3a
# key_thomp['thomp_3b'] = thomp_3b

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
print('true_sr104c_t', true_sr104c_t)
print('rcdata["sr104c"]', rcdata['sr104c'])
true_epc_100k = rcdata['ep_100k'] + dmm_corrnc_10k
print('dmm 10k correction', dmm_corrnc_10k)
print('true ep 100k', true_epc_100k)
true_esc_100k = 100 * true_epc_100k
dmm_corrn_1M = calc.meter_corrn(true_esc_100k, rcdata['es_100k'])
print('true es 100k', true_esc_100k)
print('dmm correction at 1 Mohm', dmm_corrn_1M)
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

g1_g2 = (true_g1.x / true_g2.x - 1) * 1e6  # g1/g2 in ppm

# ac measurements of external resistors
# first the ratio factor
for x in acrdata:
    by_bz = (sqrt((acrdata[x][1] - zero_acrdata[x][1]) * (acrdata[x][3] - zero_acrdata[x][3]) ) / 1 - 1) * 1e6  # sqrt of the multiplied dials in ppm
    key_gain_fact[x] = (acrdata[x][4], by_bz, by_bz - g1_g2, acrdata[x][5])  # range and square root of multiplied dials

# To proceed further we need to create a calibration file using the latest values of the internal standards.
# For now this is best created manually. This provides a check of dc resistance against the UB values.
# This uses cal constants calculated in the first part, but as stored in the calfile...i.e. no GTC link.
# Use readings from dictionary acr_data and compare with dc results in the key_dcr dictionary.
calfile = r'ub_dict_cal_2023.csv'
room_temperature = ureal(20, 0.5, 10, 'temperature')  # this should be the ambient temperature given in conditions
ub = UNIVERSALBRIDGE(calfile, room_temperature)
for x in acrdata:  # calculate the impedance and admittance
    ub_rangey = str(acrdata[x][4]) + 'Y'
    ub_rangez = str(acrdata[x][4]) + 'Z'
    f = acrdata[x][5]
    # need to subtract zeros!
    answerz = ub.bridge_value(ub_rangez, (acrdata[x][3] - zero_acrdata[x][3]) * 1e7, (acrdata[x][2] - zero_acrdata[x][2]) * 1e6, f, 1)
    answery = ub.bridge_value(ub_rangey, (acrdata[x][1] - zero_acrdata[x][1]) * 1e7, (acrdata[x][0] - zero_acrdata[x][0]) * 1e6, f, 1)
    key_acr_ub[x] = [answery, answerz]


# a set of inductors is measured
for x in inddata:
    rangez = inddata[x][4]
    f = inddata[x][5]
    a = (inddata[x][0] - inddata[x][2]) * 1e6  # zero corrected as integer rather than decimal dial
    b = (inddata[x][1] - inddata[x][3]) * 1e7  # zero corrected
    z = ub.bridge_value(rangez,b, a, f, 1)
    l = z.imag/(2 * pi * f)
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
