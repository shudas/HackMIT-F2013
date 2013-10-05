import os
import requests
from flask import Flask, render_template

app = Flask(__name__)
app.config.from_pyfile('config.py')

@app.route('/')
def hello():
    return 'SECRET=' + os.environ['SECRET']

@app.route('/minimal')
def minimal():
    result = get_wallpapers(["Death Note", "Avatar the Last Airbender"])
    return render_template("minimal.html", result=result)

def get_wallpapers(show_titles):
    api_key = os.environ['API_KEY']
    search_engine_id = os.environ['SEARCH_ENGINE_ID']

    wallpapers = [title + ' wallpaper' for title in show_titles]
    terms = " OR ".join(wallpapers)
    
    query = ('https://www.googleapis.com/customsearch/v1'
            + '?key=' + api_key
            + '&cx=' + search_engine_id
            + '&searchType=' + 'image'
            + '&imageSearchResultSetSize=' + 'large'
            + '&q=' + terms) # Temporarily hard-coded
    return requests.get(query)

if __name__ == '__main__':
    app.run(debug=True)
