from flask import Flask, render_template, url_for



@app.route('/today')
def today():
    return render_template('today.html')


@app.route('/tomorrow')
def tomorrow():
    return render_template('tomorrow.html')