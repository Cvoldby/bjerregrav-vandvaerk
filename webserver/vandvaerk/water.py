"""
This is mainpage for the display for the water tank

"""

import sys
from datetime import datetime, timedelta

from flask import Flask, redirect, url_for, render_template, request, jsonify
import mariadb
import paho.mqtt.client as mqtt


app = Flask(__name__)


def dbconnect():
    try:
        conn = mariadb.connect(
            user="webserver",
            password="Case5",
            host="35.210.127.92",
            port=3306,
            database="vandvaerk",
            autocommit=True
        )
        cur = conn.cursor()
        return cur
    except mariadb.Error as e:
        print(e)
        

# MQTT initiation
#MQTT_BROKER = "10.100.0.96"
#MQTT_PORT = 1883
MQTT_BROKER = "35.210.127.92"
MQTT_PORT = 5000
MQTT_USER = 'database'
MQTT_PASSWORD = 'FegZUO'

MQTT_TOPIC = "waterlevel"
MQTT_PUBLISH_TOPIC = 'pump/timer_today'
MQTT_PUBLISH_TOPIC2 = "pump/timer_tomorrow" 


def on_message(client, userdata, message):
    app.liquid_level = float(message.payload.decode())


# Set up MQTT client
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
client.on_message = on_message
client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.subscribe(MQTT_TOPIC)
client.loop_start()



# Initial liquid level
def initialize_var():
    """This is a function for initiating the variables"""
    app.liquid_level = 0.0

    dato_today = [datetime.now().strftime("%Y-%m-%d")]
    dato_tomorrow = [(datetime.now()+timedelta(1)).strftime("%Y-%m-%d")]

    cur = dbconnect()
    # prices today
    cur.execute(
        "SELECT * FROM vandvaerk.elPriser WHERE dato=?;", dato_today
    )
    prices = cur.fetchall()
    
    try: # catch if prices not yet in database
        prices_list = [float(x) for x in list(prices[0][1:])]
    except IndexError:
        prices_list = [0.0 for _ in range(24)]
    app.pricelist_today = prices_list
    
    # prices tomorrow
    cur.execute(
        "SELECT * FROM vandvaerk.elPriser WHERE dato=?;", dato_tomorrow
    )
    prices = cur.fetchall()
    
    try: # catch if prices not yet in database
        prices_list = [float(x) for x in list(prices[0][1:])]
        print('success db')
    except IndexError:
        prices_list = [0.0 for _ in range(24)]
        print("fail db")
    
    app.pricelist_tomorrow = prices_list
    
    # close db connection
    cur.close()
    
initialize_var()

@app.route('/')
def mainpage():
    return render_template('about.html', liquid_level=app.liquid_level) 


@app.route('/today')
def today():
    return render_template('today.html', liquid_level=app.liquid_level, pricelist=app.pricelist_today)


@app.route('/tomorrow')
def tomorrow():
    return render_template('tomorrow.html', liquid_level=app.liquid_level, pricelist=app.pricelist_tomorrow)


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/api/liquid-level')
def get_liquid_level():
    return jsonify({'level': app.liquid_level})
    
    
@app.route('/api/publish', methods=['POST'])
def publish_on():
    msg = request.json.get('message')
    client.publish(MQTT_PUBLISH_TOPIC, msg)
    return jsonify({'status': 'Message sent'})
    

@app.route('/api/publish_list_today', methods=['POST'])
def publish_list_today():
    msg = request.json.get('message')
    client.publish(MQTT_PUBLISH_TOPIC, msg)
    return jsonify({'status': 'Message sent'})
    
@app.route('/api/publish_list_tomorrow', methods=['POST'])
def publish_list_tomorrow():
    msg = request.json.get('message')
    client.publish(MQTT_PUBLISH_TOPIC2, msg)
    return jsonify({'status': 'Message sent'})


@app.route('/api/get_prices_today')
def get_prices_today():
    dato = datetime.now().strftime("%Y-%m-%d")
    cur = dbconnect()
    cur.execute(
        "SELECT * FROM vandvaerk.elPriser WHERE dato=?;", dato
    )
    prices = cur.fetchall()
    cur.close()
    prices_list = [float(x) for x in list(prices[1][1:])]
    prices_date = prices[0][0]
    
    return jsonify({'date': prices_date, 'prices': prices_list})
    
    
@app.route('/api/get_prices_tomorrow')
def get_prices_tomorrow():
    dato = datetime.now()+timedelta(1).strftime("%Y-%m-%d")
    cur = dbconnect()
    cur.execute(
        "SELECT * FROM vandvaerk.elPriser WHERE dato=?;", dato
    )
    prices = cur.fetchall()
    cur.close()
    prices_list = [float(x) for x in list(prices[1][1:])]
    prices_date = prices[0][0]
    
    return jsonify({'date': prices_date, 'prices': prices_list})

  
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0') #port=8989


