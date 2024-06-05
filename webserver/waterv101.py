"""
This is mainpage for the display for the water tank

"""

import sys
from flask import Flask, redirect, url_for, render_template, request, jsonify
#import mariadb
import paho.mqtt.client as mqtt


app = Flask(__name__)

# Database initiation
#from flask_mysqldb import MySQL 
  
#app.config['MYSQL_HOST'] = '35.210.127.92'
#app.config['MYSQL_USER'] = 'admin'
#app.config['MYSQL_PASSWORD'] = 'admin' 
#app.config['MYSQL_DB'] = 'vandvaerk'
  
#mysql = MySQL(app)


from flask_sqlalchemy import SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://admin:admin@172.16.1.100/vandvaerk'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Prices(db.Model):
    #id = db.Column(db.Integer, primary_key=True)
    dato = db.Column(db.Date, nullable=False)
    elpris1 = db.Column(db.Decimal(10,3), nullable=False)
    
    

# MQTT initiation
#MQTT_BROKER = "10.100.0.96"
#MQTT_PORT = 1883
MQTT_BROKER = "35.210.127.92"
MQTT_PORT = 5000
MQTT_USER = 'database'
MQTT_PASSWORD = 'FegZUO'

MQTT_TOPIC = "waterlevel"
MQTT_PUBLISH_TOPIC = 'pump/status'
MQTT_PUBLISH_TOPIC2 = "pump/timer" 


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
app.liquid_level = 0.0
app.prices = [0,1,2,3,4,5,6,7,8,9]


@app.route('/')
def mainpage():
    return render_template('base.html', liquid_level=app.liquid_level, prices=app.prices)


@app.route('/api/liquid-level')
def get_liquid_level():
    return jsonify({'level': app.liquid_level})
    
    
@app.route('/api/publish', methods=['POST'])
def publish_on():
    msg = request.json.get('message')
    client.publish(MQTT_PUBLISH_TOPIC, msg)
    return jsonify({'status': 'Message sent'})
    

@app.route('/api/publish_list', methods=['POST'])
def publish_list():
    msg = request.json.get('message')
    client.publish(MQTT_PUBLISH_TOPIC2, msg)
    return jsonify({'status': 'Message sent'})


@app.route('/api/prices')
def get_prices():
    cur = dbconnect()
    cur.execute(
        "SELECT * FROM elpriser ORDER BY id DESC LIMIT 1;"
    )
    prices = cur.fetchall()
    cur.close()
    
    return jsonify({'prices': app.prices})
    
  
if __name__ == '__main__':
    app.run(debug=True)


