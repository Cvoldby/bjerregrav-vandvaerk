"""
Dette er en en konfirgueringsfil med relevante parametre.
"""


"""
Tarifmodel 

00:00-06:00 - lavlast
06:00-17:00 - højlast
17:00-21:00 - spidslast
21:00-24:00 - højlast

"""

TARIF_PRISER = {
    'Lavlast': 13.76,
    'Højlast': 20.65,
    'Spidslast': 53.68
}

Kritisk_vandniveau = 100 # liter

minimumsboringstid = 2 # timer


# school network name and password
SSID = 'ITEK 2nd'
PASSWORD = '2nd_Semester_F24v'



""" 
# Connect to mqtt client - Kenneth 10.120.0.87
client = MQTTClient(
    client_id=b'vand_broker',
    server=b'10.120.0.87',
    port=5000,
    keepalive=7200,
    #user=b'',
    #password=b''
)


# Connect to mqtt client - Anders - 10.100.0.97
client = MQTTClient(
    client_id=b'chvoclient',
    server=b'10.100.0.96',
    port=0,
    keepalive=7200,
    #user=b'',
    #password=b''
)
 """



