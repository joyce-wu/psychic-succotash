'''
Joyce Wu & Queenie xiang
SoftDev2 pd7
K04 -- Mi only nyam ital food, mon!
2018-02-14
'''

from pymongo import MongoClient

c = MongoClient('lisa.stuy.edu')
mfDB = c.test
collec = mfDB.restaurants

def borough(boro):
    restaurants = collec.find({"borough": boro})
    for r in restaurants:
        print r

def zip_code(zip):
    restaurants = collec.find({"address.zipcode": str(zip)})
    for r in restaurants:
        print r

def zip_grade(zip, grade):
    restaurants = collec.find( { '$and': [{"address.zipcode":str(zip)}, {"grades.grade":grade}]})
    for r in restaurants:
        print r

def zip_score(zip, score):
    restaurants = collec.find({'$and':[{"address.zipcode":str(zip)}, {"grades.score": {'$lt': score}}]})
    for r in restaurants:
        print r

def cuisine_grade(cuisine, grade):
    restaurants = collec.find({'$and': [{"cuisine": cuisine}, {"grades.grade": grade}]})
    for r in restaurants:
        print r

                            
#borough("Manhattan")
#zip_code(10025)
#zip_grade(10025, 'A')
#zip_score(10025, 13)
cuisine_grade("American", 'A')
