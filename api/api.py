import os

from flask import Flask
from flask import render_template
from flask import jsonify

from forms import Form

import pprint
pp = pprint.PrettyPrinter(indent=4)

from yt import youtube_search

app = Flask(__name__)

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

@app.route('/', methods=['GET'])
def main():
    form = Form()
    return render_template('index.html', form=form)

@app.route('/search_youtube', methods=['GET', 'POST'])
def search_youtube():
    form = Form()
    q = form.query.data
    return jsonify(data=youtube_search(q))

#@app.route('/addSong', methods=['GET', 'POST'])
#def addSong():

    

