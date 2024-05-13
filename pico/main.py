"""
This is the main file for the micro controller
"""
from time import sleep

from umqtt.simple import MQTTClient

from network_connect import connect_to_network
from get_prices import get_elpriser_API_tarif
from date import get_date_today
from mqtt_publish import *
from sensor import *

# Connect to network - standard ITEK 2nd
ssid = "ITEK 2nd" 
password = "2nd_Semester_F24v"
connect_to_network(ssid, password)

client = MQTTClient(
    client_id=b'vand_broker',
    server=b'10.120.0.87',
    port=5000,
    keepalive=7200,
    #user=b'',
    #password=b''
)

#client.connect()


while True:
    current_day, current_time = get_date_today()

    publish_liquid_level()

    if current_time[0] == 13 and current_time[1] > 15:
        prices = get_elpriser_API_tarif()

        publish_elpriser()

        # calculate cheapest pump plan according to needs
        hour_need_to_pump = 10

    
    sleep(10)
    

