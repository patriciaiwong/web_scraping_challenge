# Dependencies
import requests
import pymongo
from splinter import Browser
from bs4 import BeautifulSoup
import os
import pandas as pd
import time

def init_browser():
    # Capture path to Chrome Driver & Initialize browser
    executable_path = {'executable_path':"C:\Drivers\chromedriver\chromedriver.exe"}
    browser = Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()
    mars_facts_data = {}

url = 'https://mars.nasa.gov/news/'
browser.visit(url)

# Retrieve page with the requests module
response = requests.get(url)
# Create BeautifulSoup object; parse with 'html'
soup = BeautifulSoup(response.text, 'html')

# Iterate through all pages
nt=[]
for x in range(50):
    # HTML object
    html = browser.html
    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')
    # Retrieve all elements that contain article information
    news_articles = soup.find_all('div', class_='slide')


    # Iterate through each article
    for article in news_articles:
        # Use Beautiful Soup's find() method to navigate and retrieve attributes
        #nt: news title
        nt = article.find('div', class_='content_title')
        title= nt.find('a').text
        #np:news paragraph
        np= article.find('div', class_='image_and_description_container')
        paragraph= np.find('div', class_='rollover_description_inner').text

        print('-----------')
        print(title)
        print(paragraph)


    # Click the 'Next' button on each page
    try:
        browser.click_link_by_partial_text('next')
          
    except:
        print("Scraping Complete")

featured_image_url='https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(featured_image_url)

#Getting the base url
from urllib.parse import urlsplit
base_url = "{0.scheme}://{0.netloc}/".format(urlsplit(featured_image_url))
print(base_url)

#Design an xpath selector to grab the image
xpath = "//*[@id=\"page\"]/section[3]/div/ul/li[1]/a/div/div[2]/img"

#Use splinter to click on the mars featured image
#to bring the full resolution image
results = browser.find_by_xpath(xpath)
img = results[0]
img.click()

#get image url using BeautifulSoup
html_image = browser.html
soup = BeautifulSoup(html_image, "html.parser")
img_url = soup.find("img", class_="fancybox-image")["src"]
full_img_url = base_url + img_url
print(full_img_url)

#Mars Facts

url_mars_facts = "https://space-facts.com/mars/"
mars_table = pd.read_html(url_mars_facts)
mars_table[0]

mars_df = mars_table[0]
mars_df.columns = ["Parameter", "Values"]
mars_df.set_index(["Parameter"])

mars_html = mars_df.to_html()
mars_html = mars_html.replace("\n", "")
mars_html

url_hemisphere = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
browser.visit(url_hemisphere)

#Get base url
hemisphere_base_url = "{0.scheme}://{0.netloc}/".format(urlsplit(url_hemisphere))
print(hemisphere_base_url)