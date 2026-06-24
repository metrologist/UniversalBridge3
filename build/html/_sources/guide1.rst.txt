This guide explains where and how to enter the data required for processing with the
Python software. The main software change since E.023.07 was validated in 2020 is the calibration
analysis with *ubcal.py*.The core calculation of the Universal Bridge remains the same. New
impedance artefacts are likely to require some specific code to ensure that the report meets
the client's needs in terms of preferred connection method and relevant zero reference. Final report preparation
still relies on Excel to manipulate the csv output file into the final report table.


.. image:: Data_flow2.png

Components
==========
For each capacitance scale buildup, the current basic characteristics of the key components need to be available. These characteristics are generally measured with an LCR meter.

Capacitors
----------
Measurements are carried out on capacitors defined as two terminal-pair components. It is assumed that the admittances to case, both at the high and low voltage terminals (yhv and ylv) are relatively stable with time so do not need routine remeasurement. These admittances only have a second-order impact on the two terminal-pair value of the capacitor.
A CAPACITOR object is defined in *components.py* with a name, nominal capacitance value (capacitance, conductance), yhv (capacitance, conductance), ylv (capacitance, conductance), angular frequency, relative uncertainty (of yhv and ylv), and the option of key word arguments.
CAPACITOR objects are created by running *create_component.py* that stores the objects in a csv file. The values are hard coded in the *create_capacitors()* method and so the code needs modification if new values are required.
The ‘best value’ of a CAPACITOR will be updated after analysing the results of a scale buildup, but the port admittances remain unaltered.

Calibration
===========

Balance Injection
-----------------
Calculating the correction factors for the balance injection dials is done by *cal_balance.py* using data entered in the file dialcal_in_yyyy-mm-dd.csv. There is no script for creating this file, but it does not take long to edit a previous version with the IVD settings, the measured dc value of the Thompson resistor and its parallel capacitance. Be careful not to change any of the quotation marks as they are critical for correctly reading the dictionary.

.. code-block::

  Date,07-Jul-25
  Reference,E005 Cap. Scale, p.64, 100k #4
  w,1.00E+04
  alpha1,"{""x"": 0.999759, ""u"": 2e-06, ""df"": Infinity, ""label"": ""alpha1""}"
  beta1,"{""x"": -0.000658, ""u"": 2e-06, ""df"": Infinity, ""label"": ""beta1""}"
  alpha2,"{""x"": -0.002058, ""u"": 2e-06, ""df"": Infinity, ""label"": ""alpha2""}"
  beta2,"{""x"": 1.002480, ""u"": 2e-06, ""df"": Infinity, ""label"": ""beta2""}"
  r,0.01
  k,0.2
  c1,es14
  c2,gr1000a
  label y3,100k4
  r3,100.198225e3
  ur3,0.1
  c3,0.028e-12
  uc3,0.001e-12


Python Scripts
==============

=====================  ================================================
Script                 Purpose
=====================  ================================================
*main.py*              edited to select files for *all_buildup.py*
*all_buildup.py*       final analysis of a set of buildups
*analysis.py*          reprocesses raw buildup results with corrections for the constraint and influence quantities
*archive.py*           general storage of GTC values and dictionaries in csv files
*cal_balance.py*       calculates correction factors for the main balance amplifier
*cal_main_ratio.py*    calculates the 10:1 voltage ratio
*cap_fit.py*           analyses historical values of all the capacitors
*capscale.py*          produces raw results from a buildup
*components.py*        objects that contain properties of capacitors and leads (COMPONENT)
*conditions.py*        manages the dictionary of temperature and pressure measurements
*constrain.py*         manages external calibration values
*create_component.py*  creates csv files for a COMPONENT
*funcdictl.py*         utility to define functions for MSL-NLF module
*intertime.py*         utility to convert between different representations of time
*primcal.py*           supports reference.py
*reference.py*         uses external calibrations to predict values of the reference AH11
*sql_cap.py*           extracts temperatures from the capacitance logging system [in caplogger2014]
*summary_check.py*     summarises output of capscale.py before final processing
*view.py*              viewer for graphs produced by all_buildup.py
=====================  ================================================