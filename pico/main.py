"""
This is the main file for the micro controller
"""


from umqtt.simple import MQTTClient

from network_connect import connect_to_network
from get_prices import get_elpriser_API_tarif

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

client.connect()

list_prices = get_elpriser_API_tarif()

for price in list_prices:
    client.publish('elpriser/', str(price))
