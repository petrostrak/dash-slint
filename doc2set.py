#!/usr/local/bin/python3
import os, sqlite3
from boltons.fileutils import iter_find_files
from bs4 import BeautifulSoup

RES_PATH = 'Slint.docset/Contents/Resources'
conn = sqlite3.connect(RES_PATH + '/docSet.dsidx')
# conn = sqlite3.connect('docSet.dsidx')
cur = conn.cursor()

try: 
    cur.execute('DROP TABLE searchIndex;')
except: 
    pass

cur.execute('CREATE TABLE searchIndex(id INTEGER PRIMARY KEY, name TEXT, type TEXT, path TEXT);')
cur.execute('CREATE UNIQUE INDEX anchor ON searchIndex (name, type, path);')

docpath = RES_PATH + '/Documents'
os.chdir(docpath)

pages = iter_find_files('HTML', '*.html')
failed_pages = []

for filename in pages:
    try:
        with open(filename) as page:
            soup = BeautifulSoup(page, 'html.parser')
            name = soup.title.text.strip()
            type = 'Entry'
            paths = soup.h3.a.attrs['href'].strip().split('/')
            path = paths[len(paths) - 1]
            cur.execute(
                'INSERT OR IGNORE INTO searchIndex(name, type, path) VALUES (?,?,?)', (name, type, path))
            print('name: %s, path: %s' % (name, path))
    except Exception as e:
        print(e)
        failed_pages.append(filename)

print('Failed pages: %s' % failed_pages)

conn.commit()
conn.close()