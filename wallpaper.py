import os
import requests
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def hello():
    return 'SECRET=' + os.environ['SECRET']

@app.route('/minimal')
def minimal():
    api_key = os.environ['API_KEY']
    search_engine_id = os.environ['SEARCH_ENGINE_ID']
    
    query = ('https://www.googleapis.com/customsearch/v1'
            + '?key=' + api_key
            + '&cx=' + search_engine_id
            + '&q=' + 'death+note') # Temporarily hard-coded

    result = requests.get(query)

    render_template("minimal.html", result=result)