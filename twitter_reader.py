import requests
from bs4 import BeautifulSoup
import sqlite3


def do():
    conn = sqlite3.connect('feeds.db')

    c = conn.cursor()

    # Create tables
    c.execute('''CREATE TABLE IF NOT EXISTS twitter_urls (url text)''')

    c.execute('SELECT * FROM twitter_urls')
    twitter_urls = c.fetchall()

    for twitter in twitter_urls:
        r = requests.get(twitter[0])

        soup = BeautifulSoup(r.text, 'html.parser')

        for tweet in soup.find('ol', {'id': 'stream-items-id'}).findAll('li', {'class': 'js-stream-item'}):
            # Insert a row of data
            c.execute('SELECT * FROM seen_urls WHERE url=?', (tweet.find('a', {'class': 'tweet-timestamp'})['href'],))
            if c.fetchone() is None:
                c.execute("INSERT INTO seen_urls (url, title, summary) VALUES (?, ?, ?)", (tweet.find('a', {'class': 'tweet-timestamp'})['href'], tweet.find('strong', {'class': 'fullname'}).text, tweet.find('p', {'class': 'tweet-text'}).text))

            # Save (commit) the changes
            conn.commit()

    conn.close()