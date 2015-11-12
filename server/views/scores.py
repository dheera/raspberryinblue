#!/usr/bin/python3

from flask import Blueprint, render_template, abort, request, Response
import requests, json
from bs4 import BeautifulSoup
from pprint import pprint

scores = Blueprint('scores', __name__, template_folder='templates')

# view-source:http://localhost:5090/scores?url=http://imslp.org/wiki/Symphony_No.9,_Op.125_(Beethoven,_Ludwig_van)

@scores.route('/scores')
def show():
  url = request.args.get('url','')
  if 'imslp.org/wiki/' not in url:
    abort(404)
  params = {
    'action': 'render',
  }
  headers = {
    'Referer': 'http://localhost:5900/scores'
  }
  response = requests.get(url, params = params).text
  soup = BeautifulSoup(response,'lxml')
  el = soup.find('h2')

  scores = []

  while el is not None:
    if el.name == 'h2':
      is_sheet_music = 'Sheet Music' in el.get_text()
    if is_sheet_music:
      if el.name == 'h3':
        scores.append( { '@type': 'heading', 'level': 3, 'text': el.get_text().strip() })
      if el.name == 'h4':
        scores.append( { '@type': 'heading', 'level': 4, 'text': el.get_text().strip() })
      if el.name == 'h5':
        scores.append( { '@type': 'heading', 'level': 5, 'text': el.get_text().strip() })

      if 'we' in el.get('class',[]):
        # begin score
        print("*** begin score")
        scores.append({ '@type': 'score', 'files': [] })

      if len(scores)>0 and 'files' in scores[-1]:
        if 'we_file_download' in el.get('class',[]):
          el_a = el.find_next('a')
          scores[-1]['files'].append({
            'url': el_a.attrs['href'],
            'description': el_a.get_text().strip(),
          })

        if 'we_edition_label' in el.get('class',[]):
          el2 = el.find_next()
          if 'we_edition_entry' in el2.get('class',[]):
            key = el.get_text().strip(':. ')
            value = el2.get_text().strip()
            if key == 'Publisher Info':
              scores[-1]['publisher'] = el2.get_text()
            if key == 'Misc. Notes':
              scores[-1]['notes'] = el2.get_text()
            if key == 'Copyright':
              scores[-1]['copyright'] = el2.get_text()

        if 'we_thumb' in el.get('class',[]):
          el2 = el.find_next('img')
          if el2:
            src = el2.attrs.get('src','')
            if src.startswith('/'):
              scores[-1]['thumb'] = 'http://imslp.org' + src
            else:
              scores[-1]['thumb'] = src

    el = el.find_next()
  return Response(json.dumps(scores, indent=2), mimetype='text/plain')

# http://imslp.org/api.php?action=query&titles=File:TN-Beethoven_Werke_Breitkopf_Serie_1_No_5_Op_67.jpg&prop=imageinfo&iiprop=url&format=json
