from flask import Flask, request, redirect, url_for, render_template, flash
from flask_pymongo import PyMongo
from routes import app

if __name__ == "__main__":
    app.run(debug=True)
