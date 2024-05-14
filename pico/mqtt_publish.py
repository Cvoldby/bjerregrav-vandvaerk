"""
This is the file for mqtt publishing and handling
"""
from time import sleep

from umqtt.simple import MQTTClient

from network_connect import connect_to_network
from sensor import *
from conf import *

def connect_client(client_id='vand_broker', server='10.120.0.87', port=5000):
    while True:
        try:
            client = MQTTClient(
                client_id=b'vand_broker',
                server=b'10.120.0.87',
                port=5000,
                keepalive=7200,
                #user=b'',
                #password=b''
            )

            return client
            
        except:
            sleep(2)
            continue
    

def publish_elpriser(client, prices):
    #client = connect_client()
    #prices = get_elpriser_API_tarif()
    client.publish('elpriser/prices', str(prices)) # publish as list

    for idx, price in enumerate(prices):
        client.publish('elpriser/price', str(price))

    client.disconnect()


def publish_liquid_level(Client):
    #client = connect_client()

    level = liquid_level()

    Client.publish('water/level', str(level))


if __name__ == "__main__":
    
    # Connect to network - standard ITEK 2nd
    ssid = "ITEK 2nd" 
    password = "2nd_Semester_F24v"
    connect_to_network(ssid, password)