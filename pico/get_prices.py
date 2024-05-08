"""Some is happening"""

import time

import ntptime
import urequests

from network_connect import connect_to_network
#from date import get_date_today

from conf import TARIF_PRISER

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

            return today
        except OSError as e:
            time.sleep(5)
            continue



def get_elpriser_API():
    today = get_date_today()

    request_addr = "https://www.elprisenligenu.dk/api/v1/prices/" + today + "_DK1.json"
    #print(request_addr)

    response = urequests.get(request_addr)

    #print(response.status_code) # print status code to check - want 200 all i good

    #for i in response.json():
    #   print('Tidsinterval:', i['time_start'][11:16], i['time_end'][11:16], 'Pris', i['DKK_per_kWh'], 'oere/kWh')

    elpriser = []
    for data in response.json():
        elpriser.append(data['DKK_per_kWh'] * 100)
    

    # tillæg moms?
    return elpriser

def get_elpriser_API_tarif():

    prices = get_elpriser_API()
    prices_tarif = []
    for idx, price in enumerate(prices):
        if idx < 6:
            prices_tarif.append(price+TARIF_PRISER['Lavlast'])

        elif idx < 17:
            prices_tarif.append(price+TARIF_PRISER['Højlast'])

        elif idx < 21:
            prices_tarif.append(price+TARIF_PRISER['Spidslast'])
        
        else:
            prices_tarif.append(price+TARIF_PRISER['Højlast'])

    return prices_tarif
    


if __name__ == "__main__":
    #get_date_today()
    #print(get_elpriser_API())

    #print(get_elpriser_API_tarif())
    test = get_elpriser_API_tarif()
    #print(test)
    print(str(test))
