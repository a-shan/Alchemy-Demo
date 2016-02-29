# -*- coding: utf-8 -*-
"""
Alchemy-Demo is a framework to use with IBM Watson's Alchemy API.

@author: Alex Shan, Jonathan Yao, Henry Yu
"""

'''
import cgi
import argparse
import json
import pprint
import sys
import urllib
import urllib2
'''

import os
from google.appengine.ext.webapp import template
from google.appengine.ext import ndb
from google.appengine.api import images
import webapp2
import urllib
import urllib2
import json
import jinja2
import key

API_KEY = key.apiKey()


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

def IdentityFinder(jsonDict):
    name = ''
    if 'identity' in jsonDict:
        name = jsonDict['identity']['name']
    return name

def urlOpener(url):
    apiResult = ''
    if urllib2.urlopen(url,None):
        apiResult = urllib2.urlopen(url, None)
    return apiResult

class MainPage(webapp2.RequestHandler):
    def get(self):
        current_dir = os.path.dirname(__file__)
        index_path = os.path.join(current_dir, 'index.html')
        self.response.write(template.render(index_path, {}))

class Alchemy(webapp2.RequestHandler):
    def post(self):
    	current_dir = os.path.dirname(__file__)
    	queryInput = self.request.get('query')
    	#keyInput = self.request.get('key')

        keyInput = API_KEY
        apiInput = 'URLGetRankedImageFaceTags'

    	#apiInput = self.request.get('api')

        url = 'http://access.alchemyapi.com/calls/url/'+apiInput+'?apikey='+keyInput+'&outputMode=json&knowledgeGraph=1&url='+queryInput

        #poor defining of variables, re-do later to prevent errors
        apiResult = urlOpener(url)
        imgResult = json.loads(apiResult.read())
        result = imgResult['imageFaces'][0]
        
        name = IdentityFinder(result)
        if not name:
            name = 'Sorry, identity unknown!'

        template_values = {
            'img':queryInput,
            'query':name
        }

        template = JINJA_ENVIRONMENT.get_template('alchemy.html')
        self.response.write(template.render(template_values))

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/alchemy', Alchemy)
], debug=True)