#!/usr/bin/python3

from flask import Blueprint, render_template, abort, request, Response
import requests, json
from bs4 import BeautifulSoup
from pprint import pprint
from server import cache

scores = Blueprint('scores', __name__, template_folder='templates')

@scores.route('/scores/<score_id>')
def show_by_id(score_id):
  try:
    scores_data = get_scores_data('http://imslp.org/wiki/' + score_id)
    return Response(json.dumps(scores_data), mimetype='application/json')
  except:
    return Response('[]', mimetype='application/json')

@scores.route('/scores')
def show_by_url():
  url = request.args.get('url','')
  if 'imslp.org/wiki/' not in url:
    abort(404)

  try:
    scores_data = get_scores_data(url)
    return Response(json.dumps(scores_data), mimetype='application/json')
  except:
    return Response('[]', mimetype='application/json')

@cache.memoize(timeout = 30*86400)
def get_scores_data(url):
  print("**")
  scores_data = []
  params = {
    'action': 'render',
  }

  response = requests.get(url, params = params).text
  if len(response) == 0:
    raise Exception()

  soup = BeautifulSoup(response,'lxml')
  el = soup.find('h2')

  while el is not None:
    if el.name == 'h2':
      is_sheet_music = 'Sheet Music' in el.get_text()
    if is_sheet_music:
      if el.name == 'h3':
        scores_data.append( { '@type': 'heading', 'level': 3, 'text': el.get_text().strip() })
      if el.name == 'h4':
        scores_data.append( { '@type': 'heading', 'level': 4, 'text': el.get_text().strip() })
      if el.name == 'h5':
        scores_data.append( { '@type': 'heading', 'level': 5, 'text': el.get_text().strip() })

      if 'we' in el.get('class',[]):
        # begin score
        print("*** begin score")
        scores_data.append({ '@type': 'score', 'files': [] })

      if len(scores_data)>0 and 'files' in scores_data[-1]:
        if 'we_file_download' in el.get('class',[]):
          el_a = el.find_next('a')
          scores_data[-1]['files'].append({
            'url': el_a.attrs['href'].replace('ImagefromIndex','IMSLPDisclaimerAccept'),
            'description': el_a.get_text().strip(),
          })

        if 'we_edition_label' in el.get('class',[]):
          el2 = el.find_next()
          if 'we_edition_entry' in el2.get('class',[]):
            key = el.get_text().strip(':. ')
            value = el2.get_text().strip()
            if key == 'Publisher Info':
              scores_data[-1]['publisher'] = el2.get_text()
            if key == 'Misc. Notes':
              scores_data[-1]['notes'] = el2.get_text()
            if key == 'Copyright':
              scores_data[-1]['copyright'] = el2.get_text()

        if 'we_thumb' in el.get('class',[]):
          el2 = el.find_next('img')
          if el2:
            src = el2.attrs.get('src','')
            if src.startswith('/'):
              scores_data[-1]['thumb'] = 'http://imslp.org' + src
            else:
              scores_data[-1]['thumb'] = src

    el = el.find_next()

  if len(scores_data) == 0:
    raise Exception()

  return scores_data

