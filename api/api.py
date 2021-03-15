import os

from flask import Flask
from flask import render_template
from flask import jsonify
from flask import request  
#from flask_sse import sse

from forms import Form

import pprint
pp = pprint.PrettyPrinter(indent=4)

from yt import youtube_search
from yt import export_playlist

app = Flask(__name__)
'''
app.config["REDIS_URL"] = 'redis://localhost'
app.register_blueprint(sse, url_prefix='/stream')
'''

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

playlist = []

@app.route('/', methods=['GET'])
def main():
    return render_template('main.html')


@app.route('/dj', methods=['GET'])
def dj():
    form = Form()
    return render_template('index.html', form=form)

@app.route('/send')
def send_message():
    sse.publish({'message': 'Hello!'}, type='greeting')
    return 'Msg sent'

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
    mode = request.form['mode']
    vid = request.form['video_id']
    if mode == 'add':
        video_title = request.form['video_title']
        playlist.append({'video_id': vid, 'video_title': video_title})
    elif mode == 'remove':
        playlist = [video for video in playlist if video['video_id'] != vid]
    #pp.pprint(playlist)
    return jsonify(data=playlist)

@app.route('/export_playlist', methods=['GET'])
def export_pl():
    playlist_title = 'Onhwa Cafe'
    description = 'Onhwa Cafe Playlist'
    export_playlist(playlist_title, description, playlist)
    return jsonify(data='OK')
