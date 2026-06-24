import csv
import time
from datetime import date, datetime

def print_hi(name = 'DMM 3468A '):
    # task name:
    print(f'Hi, {name} is starting....')
    prile(name)


def prile(*args):  # print and file
    """
    Simple combination of print to stdout and print to E3458A_Res_Date.csv
    :param args: anything a print statement will take
    :return: prints and writes to csv file
    """
    today = str(date.today())
    logfile = 'E3458A_Res_' + today + '.csv'  # this could be passed to the function if more convenient
    print(args)
    with open(logfile, 'a', newline = '') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(args)
    csvFile.close()


def before_DMM_in_use(a = 300):
    '''time of the job and time stamp'''
    print(f'Hi, now it is, {time.ctime()}')
    prile(time.ctime())
    print('Please wait for at least 5 mins before using the meter after ACAL, thanks' )
    time.sleep(a)
    print(f'Hi, now it is, {time.ctime()}, DMM is ready')


if __name__ == '__main__':
    before_DMM_in_use()

