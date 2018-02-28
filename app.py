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

#Grabs all meteorites under a given mass 
@app.route("/mass")
def mass():
    d = {}
    
    #Converts mass to a float 
    m = float(request.args["mass"])

    #Grabs all info from the DB 
    landings = meteorites.mass(m, collie)
    
    for l in landings:
        #print l["name"] 
        d[l["name"]] = l["mass"]
             
    return render_template("results.html", title="masses", result=d, m=m)

#Grabs all meteorites that start with a given letter and are under a given mass
@app.route("/letter_mass")
def letter():
    d = {} 
    letter = request.args["letter"].lower()
    mass = float(request.args["mass"])
    #print letter
    #print mass
    d = meteorites.name_mass(letter, mass, collie)
    
    #for l in d:
        #print l
        #print d[l]
        
    return render_template("letter.html", title="meteorites", result=d, l=letter, m=mass)
                    
        
if __name__ == "__main__":
    app.debug = True

app.run()
