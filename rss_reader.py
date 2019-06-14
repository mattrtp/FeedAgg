import feedparser
import sqlite3


def do():
    conn = sqlite3.connect('feeds.db')

    c = conn.cursor()

    # Create tables
    c.execute('''CREATE TABLE IF NOT EXISTS rss_urls (url text)''')
    c.execute('''CREATE TABLE IF NOT EXISTS rss_url_filter (filter text)''')

    c.execute('SELECT * FROM rss_urls')
    rss_feed_urls2 = c.fetchall()

    for feed_url in rss_feed_urls2:
        NewsFeed = feedparser.parse(feed_url[0])

        for entry in NewsFeed["entries"]:
            #
            filter_out = False
            if "media_thumbnail" in entry:
                if c.fetchone() is None:
                    c.execute('SELECT filter FROM rss_url_filter')
                    for filter_word in c.fetchall():
                        if filter_word[0] in entry["link"]:
                            filter_out = True
                    if not filter_out:
                        # Insert a row of data
                        c.execute('SELECT * FROM seen_urls WHERE url=?', (entry["link"],))
                        if c.fetchone() is None:
                            c.execute("INSERT INTO seen_urls VALUES (?, ?, ?, ?)", (entry["link"], entry["title"], entry["summary"], entry["media_thumbnail"][0]["url"]))

            # Save (commit) the changes
            conn.commit()

    conn.close()