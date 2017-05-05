# coding: utf-8

# In[ ]:

#!/usr/bin/env python

import os
import sys
import json
import sqlite3
import argparse


def dict_factory(cursor, row):
    '''strict dictionary format for rows'''
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

class ShowsDB(object):
    '''A connection to the battlefields database'''

    DATA_DIR = 'shows.json'
    DB_FILE = os.path.join(DATA_DIR, '')

    def __init__(self, data_dir=DATA_DIR):
        '''A new connection to the database'''
        
        self.data_file = data_dir
        self.conn     = sqlite3.connect('shows.db')
        self.conn.row_factory = dict_factory
        self.conn.execute('PRAGMA foreign_keys = ON')
        
        self._create_table()
        self._populate_table()


    
    
    def _create_table(self):
        cur = self.conn.cursor()
        cur.execute( '''DROP TABLE IF EXISTS GenreTag;''')
        cur.execute( '''DROP TABLE IF EXISTS Shows;''')

        createS = '''CREATE TABLE Shows(
                    show_id INTEGER PRIMARY KEY,
                    name TEXT,
                    language TEXT,
                    summary TEXT,
                    img TEXT,
                    url TEXT);'''
        
        createG = '''CREATE TABLE GenreTag(
                    gtag_id INTEGER PRIMARY KEY,
                    show_id INTEGER,
                    genres TEXT,
                     FOREIGN KEY (show_id) REFERENCES Shows(show_id));'''
        cur.execute(createS)
        cur.execute(createG)

        
    
    
    def _populate_table(self):
        showsfile  = self.data_file
        cur = self.conn.cursor()
        with open(showsfile) as fh:
            data = json.load(fh)
        insert =  '''INSERT INTO Shows Values(:id,:name,:language,:summary,:image,:url);''' 
        insertg =  '''INSERT INTO GenreTag Values(NULL,?,?);''' 
        for record in data: 
            record['image']=record['image']['medium']
            cur.execute(insert, record)
            for genre in record['genres']:
                cur.execute(insertg,(record['id'],genre))
        
        self.conn.commit()

        
       
    
    
    def search(self,genre1,genre2):
        cur = self.conn.cursor()
   
        search = '''SELECT Shows.show_id, Shows.name,Shows.language,Shows.summary,Shows.img,Shows.url
                    FROM GenreTag JOIN Shows USING(show_id)
                    WHERE genres LIKE ? or genres LIKE ?;'''
        cur.execute(search,(genre1,genre2))
        return cur.fetchall()
        
    def searchg(self,show_id):
        cur = self.conn.cursor()
        search = '''SELECT genres
                    FROM GenreTag 
                    WHERE show_id ==?;'''
        cur.execute(search,(show_id,))
        a = []
        for row in cur.fetchall():
            a.append(row['genres'])
        return a
    
    def detail(self, show_id):
        cur = self.conn.cursor()        
        search = '''SELECT summary,show_id, name,img, url FROM Shows
                    WHERE show_id == ? ;'''
        cur.execute(search,(show_id,))
        return cur.fetchone()

        
      

    
    def genres(self):
        cur = self.conn.cursor()
        search = '''SELECT DISTINCT genres FROM GenreTag;'''
        cur.execute(search)
        a = []
        for row in cur.fetchall():
            a.append(row['genres'])
            print '{}'.format(row['genres'])
        return a
                
    def test(self):
        cur = self.conn.cursor()
        search = '''SELECT * FROM Shows;'''
        cur.execute(search)
        return cur.fetchall()
        
        
        
    
# main code block: test the module
if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description = 'test the ShowesDB interface'
    )
    parser.add_argument('--name', default='%',nargs = 2, help="Value for show name")
    args = parser.parse_args()
    db = ShowsDB()
    
    print json.dumps(db.search("Comedy","Action"), indent=1)
