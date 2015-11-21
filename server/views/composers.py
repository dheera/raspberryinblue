#!/usr/bin/python3

from flask import Blueprint, render_template, abort, request, Response, redirect
import requests, json
from bs4 import BeautifulSoup
from pprint import pprint
from server import cache

composers = Blueprint('composers', __name__, template_folder='templates')

@composers.route('/composers/<name>/thumb')
def show_photo(name):
  name = name.replace(' ','_')
  try:
    data = get_composer_data(name)
    if 'thumb' in data:
      return redirect(data['thumb'])
    else:
      return redirect('/static/blank.gif')
  except:
    return redirect('/static/blank.gif')

@cache.memoize(timeout = 30*86400)
def get_composer_data(name):

  composer_data = {}

  url = 'http://imslp.org/wiki/Category:' + name
  params = {
    'action': 'render',
  }
  response = requests.get(url, params = params).text

  if not response:
    raise Exception()

  soup = BeautifulSoup(response,'lxml')
  el = soup.find('img')

  if el.attrs.get('src'):
    src = el.attrs.get('src')
    if not src.startswith('http'):
      src = 'http://imslp.org' + src
    composer_data['thumb'] = src

  return composer_data

