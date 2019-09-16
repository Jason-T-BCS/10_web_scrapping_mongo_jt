from bs4 import BeautifulSoup
import urllib.request
from splinter import Browser
import pandas as pd
import requests


def init_browser():
#path to chromedriver
    executable_path = {'executable_path':'/usr/local/bin/chromedriver'}
    return Browser('chrome', **executable_path, headless=False)

#create mars dict
mars_info = {}

### NASA Mars News
def scrape_mars_news():
    try:
        browser = init_browser()

        #link to website
        the_url = 'https://mars.nasa.gov/news/'

        #browser to open link
        browser.visit(the_url)

        #html object
        the_page = browser.html

        #parse
        soup = BeautifulSoup(the_page,'html.parser')

        #find element
        news_title = soup.find('div', class_='content_title').find('a').text
        news_p = soup.find('div', class_='article_teaser_body').text

        #add to mars dict
        mars_info['news_title'] = news_title
        mars_info['news_paragraph']= news_p

        return mars_info

    finally:
        #quit browser
        browser.quit()


###JPL Mars Space Images - Featured Image
def scrape_img():
    try:
        browser = init_browser()
        the_url2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
        browser.visit(the_url2)
        the_page2 = browser.html
        soup = BeautifulSoup(the_page2,'html.parser')
        img_url = soup.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]
        img_url
        base_url = 'https://www.jpl.nasa.gov'
        featured_img_url = base_url + img_url
        mars_info['featured_img_url'] = featured_img_url

        return mars_info
    finally:
        #quit browser
        browser.quit()

### Mars Weather
def scrape_mars_weather():
    try:
        browser = init_browser()
        weather_url = 'https://twitter.com/marswxreport?lang=en'
        browser.visit(weather_url)
        html_weather = browser.html
        soup = BeautifulSoup(html_weather, 'html.parser')
        latest_tweets = soup.find_all('div', class_='js-tweet-text-container')

        for tweet in latest_tweets:
            weather_tweet = tweet.find('p').text
            if 'Sol' and 'pressure' in weather_tweet:
                print(weather_tweet)
                break
            else:
                pass

        mars_info['weather_tweet'] = weather_tweet

        return mars_info
    finally:
        #quit browser
        browser.quit()

###Mars Facts
def scrape_facts():

    facts_url = 'http://space-facts.com/mars/'
    mars_facts = pd.read_html(facts_url)
    mars_df = mars_facts[1]
    mars_df.columns = ['Description','Value']
    mars_df.set_index('Description', inplace=True)
    mars_data = mars_df.to_html()
    mars_info['mars_facts'] = mars_data

    return mars_info

###Mars Hemispheres
def scrape_hemis():
    try:
        browser = init_browser()
        hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(hemispheres_url)
        html_hemispheres = browser.html
        soup = BeautifulSoup(html_hemispheres, 'html.parser')
        items = soup.find_all('div', class_='item')
        hemisphere_image_urls = []
        base_url = 'https://astrogeology.usgs.gov'

        for i in items:
            title = i.find('h3').text
            img_url = i.find('a', class_='itemLink product-item')['href']
            browser.visit(base_url + img_url)
            img_html = browser.html
            soup = BeautifulSoup(img_html, 'html.parser')
            img_url = base_url + soup.find('img', class_='wide-image')['src']
            hemisphere_image_urls.append({"title" : title, "img_url" : img_url})
            mars_info['hemisphere_img_urls'] = hemisphere_image_urls
            
        return mars_info
    finally:
        #quit browser
        browser.quit()
