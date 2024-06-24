Individuelle Præsentation
====

# Gruppe præsentation
Vi har lavet en flask web app som bruger interface. Det er herfra brugeren skal kunne vælge, hvilke tider pumpen skal pumpe. Siden giver derfor brugeren information om priser for de givne tidsintervaller. Siden viser også det nuværende vandmængde i tanken. 

Dette gøres gennem MQTT, hvor appen er en subscriber klient. Den subscriber på vandniveauet, som Pico publisher. 

De ønskede pumpetider sendes også via MQTT, hvor appen nu er publisher og Picoen er subscriber. 

De aktuelle elpriser hentes med et database kald til Google VM database. 

De ønskede pumpetider kan både vælges for idag og for i morgen. (Morgendagens elpriser bliver opdateres kl 14).

## Demo
Vi har flask appen kørende på en virtuel maskine på Itek 2nd. Den har ip 10.120.0.21/5000.

## Web scraping vs API
For at skaffe elpriserne har vi både prøvet os frem med python web scraping biblioteker. Dette viste sig dog mere besværligt. Vi fandt et åben og gratis API på elpriserligenu, der nemt og simplet gav den ønskede information.






# Indledende overvejelser
Jeg vil komme først kort komme ind på brugen af API til at skaffe el priser, og derefter vil jeg beskrive, hvordan Flask frameworket er anvendt til at give et GUI. 

# API - Application Programming Interface
En API gør det muligt at interagere med et system - eksempelvis webside med en database. Det er API, der håndterer din forespørgsel/request og giver dig et response. I dette tilfælde vil vi gerne have dagens og morgendagens elpriser. Vi kan gå ind på Nordlys.dk, og aflæse disse, og manuelt skrive dem ind i vores program, men det gider vi ikke. Det er her en API kommer til sin magt.

![alt text](pictures/api.png)

*Beskriv nedenstående kode*

```python
import requests 
#import urequest # for MicroPython

response = requests.get("https://www.elprisenligenu.dk/api/v1/prices/2024/06-22_DK1.json")

print(response.status_code) # print 200 if successfull

for i in response.json():
    print('Tidsinterval:', i['time_start'][11:16], i['time_end'][11:16], 'Pris', i['DKK_per_kWh'], 'oere/kWh')
 
#print(response.status_code)
```

# WSGI Flask framework
Flask er Python Micro framework, der er designet til at lave web applikationer. WSGI står for Web Server Gateway Interface. Flask er kun web app, og bør *ikke* anvendes som web server. Vi har ikke lykkedes at implementere vores flask web app til en web server eller google. En WSGI server er brugt til at køre applikationen - altså HTTP/HTTPS håndtering.

Jeg vil dog gennemgå nogle web appens væsentligste features.

## MQTT kommunikation - vandstand 
Den mest væsentlige feature er, at den aktuelle vandstand præsenteres på siden. Dette gør den som sagt med MQTT.

```python
import paho.mqtt.client as mqtt

# MQTT initiation
MQTT_BROKER = "35.210.127.92" # Google VM
MQTT_PORT = 5000
MQTT_USER = '*'
MQTT_PASSWORD = '*'

MQTT_TOPIC = "waterlevel"
MQTT_PUBLISH_TOPIC = 'pump/timer_today'
#MQTT_PUBLISH_TOPIC2 = "pump/timer_tomorrow" 

def on_message(client, userdata, message):
    app.liquid_level = float(message.payload.decode())

# Set up MQTT client
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
client.on_message = on_message # This call the function when a subscribetion messege is received.
client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.subscribe(MQTT_TOPIC) # subscribe topic
client.loop_start()
```

```python
@app.route('/api/liquid-level')
def get_liquid_level():
    return jsonify({'level': app.liquid_level})
```

```js
<script>
    function updateLevel(level) {
        var liquid = document.getElementById("liquid");
        var levelIndicator = document.querySelector(".level");
        
        //var level = (level*100)
        liquid.style.height = level + "%";
        levelIndicator.style.bottom = level + "%";
        
        document.getElementById("levelValue").innerHTML = level.toFixed(2) + "%";
    }

    // Fetch data from server
    setInterval(function(click_id) {
        fetch('/api/liquid-level')
            .then(response => response.json())
            .then(data => {
                updateLevel(data.level);
            })
            .catch(error => {
                console.error('Error fetching data:', error);
            });
    }, 5000); // Update every 5 seconds
    
</script>	
```


## MQTT - ønskede priser

```python
@app.route('/api/publish_list_today', methods=['POST'])
def publish_list_today():
    msg = request.json.get('message')
    client.publish(MQTT_PUBLISH_TOPIC, msg)
    return jsonify({'status': 'Message sent'})
```


```js
function publishListToday() {
    // code not related to messege    
    var onoffarray = Array.from(pump_map_today.values());
    var msg = onoffarray.toString();
    
    fetch('/api/publish_list_today', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message: msg })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data.status);
    })
    .catch(error => {
        console.error('Error publishing message:', error);
    });
}
```


## Hvad har jeg lært
Gennem projektet har jeg lært at arbejde med MQTT. Jeg har både arbejde med MQTT på web app og på MicroControlleren.

Derudover har jeg både prøvet at arbejde med API og webscraping python libraries. Jeg har læst om hvordan en API fungerer.

Jeg har fået et rimelig godt indblik i Flask som web app/framework.

Derudover har jeg arbejdet med JavaScript til web appen for at prøve et nyt programmeringssprog. Jeg er ikke blevet ekspert, men jeg har kradset lidt i overfladen af JavaScript.

Trods det ikke er endeligt lykkedes, så har jeg læst meget omkring Google Cloud Run og Google App Engine samt Self-Hosted muligheder som Gunicorn.

