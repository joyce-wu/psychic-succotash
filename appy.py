from flask import Flask, render_template, request
import meteorites
import os
from pymongo import MongoClient
import urllib2, json
import ssl

print(ssl.OPENSSL_VERSION)

app = Flask(__name__)
app.secret_key = os.urandom(32)
data = {}
c = MongoClient('lisa.stuy.edu')
mfDB = c.chobani_flips
collie = mfDB.meteorites

@app.route("/")
def start():
    collie.drop()
    data = meteorites.import_info()
    collie.insert_many(data)
    meteorites.convert()
    return render_template("welcome.html")

@app.route("/mass")
def mass():
    m = float(request.args["mass"])
    landings = meteorites.mass(m, collie)
    print m
    print landings
    return render_template("results.html", title="masses", result=landings)

if __name__ == "__main__":
    app.debug = True

app.run()
