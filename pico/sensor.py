from time import sleep

from machine import Pin, ADC


def output_test(adc_pin=28):
    """This function tests the connection and output for the liquid level sensor"""
    tryk_sensor = ADC(Pin(adc_pin))
    
    test_max = 10
    while test_max > 0:
        print(tryk_sensor.read_u16())
        test_max -= 1
        sleep(1)


def liquid_level(adc_pin=28):
    tryk_sensor = ADC(Pin(adc_pin))

    level = tryk_sensor.read_u16()

    return round(level/65535, 3)
    

