import os
import string
import requests
from flask import Flask, render_template, session, request, redirect, url_for

from MyAnimeListStuffs.getMALShowList import _getAnimeList

app = Flask(__name__)
app.config.from_pyfile('config.py')
app.secret_key = 'supah_secret'

@app.route('/')
def hello():
    return render_template("home.html")

#@app.route('/minimal')
#def minimal():
    #terms = get_terms(["Death Note", "Avatar the Last Airbender"])
    #result = get_wallpapers(terms)
    #return render_template("minimal.html", result=result, terms=terms)

@app.route('/results', methods=['GET', 'POST'])
def results():
    if request.method == 'POST':
        username = request.form['username']
        session['username'] = username
        return redirect(url_for('results'))
    else:
        shows = _getAnimeList(session['username'])
        terms = get_terms(shows)
        result = get_wallpapers(terms)
        return render_template("results.html", result=result, username=session['username'])

def get_wallpapers(terms):
    api_key = os.environ['API_KEY']
    search_engine_id = os.environ['SEARCH_ENGINE_ID']
    
    query = ('https://www.googleapis.com/customsearch/v1'
            + '?key=' + api_key
            + '&cx=' + search_engine_id
            + '&searchType=' + 'image'
            + '&imageSearchResultSetSize=' + 'large' # Lots of images
            + '&imgSize=' + 'huge'
            #+ '&imgColorType=' + 'color'
            + '&num=' + '10'
            + '&q=' + terms)
    return requests.get(query)

def get_terms(show_titles):
    wallpapers = [title + ' wallpaper' for title in show_titles]
    with_spaces = " OR ".join(wallpapers)
    return string.replace(with_spaces, " ", "+")

if __name__ == '__main__':
    app.run(debug=True)
