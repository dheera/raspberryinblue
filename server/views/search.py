#!/usr/bin/python3

from flask import Blueprint, render_template, abort, request
import requests, json, re

search = Blueprint('search', __name__, template_folder='templates')

@search.route('/search')
def show():
  # Todo: Build our own search engine (Elasticsearch?)
  # because Google is deprecating this API and not providing a
  # usable replacement

  query = request.args.get('q','').strip()

  if query == '':
    return '[]'

  url = 'https://ajax.googleapis.com/ajax/services/search/web'
  params = {
    'v': '1.0',
    'q': 'site:imslp.org ' + query,
    'userip': request.remote_addr,
    'rsz': '8',
  }
  headers = {
    'Referer': 'http://sonatainblue.com/search'
  }
  response = json.loads(requests.get(url, params = params, headers = headers).text)
  results = response.get('responseData',{}).get('results',[])
  results_out = []
  for result in results:
    if 'Category:' not in result['titleNoFormatting'] and \
       'List of' not in result['titleNoFormatting'] and \
       'Talk:' not in result['titleNoFormatting'] and \
       'User:' not in result['titleNoFormatting'] and \
       'IMSLP:' not in result['titleNoFormatting'] and \
       '(' in result['titleNoFormatting']:

      result_out = {
        'url': result['unescapedUrl'],
        'title': result['titleNoFormatting'].split(' - ',1)[0],
      }

      m = re.search(r".*\((.*)\)", result['unescapedUrl'])
      if(m):
        result_out['composer'] = m.group(1)
        result_out['thumb'] = '/composers/' + result_out['composer'].replace(' ','_') + '/thumb'

      results_out.append(result_out)

  return json.dumps(results_out)
