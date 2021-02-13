from flask import Flask
from config import Config
from pymongo import MongoClient
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

#Establish connection to Mongo, load db object then close connection
client = MongoClient(Config.DB_URI, connect=False, maxIdleTimeMS=600000)
db = client.get_database('grdiscourse')
client.close()

from application import routes
from application import models