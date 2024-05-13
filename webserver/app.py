from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello():
    
    html = open('temlplates/base', 'r').readlines()
    return html

