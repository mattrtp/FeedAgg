import rss_reader
import twitter_reader
import sqlite3

conn = sqlite3.connect('feeds.db')

c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS seen_urls (url text, title text, summary text, img_url text)''')


with open('output.html', 'w', encoding='utf8') as outfile:
    outfile.write("<!DOCTYPE html><html><meta charset=\"utf-8\">")
    rss_reader.do()
    twitter_reader.do()

    c.execute('SELECT * FROM seen_urls ORDER BY rowid DESC')
    for entry in c.fetchall():
        outfile.write("<h1>")
        outfile.write(entry[1])
        outfile.write("</h1>")
        outfile.write("<br>")
        if entry[3] is not None:
            outfile.write('<img src="' + entry[3] + '" style="height:250px">')
        outfile.write("<br>")
        outfile.write(entry[2])
        outfile.write("<br>")
        outfile.write('<a href="' + entry[0] + '">' + entry[0] + '</a>')
        outfile.write("<br>")
        outfile.write("<br>")
        outfile.write("<br>")

    outfile.write("</html>")

conn.close()