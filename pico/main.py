"""
This is the main file for the micro controller
"""
from time import sleep
from random import randint

from network_connect import connect_to_network

max_wait = 5
while max_wait > 0:
    try:
        from umqtt.simple import MQTTClient
        break
    except ImportError:
        import mip
        mip.install("umqtt.simple")
    max_wait -= 1
    sleep(1)


from get_prices import *
from date import get_date_today, get_date_tomorrow
from mqtt_publish import *
from sensor import *
from conf import *


sleep(2)

# Connect to network - standard ITEK 2nd
connect_to_network('ITEK 2nd', '2nd_Semester_F24v')

sleep(2)

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

water_level = 80
pump_status = b'OFF'

def sub_callback(topic, msg):
    global pump_status
    pump_status = msg
    
    print((topic, msg))

client.set_callback(sub_callback)
client.subscribe(b'F24v/grp8/pump_status')
    

while True:
    msg = client.check_msg()
    print(pump_status)
    if pump_status == b'ON':
        water_level += randint(8,10)

    #current_day, current_time = get_date_today()
    #tomorrow_date = get_date_tomorrow()

    #print(current_day, current_time)

    publish_liquid_level(client)
    print("send")

    #if current_time[0] == 14 and current_time[1] < 10:
        #prices = get_elpriser_API_tarif_tomorrow(tomorrow_date)

        #publish_elpriser(client, prices)
        # calculate cheapest pump plan according to needs for tomorrow
        #hour_need_to_pump = 10
        #pass

    client.publish('F24v/grp8/vandniveau', str(water_level))
    water_level -= randint(2,5)
    sleep(2)
    
        

