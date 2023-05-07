import sys 
import sqlite3
from pymongo import MongoClient 

mongoClient = MongoClient("mongodb://localhost/pokemon")
pokemonDB = mongoClient['pokemondb']
pokemonColl = pokemonDB['pokemon_data']

## Q1: Pikachu
print(" \n Pikachu:")
pikachuResult = pokemonColl.find({"name" : "Pikachu"})
for record in pikachuResult:
    print(record)

## Q2: ATK > 150
print(" \n All pokemon w/ ATK > 150:")
attackResult = pokemonColl.find({"attack" : {"$gt":150}})
for record in attackResult:
    print(record)

## Q3: has Overgrow
print(" \n All pokemon w/ ability Overgrow:")
overgrowResult = pokemonColl.find({"abilities" : {"$regex" : ".*Overgrow.*"}})
for doc in overgrowResult:
    print(doc)