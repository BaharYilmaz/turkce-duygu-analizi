from pymongo import MongoClient
client = MongoClient()

client = MongoClient('mongodb://127.0.0.1:27017/?compressors=disabled&gssapiServiceName=mongodb')
db = client.['userDb']
collection = db['user']

#mongodb://127.0.0.1:27017/?compressors=disabled&gssapiServiceName=mongodb
