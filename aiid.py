from pymongo import MongoClient
# import pymongoarrow.api as pma
from dotenv import load_dotenv
import os
import csv

load_dotenv()
URI = os.getenv("URI")

def write_to_csv(collection):
   if collection.count_documents({}) == 0:
      return 
   #make API call to the MongoServer
   mongo_docs = collection.find()

   fieldnames = set()
   for doc in mongo_docs:
      for key in doc.keys():
         fieldnames.add(key)
   # fieldnames = list(mongo_docs[0].keys())
   fieldnames.remove('_id')

   mongo_docs.rewind()
   
   #compute output file directory and name
   output_dir = os.path.join("./views")
   output_file = os.path.join(output_dir, collection.name+"_view"+".csv")
   with open(output_file, "w", newline="") as csvfile:
      writer = csv.DictWriter(csvfile,fieldnames=fieldnames,extrasaction="ignore", escapechar='\\')
      writer.writeheader()
      writer.writerows(mongo_docs)

def get_database():
 
   # Provide the mongodb atlas url to connect python to mongodb using pymongo
   CONNECTION_STRING = URI + "/aiidprod"
 
   # Create a connection using MongoClient
   client = MongoClient(CONNECTION_STRING)

   db = client.get_database("aiidprod")

   return db

def show_collection(db, collection_name):

   docList = list(db.get_collection(collection_name).find({}))
   print(docList[0])

# This is added so that many files can reuse the function get_database()
if __name__ == "__main__":   
  
   # Get the database
   db = get_database()
   collection_names = list(db.list_collection_names()) # list all collections
   print("collection_names",collection_names)

   for cname in collection_names:
      write_to_csv(db.get_collection(cname))

   
