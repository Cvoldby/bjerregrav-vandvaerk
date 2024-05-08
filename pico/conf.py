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

Kritisk_vandniveau = 1 # liter

minimumsboringstid = 2 # timer


# school network name and password
SSID = 'ITEK 2nd'
PASSWORD = '2nd_Semester_F24v'



