Webserver
====

Til at opsætte en webside er Flask valgt som webframe. Formålet med webserveren er at kunne display data fra databasen og til det kræves blot en simpel webside, hvor til Flask er ideelt. Webserveren henter elpriser fra databasen og subscriber på vandniveauet hos MQTT brokeren. 

## Module Design
Flask webserver lægger på en Ubuntu server på VMware Workstation. På Ubuntu serveren initieres et virtual environment. I dette *venv* installeres *flask*. Her dannes følgende mappe struktur.

water-webserver
- venv
- templates
- - today.html
- - tomorrow.html
- - about.html
- - base.html
- - login.html
- static
- - style.css
- water.py
- login.py
- pyproject.toml

Filen water.py indeholder selve applikationen. Filen login.py er til fremtidig udvikling og mere nice-to-have end need-to-have. Filen style.css indeholder diverse css objekter, der anvendes til at give webpagen udseende. 

Websiden indeholder følgende funktioner - det er de funktionskritiske implementationer, der oplyser opgavens krav:
- Modtage data fra pico
- Tilgå DB og hente data
- Sende besked til Pico om hvornår der skal pumpes

Da morgendagens elpriser bliver offentliggjort kl. 13 dagen inden, er applikationen sat op til både at kunne håndtere timeintervallerne for i dag og i morgen.

## Module Implementation
Til implementeringen af Flask framework er der som beskrevet i design både skrevet .html, .py, og .css filer. De væsentligste implementationselementer ligger i water.py filen. Der er også skrevet nogle scripts i JavaScript i nogle af .html filerne. Her er blandt andet håndteret nogle api kald til applikationen.

### MQTT Client - Subscriber
MQTT Brokeren er opsat på Google Cloud. For at applikationen kan til tilgå Brokeren skal MQTT klienten initieres. Applikationen gøre brug af Eclipse Paho MQTT Client. Dette ses herunder.

```python
import paho.mqtt.client as mqtt
# MQTT initiation
#MQTT_BROKER = "10.100.0.96" # Anders' broker
#MQTT_PORT = 1883
MQTT_BROKER = "35.210.127.92" # Kenneths broker
MQTT_PORT = 5000 

def on_message(client, userdata, message):
    app.liquid_level = float(message.payload.decode())

# Set up MQTT client
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
client.on_message = on_message
client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.subscribe(MQTT_TOPIC)
client.loop_start() # start loop
```
Heraf ses *on_message* funktionen, der opdaterer app.liquid_level, der modtager en besked på MQTT topic waterlevel. Denne funktion sat til klientens callback i linjen - *client.on_message = on_message*.

Dette bruger applikationen til at sende til websiden.
```python
@app.route('/api/liquid-level')
def get_liquid_level():
    return jsonify({'level': app.liquid_level})
```
Denne funktion ser måske ikke ud af meget, men i sammenhæng med klientens *on_message* callback funktion opdates vandniveauet i tanken, når klienten modtager beskeder og *get_liquid_level* sender dette vandniveau til websiden.

```js
function updateLevel(level) {
    var liquid = document.getElementById("liquid");
    var levelIndicator = document.querySelector(".level");
    //var level = (level*100) // If send data has been divided by 100

    liquid.style.height = level + "%";
    levelIndicator.style.bottom = level + "%";
    document.getElementById("levelValue").innerHTML = level.toFixed(2) + "%";
}

// Fetch data from server
setInterval(function(click_id) {
    fetch('/api/liquid-level') // call get_liquid_level()
        .then(response => response.json())
        .then(data => {
            updateLevel(data.level);
        })
        .catch(error => {
            console.error('Error fetching data:', error);
        });
}, 2000); // Update every 2 seconds
```
Her ses scriptet i base.html, der kalder get_liquid_level funktionen. Scriptet er sat til at lave api kaldet hver andet sekund. Scriptet er opdelt i funktionen *updateLevel* og setInterval delen. I setInterval kaldes '/api/liquid-level', der henter liquid_level fra ovenstående funktion, hvorefter denne data bliver indsat som parameter i *updateLevel* funktionen.

For at modtage de 'korrekte' pakker, og håndtere disse efter hensigten om at give et visuelt element til websiden, er der anvendt MQTTBox. Her er der både publiceret genereret data, for at teste håndteringen, og testet med publiceret data fra Picoen.

### MQTT Client - Publisher
Webserveren er ikke alene subscriber - den er også publisher. Som beskrevet kan der både publiceres pumpetidsintervaller for i dag og i morgen. Dette gør i to forskellige funktioner. Herunder ses funktionen for at publicere pumpeplanen for i dag.
```python
@app.route('/api/publish_list_today', methods=['POST'])
def publish_list_today():
    msg = request.json.get('message') # request til websiden
    client.publish(MQTT_PUBLISH_TOPIC, msg)
    return jsonify({'status': 'Message sent'})
```
Her er der en *request* til websiden, der poster en liste med 24 elementer af henholdsvis 0(slukket) og 1(tændt). Derefter publiceret denne liste til MQTT Brokeren.

```js
function publishListToday() {
    var onoffarray = Array.from(pump_map_today.values());
    //var onoffarray = Array.from(pump_map_tomorrow.values());
    var msg = onoffarray.toString(); // the message string 
    
    fetch('/api/publish_list_today', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message: msg }) // the message in the data
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
Her kan det ses hvordan besked først konverteres til en string. Også her anvendes et api kald til *publish_list_today* funktionen. Det noteres, at besked bliver postet med key *message*, hvilket er den *publish_list_today* funktionen kalder *get* på. Denne process er ligeledes anvendt til at sende pumpetimeplanen for i morgen. Disse er publiceret på to forskellige topics til MQTT brokeren - pump/timer_today og pump/timer_tomorrow. Det er gjort for nemmere at adskille dataen på Pico siden.

### Database call
For at brugeren kan træffe beslutninger på et oplyst, opdateret grundlag, giver websiden muligheden for at se dagens elpriser (og morgendagens priser efter kl. 14). Til dette skal vi tilgå vores database der ligesom MQTT brokeren ligger i Google Cloud.

```python
import mariadb

def dbconnect():
    """Establish mariadb connection"""
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
```
Her er funktionen der etablerer forbindelsen til mariadb serveren. Denne funktion anvendes til hente elpriserne fra databasen.

```python
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
```

Denne funktioner gør brug af *dbconnect* funktionen. Herefter eksekverer den en SELECT statement, der henter dagens elpriser. Disse priser virker ligesom med MQTT api kaldene ved at '/api/get_prices_today' bliver kaldt og priserne bliver vist på websiden. 

## Formal Module test
Gennem udviklingen af webserveren har der været adskillige versioner.
Som beskrevet har de mest systemkritiske test handlet om håndtering af MQTT Client subscribe/publish og database forbindelse - især i forbindelse med at have både MQTT Broker og databasen i Google Cloud. 

Når man kommer ind på websiden bliver du mødt af følgende side.





