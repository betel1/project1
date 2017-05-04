# -*- coding: utf-8 -*-
"""
Created on Thu May 04 14:49:11 2017

@author: Eric
"""
from db import ShowsDB
import tornado.ioloop
import tornado.web
import json
import io
import matplotlib.pyplot as plt
import pylab
import os
import time
from PIL import Image


PORT = 9137

COLORS = (
    'A',
    'B',
    'C'
)

# Ten-Item Personality Inventory (TIPI)
# http://gosling.psy.utexas.edu/wp-content/uploads/2014/09/tipi.pdf
# Preceded by the header: 'I see myself as:'

try:
    os.remove('votes.json')
    os = {}
except (OSError):
    os = {}

try:
    VOTES = json.load(open('votes.json'))
except (IOError, ValueError):
    VOTES = {}

class MainHandler(tornado.web.RequestHandler):
   
    
    '''def initialize(self, db):
        self.db = db'''
        
    def get(self):
        self.render('responses.html', colors=COLORS, votes=VOTES)
class FormHandler(tornado.web.RequestHandler):
    def get(self):
        # Calculate the score for each personality trait
        Extraversion = float(int(self.get_argument("q01", 0)) + int(self.get_argument("q06", 0)))/2
        Agreeableness = float(int(self.get_argument("q02", 0)) + int(self.get_argument("q07", 0)))/2
        Conscientiousness = float(int(self.get_argument("q03", 0)) + int(self.get_argument("q08", 0)))/2
        Neuroticism = float(int(self.get_argument("q04", 0)) + int(self.get_argument("q09", 0)))/2
        Openness = float(int(self.get_argument("q05", 0)) + int(self.get_argument("q10", 0)))/2
        
        if Openess>=5:
            gen1 = "Action"
            gen2 = ""
        # Load the scores into dictionary
        gen = []
        gen[0] = gen1
        gen[1] =gen2
        VOTES['Extraversion'] = VOTES.get('Extraversion', 0) + Extraversion
        VOTES['Agreeableness'] = VOTES.get('Agreeableness', 0) + Agreeableness
        VOTES['Conscientiousness'] = VOTES.get('Conscientiousness', 0) + Conscientiousness
        VOTES['Neuroticism'] = VOTES.get('Neuroticism', 0) + Neuroticism
        VOTES['Openness'] = VOTES.get('Openness', 0) + Openness
        json.dump(VOTES, open('votes.json', 'w'))
        self.render('result.html', votes=VOTES,gen1 = gen1,gen2 = gen2)
        
class GenreHandler(tornado.web.RequestHandler):
    def initialize(self, db):
        self.db = db
    def get(self):    
        shows = self.db.search_genre("genre")
        for i in range(len(shows)):
            shows[i]['genres'] = self.db.searchg(shows[i]['show_id'])
                
        self.write(dict(data = shows))

# BE SURE TO TURN OFF DEBUG IN PROD
db = ShowsDB
Application = tornado.web.Application([
        (r"/", MainHandler),
        (r"/results", ResultsHandler),
        (r"/search", GenreHandler,{'db':db}),
        (r"/files/(.*)", tornado.web.StaticFileHandler, {'path': '.'}),
    ], debug=True)

Application.listen(PORT)
