#!/usr/bin/env python
# coding: utf-8

from flask import Flask, render_template
import pymongo
import scrape_mars
import os

# create instance of Flask app
app = Flask(__name__)

# create mongo connection
client = pymongo.MongoClient()
db = client.mars_db
collection = db.mars_info

@app.route("/")
def home():

    mars_info = mongo.db.mars_info.find_one()
    return render_template("index.html", mars_info=mars_info)

@app.route("/scrape")
def scrape():
    
    mars_info = mongo.db.mars_db
    mars_data = scrape_mars.scrape_mars_news()
    mars_data = scrape_mars.scrape_img()
    mars_data = scrape_mars.scrape_mars_weather()
    mars_data = scrape_mars.scrape_facts()
    mars_data = scrape_mars.scrape_hemis()
    mars_info.update({}, mars_data, upsert=True)

if __name__ == "__main__":
    app.run(debug=False)
