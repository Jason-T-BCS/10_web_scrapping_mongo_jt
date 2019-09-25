from bs4 import BeautifulSoup
import urllib.request
from splinter import Browser
import pandas as pd
import requests

def init_browser():
    exec_path = {'executable_path': '/app/.chromedriver/bin/chromedriver'}
    return Browser('chrome', headless=True, **exec_path)

#dictionary
mars_info = {}

# News
def scrape_mars_news():
    try:
        browser = init_browser()
        url = 'https://mars.nasa.gov/news/'
        browser.visit(url)

        # HTML Object
        html = browser.html

        # Parse HTML
        soup = BeautifulSoup(html, 'html.parser')

        # Retrieve
        news_title = soup.find('div', class_='content_title').find('a').text
        news_p = soup.find('div', class_='article_teaser_body').text

        # Dictionary entry
        mars_info['news_title'] = news_title
        mars_info['news_paragraph'] = news_p

        return mars_info

    finally:
        browser.quit()

# Images
def scrape_mars_image():

    try:
        browser = init_browser()
        image_url_featured = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
        browser.visit(image_url_featured)

        # HTML Object
        html_image = browser.html

        # Parse HTML
        soup = BeautifulSoup(html_image, 'html.parser')

        # Retrieve image url
        featured_image_url  = soup.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]

        # Base Url
        main_url = 'https://www.jpl.nasa.gov'

        # full image url
        featured_image_url = main_url + featured_image_url
        featured_image_url

        # Dictionary entry
        mars_info['featured_image_url'] = featured_image_url
        
        return mars_info
        
    finally:
        browser.quit()

        

# Mars Weather
def scrape_mars_weather():

    try:
        browser = init_browser()
        weather_url = 'https://twitter.com/marswxreport?lang=en'
        browser.visit(weather_url)

        # HTML Object
        html_weather = browser.html

        # Parse HTML
        soup = BeautifulSoup(html_weather, 'html.parser')

        # Find tweets
        latest_tweets = soup.find_all('div', class_='js-tweet-text-container')

        for tweet in latest_tweets:
            weather_tweet = tweet.find('p').text
            if 'Sol' and 'pressure' in weather_tweet:
                print(weather_tweet)
                break
            else:
                pass

        # Dictionary entry
        mars_info['weather_tweet'] = weather_tweet
        
        return mars_info
        
    finally:
        browser.quit()


# Mars Facts
def scrape_mars_facts():

    facts_url = 'http://space-facts.com/mars/'

    #read_html to parse url
    mars_facts = pd.read_html(facts_url)
    
    #create df
    mars_df = mars_facts[1]
    
    #name columns
    mars_df.columns = ['Description','Value']

    #set index
    mars_df.set_index('Description', inplace=True)

    #save html
    data = mars_df.to_html()

    #dictionary entry
    mars_info['mars_facts'] = data

    return mars_info

def scrape_mars_hemispheres():

    try:
        browser = init_browser()
        hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(hemispheres_url)

        #HTML Object
        html_hemispheres = browser.html

        #Parse HTML
        soup = BeautifulSoup(html_hemispheres, 'html.parser')

        #find
        items = soup.find_all('div', class_='item')

        #create list
        img_urls = []

        #main url
        hemispheres_main_url = 'https://astrogeology.usgs.gov'

        for i in items:
            #find img url
            title = i.find('h3').text
            partial_img_url = i.find('a', class_='itemLink product-item')['href']
            browser.visit(hemispheres_main_url + partial_img_url)
            
            #HTML Object
            partial_img_html = browser.html
            
            #Parse HTML
            soup = BeautifulSoup( partial_img_html, 'html.parser')
            
            #Retrieve full image
            img_url = hemispheres_main_url + soup.find('img', class_='wide-image')['src']
            
            #Dictionary entry
            img_urls.append({"title" : title, "img_url" : img_url})

        mars_info['img_urls'] = img_urls

        return mars_info
        
    finally:
        browser.quit()
