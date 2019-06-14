import requests
from bs4 import BeautifulSoup
import sqlite3
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

conn = sqlite3.connect('feeds.db')

c = conn.cursor()

# Create tables
c.execute('''CREATE TABLE IF NOT EXISTS instagram_urls (url text)''')
c.execute('''CREATE TABLE IF NOT EXISTS insta_photo_urls (url text)''')

c.execute('SELECT * FROM instagram_urls')
#twitter_urls = c.fetchall()
instagram_urls = ['https://www.instagram.com/litterati/', 'https://www.instagram.com/thewhitehartford/']


for instagram_user_url in instagram_urls:
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)
    driver.get(instagram_user_url)

    r = requests.get(instagram_user_url)

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    for post in soup.find('article', {'class': 'FyNDV'}).findAll('a'):
        print(post['href'])
        c.execute('SELECT * FROM insta_photo_urls WHERE url=?', (post['href'],))
        if c.fetchone() is None:
            # Insert a row of data
            c.execute("INSERT INTO insta_photo_urls VALUES (?)", (post['href'],))

            # Save (commit) the changes
            conn.commit()

conn.close()


