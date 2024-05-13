import time

import ntptime
from network_connect import connect_to_network
from conf import *

# Connect to network - standard ITEK 2nd
ssid = "ITEK 2nd" 
password = "2nd_Semester_F24v"

connect_to_network(ssid, password)

def get_date_today():
    
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




if __name__ == "__main__":
    print(get_date_today())

