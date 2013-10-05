import os
import string
import requests
from flask import Flask, render_template

app = Flask(__name__)
app.config.from_pyfile('config.py')

@app.route('/')
def hello():
    return 'SECRET=' + os.environ['SECRET']

@app.route('/minimal')
def minimal():
    terms = get_terms(["Code Geass", "Full Metal Alchemist"])
    result = get_wallpapers(terms)
    return render_template("minimal.html", result=result, terms=terms)

def get_wallpapers(terms):
    api_key = os.environ['API_KEY']
    search_engine_id = os.environ['SEARCH_ENGINE_ID']
    
    query = ('https://www.googleapis.com/customsearch/v1'
            + '?key=' + api_key
            + '&cx=' + search_engine_id
            + '&searchType=' + 'image'
            + '&imageSearchResultSetSize=' + 'large' # Lots of images
            + '&tbs=' + 'isz:l' # Large images
            + '&as_q=' + 'wallpaper'
            + '&as_oq=' + terms
            + '&q=' + terms)
    return requests.get(query)

def get_terms(show_titles):
    with_spaces = " OR ".join(show_titles)
    return string.replace(with_spaces, " ", "+")

if __name__ == '__main__':
    app.run(debug=True)
