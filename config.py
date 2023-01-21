import pymongo
import certifi

connection_str = "mongodb+srv://FSDI:Test1234@cluster0.w4dponr.mongodb.net/?retryWrites=true&w=majority"

client = pymongo.MongoClient(connection_str, tlsCAFile=certifi.where() )
db = client.get_database("OnlineStore")