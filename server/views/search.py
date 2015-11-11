#!/usr/bin/python3

from flask import Blueprint, render_template, abort, request
import requests, json

search = Blueprint('search', __name__, template_folder='templates')

@search.route('/search')
def show():
  # Todo: Build our own search engine (Elasticsearch?)
  # because Google is deprecating this API and not providing a
  # usable replacement

  query = request.args.get('q','')
  url = 'https://ajax.googleapis.com/ajax/services/search/web'
  params = {
    'v': '1.0',
    'q': 'site:imslp.org -"Category:"' + query,
    'userip': request.remote_addr,
  }
  headers = {
    'Referer': 'http://localhost:5900/search'
  }
  response = json.loads(requests.get(url, params = params).text)
  results = response.get('responseData',{}).get('results',[])
  results_out = []
  for result in results:
    results_out.append({
      'url': result['url'],
      'title': result['titleNoFormatting'].split(' - ',1)[0],
    })
  return json.dumps(results_out)
