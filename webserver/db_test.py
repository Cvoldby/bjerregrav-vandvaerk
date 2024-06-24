import mariadb
from flask import jsonify, Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('base.html')

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


cur = dbconnect()
dato = ['2024-06-06']
print(dato)
print(list(dato))
cur.execute("SELECT * FROM vandvaerk.elPriser WHERE dato=?;", dato)# WHERE dato='2024-05-30
prices = cur.fetchall()

price_date, price_int = prices[0][0],[float(x) for x in list(prices[0][1:])]
print(price_date, price_int)
price_dict = [{'price'+str(idx):price} for idx, price in enumerate(price_int)]

#print(price_dict)
#jsonify(price_dict)


cur.close()

import datetime

print([(datetime.datetime.now()+datetime.timedelta(1)).strftime("%Y-%m-%d")])