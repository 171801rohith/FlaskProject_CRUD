from flask import Flask, session
from datetime import timedelta
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/FlaskProject"
app.secret_key = "8f3a7d9b2c6e4f1a9b3c8d7e6f5a4b2c1d0e9f8a7c6b5d4e3f2a1b0c9d8e7f6g"
app.permanent_session_lifetime = timedelta(minutes=30)
mongodb = PyMongo(app).db
