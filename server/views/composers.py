#!/usr/bin/python3

from flask import Blueprint, render_template, abort, request, Response, redirect
import requests, json
from bs4 import BeautifulSoup
from pprint import pprint
from server import cache

def make_cache_key(*args, **kwargs):
  return request.url

composers = Blueprint('composers', __name__, template_folder='templates')

@composers.route('/composers/<name>/thumb')
@cache.cached(timeout = 30*86400, key_prefix = make_cache_key)
def show_photo(name):
  name = name.replace(' ','_')
  data = get_composer_info(name)
  if 'thumb' in data:
    return redirect(data['thumb'])

@cache.cached(timeout = 30*86400, key_prefix = make_cache_key)
def get_composer_info(name):

  composer_data = {}

  url = 'http://imslp.org/wiki/Category:' + name
  params = {
    'action': 'render',
  }
  response = requests.get(url, params = params).text
  soup = BeautifulSoup(response,'lxml')
  el = soup.find('img')

  if el.attrs.get('src'):
    src = el.attrs.get('src')
    if not src.startswith('http'):
      src = 'http://imslp.org' + src
    composer_data['thumb'] = src

  return composer_data

