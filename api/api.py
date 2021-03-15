import os

import logging

from flask import Flask
from flask import render_template
from flask import jsonify
from flask import request  
from flask import redirect, url_for
#from flask_sse import sse

from forms import Form
from forms import RequestForm

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

playlist = [{'video_id': 'fBVtXuA-xB8', 'video_title': 'Relaxing Bossa Nova & Jazz Music For Study - Smooth Jazz Music - Background Music'}]
requests = []

logging.basicConfig(level = logging.DEBUG)

if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
else:
    file_handler = logging.FileHandler('onhwa.log')
    handler = logging.StreamHandler()
    file_handler.setLevel(logging.DEBUG)
    logging.handler.setLevel(logging.DEBUG)
    logging.file_handler.setFormatter(Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]'
     ))
    logging.handler.setFormatter(Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]'
     ))
    app.logger.addHandler(handler)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.DEBUG)

@app.route('/', methods=['GET'])
def main():
    form = RequestForm()
    return render_template('main.html',  form=form)


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

@app.route('/request_song', methods=['GET', 'POST'])
def request_song():
    form = RequestForm()
    q = {}
    q['artist'] = form.artist.data
    q['title'] = form.title.data
    q['requester'] = form.requester.data
    requests.append(q)
    app.logger.debug('current requests')
    app.logger.debug(requests)
    return redirect(url_for('main'))


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
    app.logger.debug('Current playlist')
    app.logger.debug(playlist)
    return jsonify(data=playlist)

@app.route('/update_playlist', methods=['GET', 'POST'])
def update_playlist():
    global playlist
    video_ids = request.form.getlist('video_ids[]')
    playlist = [list(filter(lambda v: v['video_id'] == video_id, playlist))[0] for video_id in video_ids]
    
    app.logger.debug('update_playlist')
    app.logger.debug(playlist)

    return 'OK'

@app.route('/export_playlist', methods=['GET'])
def export_pl():
    playlist_title = 'Onhwa Cafe'
    description = 'Onhwa Cafe Playlist'
    export_playlist(playlist_title, description, playlist)
    return jsonify(data='OK')


