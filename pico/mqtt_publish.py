"""
This is the file for mqtt publishing and handling
"""

from umqtt.simple import MQTTClient

from network_connect import connect_to_network
from get_prices import get_elpriser_API_tarif
from sensor import *
from conf import *

# Connect to network - standard ITEK 2nd
ssid = "ITEK 2nd" 
password = "2nd_Semester_F24v"
connect_to_network(ssid, password)


def connect_client(client_id='vand_broker', server='10.120.0.87', port=5000):
    client = MQTTClient(
        client_id=b'vand_broker',
        server=b'10.120.0.87',
        port=5000,
        keepalive=7200,
        #user=b'',
        #password=b''
    )

    client.connect()

    return client

list_prices = get_elpriser_API_tarif()

def publish_elpriser():
    client = connect_client()
    prices = get_elpriser_API_tarif()
    client.publish('elpriser/', str(prices)) # publish as list

    for idx, price in enumerate(prices):
        client.publish('elpriser/', str(price))


def publish_liquid_level():
    client = connect_client()

    level = liquid_level()

    client.publish('water/level', str(level))

