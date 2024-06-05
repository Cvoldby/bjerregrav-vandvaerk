"""
This is the main file for the micro controller
"""
from time import sleep
from random import randint

from machine import RTC

from network_connect import connect_to_network

max_wait = 3
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
from date import get_date_today, get_date_tomorrow, set_RTC_pico
from mqtt_publish import *
from sensor import *
from conf import *

# Connect to network - standard ITEK 2nd
sleep(1)
connect_to_network('ITEK 2nd', '2nd_Semester_F24v')

# Initalize MQTT Client
sleep(1)
client = MQTTClient(
    client_id=b'chvoclient',
    server=b'35.210.127.92',
    port=5000,
    keepalive=7200,
    user=b'database',
    password=b'FegZUO'
)

client.connect()
print('Connected mqtt')

# init variables
pump_plan_today = [] # 48 => 0, 49 => 1
pump_plan_tomorrow = []

def sub_callback(topic, msg):
    global pump_plan_today, pump_plan_tomorrow
    print((topic, msg))
    
    if topic == b'pump/timer_today':
        pump_plan_today = list(msg.decode().split(","))
        pump_plan_today = [int(x) for x in pump_plan_today]
    elif topic == b'pump/timer_tomorrow':
        pump_plan_tomorrow = list(msg.decode().split(","))
        pump_plan_tomorrow = [int(x) for x in pump_plan_tomorrow]

client.set_callback(sub_callback)
client.subscribe(b'pump/timer_today')
client.subscribe(b'pump/timer_tomorrow')
    
RTC = set_RTC_pico(RTC())

current_day, current_time = get_date_today()
tomorrow_date = get_date_tomorrow()

try:
    prices_today = get_elpriser_API_tarif()
    publish_elpriser(client, prices_today)
    if RTC.datetime()[4] >= 14:
        prices_tomorrow = get_elpriser_API_tarif_tomorrow(tomorrow_date)
        publish_elpriser(client, prices_tomorrow)
    print('succes db call')
except:
    print('fail db call')
    pass


# Enter main loop
while True:
    msg = client.check_msg() # listen - not blocking
    
    # publish current water level
    try:
        publish_liquid_level(client)
        print("send")
    except:
        pass

    # pump logic
    try:
        water_level = liquid_level()
        print(water_level)
        if water_level <= .20:
            print('Begin pump')
        else:
            hour_as_idx = RTC.datetime()[4]
            if pump_plan_today[hour_as_idx] == 1:
                print('Begin pump')
            else:
                print('Not pumping')
    except:
        pass
    


    # update stuff
    try:
        time_now = RTC.datetime()
        if time_now[4] == 00 and time_now[5] <= 10:
            current_day, current_time = get_date_today()
            tomorrow_date = get_date_tomorrow()
            RTC = set_RTC_pico(RTC)

            pump_plan_today, pump_plan_tomorrow = pump_plan_tomorrow, []
        # update prices
        elif time_now[4] == 14 and time_now[5] <= 10:
            prices_tomorrow = get_elpriser_API_tarif_tomorrow(tomorrow_date)
            publish_elpriser(client, prices_tomorrow)
    except:
        pass

    sleep(2)
    
        

