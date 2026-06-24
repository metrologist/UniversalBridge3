#set up a csv file, name as the currengt date
from datetime import datetime, date
import csv

def prile(*args):  # print and file
    """
    Simple combination of print to stdout and print to log.csv
    :param args: anything a print statement will take
    :return: prints and writes to csv file
    """
    today = str(date.today())
    logfile = 'E4980_02_' + today + '.csv'  # this could be passed to the function if more convenient
    print(args)
    with open(logfile, 'a', newline = '') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(args)
    csvFile.close()