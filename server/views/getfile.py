#!/usr/bin/python3

from flask import Blueprint, render_template, abort, request, Response, redirect
import requests, json
from bs4 import BeautifulSoup
from pprint import pprint

getfile = Blueprint('getfile', __name__, template_folder='templates')

@getfile.route('/getfile/<path:url>')
def show(url):
  # url = request.args.get('url','')
  if 'imslp.org/' not in url:
    abort(404)

  headers = {
    'Cookie': 'imslpdisclaimeraccepted=yes',
  }

  url = url.replace('DisclaimerAccept', 'ImageHandler')

  response = requests.get(url, allow_redirects = False, headers = headers)
  print(response.headers.get('Location',''))
  return redirect(response.headers.get('Location',''))
