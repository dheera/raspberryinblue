#!/usr/bin/python3

from flask import Blueprint, render_template, abort, request
import requests, json

scores = Blueprint('scores', __name__, template_folder='templates')

# view-source:http://localhost:5090/scores?url=http://imslp.org/wiki/Symphony_No.9,_Op.125_(Beethoven,_Ludwig_van)

@scores.route('/scores')
def show():
  url = request.args.get('url','')
  if 'imslp.org/wiki/' not in url:
    abort(404)
  params = {
    'action': 'raw',
  }
  headers = {
    'Referer': 'http://localhost:5900/scores'
  }
  response = requests.get(url, params = params).text
  lines = response.split('\n')
  outscores = []
  attrs = {}
  for line in lines:
    line = line.strip()
    if line.startswith('{{#fte:imslpfile'):
      outscores.append({'files':[]})

    if line.startswith('|') and '=' in line and len(outscores)>0:
      line = line.strip('|')
      key, val = line.split('=',1)
      attrs[key] = val

    if line.startswith('}}') and len(outscores)>0:
      for i in range(1,32):
        if 'File Name ' + str(i) in attrs and 'File Description ' + str(i) in attrs:
          outscores[-1]['files'].append({
            'filename':    attrs.get('File Name ' + str(i),''),
            'description': attrs.get('File Description ' + str(i),''),
            'page_count':  attrs.get('Page Count ' + str(i),0),
          })

      if 'Copyright' in attrs:
        outscores[-1]['copyright'] = attrs.get('Copyright')

      if 'Publisher Information' in attrs:
        outscores[-1]['publisher'] = attrs.get('Publisher Information')

      if 'Misc. Notes' in attrs:
        outscores[-1]['notes'] = attrs.get('Misc. Notes')

      if 'Thumb Filename' in attrs:
        outscores[-1]['thumb'] = attrs.get('Thumb Filename')

  return json.dumps(outscores)

# http://imslp.org/api.php?action=query&titles=File:TN-Beethoven_Werke_Breitkopf_Serie_1_No_5_Op_67.jpg&prop=imageinfo&iiprop=url&format=json
