import psycopg2
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())

db = psycopg2.connect(dbname=os.getenv("DBNAME"), user=os.getenv("DBUSER"), password=os.getenv("DBPASSWORD"))
