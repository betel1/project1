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


PORT = 8888



class MainHandler(tornado.web.RequestHandler):
   
        
    def get(self):
        self.render('responses.html')
class FormHandler(tornado.web.RequestHandler):
    def get(self):
        # Calculate the score for each personality trait
        
        Open= float(int(self.get_argument("q01", 0)) + int(self.get_argument("q05", 0)))/2
        violence= float(int(self.get_argument("q02", 0)) + int(self.get_argument("q03", 0)))/2
        Realistic= float(int(self.get_argument("q06", 0)) + int(self.get_argument("q09", 0)))/2
        Popular = float(int(self.get_argument("q10", 0)) + int(self.get_argument("q07", 0)))/2
        Engaging= float(int(self.get_argument("q10", 0)) + int(self.get_argument("q3", 0)))/2
        
        if Open >= 3.5 :
            gen1 = "Drama"
            gen2 = "Mystery"
        
        elif violence >= 3.5: 
        	gen1 ="Action"
        	gen2 ="Thriller"
        elif Realistic >= 3.5: 
        	gen1="Drama"
        	gen2="Comedy"
        elif Popular >= 3.5: 
        	gen1="Drama"
        	gen2= "Adventure"
        elif Engaging >= 3.5: 
        	gen1="Mystery"
        	gen2= "Sci-fi"
        else:
               gen1= "Western"
               gen2 = "Fantasy"
        

        
        self.render('result.html', gen1=gen1,gen2=gen2)
        
class GenreHandler(tornado.web.RequestHandler):
    def initialize(self, db):
        self.db = db
    def get(self):  
        gen1 = self.get_argument('genre1')
        gen2 = self.get_argument('genre2')
        shows = self.db.search(gen1,gen2)
        for i in range(len(shows)):
            shows[i]['genres'] = self.db.searchg(shows[i]['show_id'])
                
        self.write(dict(data = shows))
        
class DetailHandler(tornado.web.RequestHandler):
    def initialize(self,db):
        self.db = db
    def get(self):
        show_id = self.get_argument('show_id')
        self.write(dict(data = self.db.detail(show_id)))

# BE SURE TO TURN OFF DEBUG IN PROD
db = ShowsDB()
Application = tornado.web.Application([
        (r"/", MainHandler),
        (r"/form", FormHandler),
        (r"/search", GenreHandler,{'db':db}),
        (r'/detail', DetailHandler, {'db': db }),
        (r"/js/(.*)", tornado.web.StaticFileHandler, {'path': 'js'}),
        (r"/css/(.*)", tornado.web.StaticFileHandler, {'path': 'css'})
    ], debug=True)

Application.listen(PORT)
tornado.ioloop.IOLoop.current().start()
