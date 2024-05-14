"""
This is the main file for the micro controller
"""
from time import sleep

from umqtt.simple import MQTTClient

from network_connect import connect_to_network
from get_prices import *
from date import get_date_today, get_date_tomorrow
from mqtt_publish import *
from sensor import *
from conf import *

# Connect to network - standard ITEK 2nd
connect_to_network('ITEK 2nd', '2nd_Semester_F24v')

 
client = MQTTClient(
    client_id=b'chvoclient',
    server=b'10.100.0.96',
    port=0,
    keepalive=7200,
    #user=b'',
    #password=b''
)

client.connect()
print('Connected mqtt')



while True:
    #current_day, current_time = get_date_today()
    #tomorrow_date = get_date_tomorrow()

    publish_liquid_level(client)
    print("send")

    """ 

    if current_time[0] == 16:
        prices = get_elpriser_API_tarif_tomorrow(tomorrow_date)

        publish_elpriser(prices)

        # calculate cheapest pump plan according to needs for tomorrow
        #hour_need_to_pump = 10

        """
    sleep(2)
    
        

