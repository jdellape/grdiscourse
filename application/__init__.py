from flask import Flask
from config import Config
from pymongo import MongoClient
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

client = MongoClient(Config.DB_URI)
db = client.get_database('grdiscourse')

from application import routes
from application import models