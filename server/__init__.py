#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, request, render_template, send_file, send_from_directory, redirect
from jinja2 import Markup
import re, json, os, socket, htmlmin
from random import randrange

app = Flask(__name__)

@app.route('/')
def get_index():
  return htmlmin.minify(render_template('index.html'))

from .views.search import search
app.register_blueprint(search)

from .views.scores import scores
app.register_blueprint(scores)

@app.route('/favicon.ico')
def send_favicon():
    return send_file('static/favicon.ico')

@app.after_request
def after_request(response):

  if response.headers['Content-Type'].find('image/')==0:
    response.headers['Cache-Control'] = 'max-age=7200, must-revalidate'
    response.headers['Expires'] = '0'
  elif response.headers['Content-Type'].find('application/')==0:
    response.headers['Cache-Control'] = 'max-age=7200, must-revalidate'
    response.headers['Expires'] = '0'
  else:
    response.headers['Cache-Control'] = 'no-cache, must-revalidate'
    response.headers['Expires'] = '0'

  return response

if __name__ == '__main__':
  print(app.url_map)
  app.run(debug=True)
