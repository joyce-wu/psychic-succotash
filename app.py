from flask import Flask, render_template, request
import meteorites
import os
from pymongo import MongoClient
import urllib2, json

app = Flask(__name__)
app.secret_key = os.urandom(32)
data = {}
c = MongoClient('lisa.stuy.edu')
mfDB = c.chobani_flips
collie = mfDB.meteorites

@app.route("/")
def start():
    global collie
    collie.drop()
    global data
    data = meteorites.import_info()
    collie.insert_many(data)
    collie = meteorites.convert(collie)
    return render_template("welcome.html")

@app.route("/mass")
def mass():
    m = float(request.args["mass"])
    landings = meteorites.mass(m, collie)
    for l in landings:
        print l
        global data
        data[l["name"]] = l["mass"]
             
    return render_template("results.html", title="masses", result=data, m = m)

if __name__ == "__main__":
    app.debug = True

app.run()
