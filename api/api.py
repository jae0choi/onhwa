import os

from flask import Flask
from flask import render_template
from flask import jsonify
from flask import request  

from forms import Form

import pprint
pp = pprint.PrettyPrinter(indent=4)

from yt import youtube_search

app = Flask(__name__)

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

playlist = []

@app.route('/', methods=['GET'])
def main():
    form = Form()
    return render_template('index.html', form=form)

@app.route('/search_youtube', methods=['GET', 'POST'])
def search_youtube():
    form = Form()
    q = form.query.data
    return jsonify(data=youtube_search(q))

@app.route('/load_playlist', methods=['GET'])
def load_playlist():
    return jsonify(data=playlist)

@app.route('/edit_playlist', methods=['GET', 'POST'])
def edit_playlist():
    global playlist
    vid = request.form['video_id']
    mode = request.form['mode']
    if mode == 'add':
        playlist.append(vid)
    elif mode == 'remove':
        playlist.remove(vid)
    pp.pprint(playlist)
    return jsonify(data=playlist)

#@app.route('/remove_from_playlist', methods=['GET', 'POST'])
