'''
Joyce Wu & Queenie Xiang
Softdev2 pd7 
K05 -- Import/Export Bank
2018-02-26
'''

'''
Dataset: Record of Earth Meteorite Landings
Description: Contains information about location, date, name, mass, and unique id of each meteorite
Download hyperlink: https://data.nasa.gov/resource/y77d-th95.json
Import: We opened the url to retrieve data and imported as json. write_json writes the json object into meteorites.json file
'''

from pymongo import MongoClient
import urllib2, json

data = {} 
c = MongoClient('lisa.stuy.edu')
mfDB = c.chobani_flips
collie = mfDB.meteorites

def import_info():
    url = "https://data.nasa.gov/resource/y77d-th95.json"
    resp = urllib2.urlopen(url)
    data = json.loads(resp.read())
    return data

def write_json(data):
    f = open("meteorites.json", "w+")
    f.write(str(data))
    f.close()

#retrieve data and insert into database and imported into json file
data = import_info()
#write_json(data)
collie.drop()
collie.insert_many(data)

#parses through collection to convert all masses to floats from strings
def convert(collie):
    #finds all landings with field mass
    landings = collie.find()
    for l in landings:
        print l
	try:
             l["mass"] = float(l["mass"])
             collie.save(l)
        except:
             print "no mass"
    return collie
#convert()

#retrieves all meteorite landings with mass less than n  
def mass(n, collie):
    landings = collie.find({"mass": {"$lt": n}})
    #for l in landings:
        #print l
    return landings

#retrieves all meteorite landings with that recclass
def recclass(recclass):
    landings = collie.find({"recclass": str(recclass)})
    for l in landings:
        print l

#retrieves all meteorite landings with names that start with 'letter'
#and have a mass less than 'mass' 
def name_mass(letter, mass):
    landings = collie.find({"mass": {"$lt": mass}})
    d = {}; 
    for l in landings:
        if l["name"][0].lower() == letter:
            d[l["name"]] = l["mass"]
    for meteorite in d:
        print meteorite + ": " + str(d[meteorite]) 
    


#retrieves meteorite landings with mass between mass1 and mass2
def between_masses(mass1, mass2):
    if mass1 > mass2:
        max_val = mass1
        min_val = mass2
    else:
        max_val = mass2
        min_val = mass1 
        
    landings = collie.find({"mass": {"$lt": max_val}})
    for l in landings:
        if l["mass"] > min_val: 
            print l


#retrieves meteorite landings with a given year 
def date_range(y):

    landings = collie.find() 
    
    for l in landings:
        try: 
            if l["year"][0:4] == str(y):
                print l

        except:
            print ""

                               
    
#TESTING
#recclass("L5")
#mass(2000)
#name_mass("a", 2000)
#between_masses(300, 400)
#date_range(1950)
