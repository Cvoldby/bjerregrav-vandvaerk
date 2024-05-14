"""
This is mainpage for the display for the water tank

"""

import sys
from flask import Flask, redirect, url_for, render_template, request
#import mariadb
import paho.mqtt.client as mqtt


app = Flask(__name__)


def dbconnect():
    try:
        conn = mariadb.connect(
            user="user1",
            password="password1",
            host="localhost",
            port=3306,
            database = "appusers",
            autocommit = True
        )
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)

    return conn

MQTT_BROKER = "10.120.0.87"
MQTT_PORT = 1883
MQTT_TOPIC = "water_level/#"

def on_message(client, userdata, message):
    app.liquid_level = float(message.payload.decode())


# Set up MQTT client
client = mqtt.Client()
client.on_message = on_message
client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.subscribe(MQTT_TOPIC)
client.loop_start()

# Initial liquid level
app.liquid_level = 0.0

@app.route('/')
def mainpage():
    return render_template('base.html', liquid_level=app.liquid_level)

@app.route('/api/liquid-level')
def get_liquid_level():
    return jsonify({'level': app.liquid_level})

if __name__ == '__main__':
    app.run(debug=True)


