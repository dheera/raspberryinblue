#!/usr/bin/python3

from flask import Blueprint, render_template, abort, request

search = Blueprint('search', __name__, template_folder='templates')

@search.route('/search')
def show():
  query = request.args.get('q','')
  return query
