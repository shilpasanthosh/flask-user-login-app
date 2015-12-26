from passlib.hash import sha256_crypt
from pymongo import MongoClient
password=input("enter the password")
collection=MongoClient()["blog"]["users"]
data=collection.find_one({"username":"amma"})
#for r in data:
 #   print r
if sha256_crypt.verify(password,data['password']):
   print("successful ")
else:
    print("failure")
