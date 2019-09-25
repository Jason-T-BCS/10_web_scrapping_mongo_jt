from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars
import os

# create instance of Flask app
app = Flask(__name__)

# create mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_db")

@app.route("/")
def home():
    mars_info = mongo.db.mars_info.find_one()
    return render_template("index.html", mars_info=mars_info)

@app.route("/scrape")
def scrape():
    mars_info = mongo.db.mars_info
    mars_info = scrape_mars.scrape()
    mars_data = scrape_mars.scrape_mars_news()
    mars_data = scrape_mars.scrape_mars_image()
    mars_data = scrape_mars.scrape_mars_facts()
    mars_data = scrape_mars.scrape_mars_weather()
    mars_data = scrape_mars.scrape_mars_hemispheres()
    mars_info.update({}, mars_data, upsert=True)
    
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=False)
