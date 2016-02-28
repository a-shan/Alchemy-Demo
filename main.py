# -*- coding: utf-8 -*-
"""
Alchemy-Demo is a framework to use with IBM Watson's Alchemy API.

@author: Alex Shan, Jonathan Yao
"""

import os
from google.appengine.ext.webapp import template
import webapp2
import cgi
import argparse
import json
import pprint
import sys
import urllib
import urllib2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class MainPage(webapp2.RequestHandler):
    def get(self):
        current_dir = os.path.dirname(__file__)
        index_path = os.path.join(current_dir, 'index.html')
        self.response.write(template.render(index_path, {}))

    def post(self):
    	current_dir = os.path.dirname(__file__)
    	queryInput = self.request.get('query')
    	keyInput = self.requrest.get('key')
    	apiInput = self.request.get('api')

app = webapp2.WSGIApplication([
    ('/', MainPage)
], debug=True)