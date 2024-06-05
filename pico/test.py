"""
This file includes several test for the different functionalities of the Pico
"""

from machine import Pin

Pin(4).off()

def test_pico_time():
    return True