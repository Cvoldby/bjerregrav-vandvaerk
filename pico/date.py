"""
This file includes two functions.
- get_date_today
- get_date_tomorrow

The functions need internet connection to access a NTP server

"""

import time

import ntptime
from network_connect import connect_to_network
from conf import *

def get_date_today():
    """This function returns a tuple with the date in format year/month-day and the time [hour, minute]"""
    
    while True:
        try:
            ntptime.settime()

            sec = ntptime.time()

            sec = int(sec + (2*3600))
            (year, month, day, hours, minutes, seconds, weekday, yearday) = time.localtime(sec)
            
            today = f"{year}/{month:02}-{day:02}" 
            current_time = [hours, minutes]

            return today, current_time
        except OSError as e:
            time.sleep(5)
            continue


def get_date_tomorrow():
    """This function returns the tomorrows date in format year/month-day"""
    
    while True:
        try:
            ntptime.settime()

            sec = ntptime.time()

            sec = int(sec + (26*3600))
            (year, month, day, hours, minutes, seconds, weekday, yearday) = time.localtime(sec)
            
            tomorrow = f"{year}/{month:02}-{day:02}" 
            
            return tomorrow
        except OSError as e:
            time.sleep(5)
            continue


if __name__ == "__main__":
    # Connect to network - standard ITEK 2nd
    ssid = "ITEK 2nd" 
    password = "2nd_Semester_F24v"

    connect_to_network(ssid, password)

    print(get_date_today())
    print(get_date_tomorrow())

