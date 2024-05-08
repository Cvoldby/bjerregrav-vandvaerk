"""
This is a network connection module with the connect_to_network function. 

The function takes the name and password for the network you want the Pico W to connect to.
"""
import network
import time

def connect_to_network(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    
    wlan.active(True)
    wlan.config(pm=0x11140) # Disable power-save mode
    wlan.connect(ssid, password)

    max_wait = 10 # Initialize network connection
    while max_wait > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        max_wait -= 1
        print("Waiting for connection...")
        time.sleep(1)

    if wlan.status() != 3:
        raise RuntimeError("network connection failed")
    else:
        print("Connected")
        status = wlan.ifconfig()
        print(f"ip: {status[0]}")

