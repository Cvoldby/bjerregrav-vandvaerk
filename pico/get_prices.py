"""
This file includes function regarding retrieving el prices.
"""

import urequests

from network_connect import connect_to_network
from date import get_date_today as gdt

from conf import *
""" 
TARIF_PRISER = {
    'Lavlast': 13.76,
    'Højlast': 20.65,
    'Spidslast': 53.68
}
 """
def get_elpriser_API():
    today, c_time = gdt()
    print(today)

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
    
def get_elpriser_API_date(date):
    request_addr = "https://www.elprisenligenu.dk/api/v1/prices/" + date + "_DK1.json"
    #print(request_addr)

    response = urequests.get(request_addr)
    #print(response.status_code) # print status code to check - want 200 all i good

    elpriser = []
    for data in response.json():
        elpriser.append(data['DKK_per_kWh'] * 100)
    
    # tillæg moms?
    return elpriser

def get_elpriser_API_tarif_tomorrow(date):

    prices = get_elpriser_API_date(date)
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
    # Connect to network - standard ITEK 2nd
    ssid = "ITEK 2nd" 
    password = "2nd_Semester_F24v"

    connect_to_network(ssid, password)

    #get_date_today()
    #print(get_elpriser_API())

    #print(get_elpriser_API_tarif())
    test = get_elpriser_API_tarif()
    #print(test)
    print(str(test))

    print(gdt())
