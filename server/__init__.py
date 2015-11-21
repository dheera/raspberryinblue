#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, request, render_template, send_file, send_from_directory, redirect, make_response
from jinja2 import Markup
import re, json, os, socket, htmlmin
from random import randrange
from pprint import pprint
import redis
from flask.ext.cache import Cache

app = Flask(__name__)

cache = Cache(app,config={
  'CACHE_TYPE':       'redis',
  'CACHE_REDIS_URL':  os.environ.get('REDIS_URL') or 'redis://localhost/0',
})

@app.route('/')
def get_index():
  return htmlmin.minify(render_template('index.html'))

@app.route('/manifest.appcache')
def get_appcache():
  res = make_response(render_template('manifest.appcache'), 200)
  res.headers["Content-Type"] = "text/cache-manifest"
  return res

from .views.search import search
app.register_blueprint(search)

from .views.scores import scores
app.register_blueprint(scores)

from .views.composers import composers
app.register_blueprint(composers)

from .views.getfile import getfile
app.register_blueprint(getfile)

@app.route('/favicon.ico')
def send_favicon():
    return send_file('static/favicon.ico')

@app.after_request
def after_request(response):
  if response.headers['Content-Type'].find('image/')==0:
    response.headers['Cache-Control'] = 'max-age=7200, must-revalidate'
    response.headers['Expires'] = '0'
  elif response.headers['Content-Type'].find('application/')==0:
    response.headers['Cache-Control'] = 'no-cache, must-revalidate'
    response.headers['Expires'] = '0'
  else:
    response.headers['Cache-Control'] = 'no-cache, must-revalidate'
    response.headers['Expires'] = '0'

  return response

if __name__ == '__main__':
  print(app.url_map)
  app.run(debug=True)
