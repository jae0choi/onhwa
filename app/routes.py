from flask import render_template
from flask import jsonify
from flask import request  
from flask import redirect, url_for
#from flask_sse import sse

from app import app
from app import db
from app.forms import Form
from app.forms import RequestForm
from app.yt import youtube_search
from app.yt import export_playlist
from app.models import Video

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
    app.logger.debug('current requests')
    app.logger.debug(requests)
    return redirect(url_for('main'))


@app.route('/load_playlist', methods=['GET'])
def load_playlist():
    playlist = [{'video_id': video.video_id, 'video_title': video.title} for video in Video.query.all()]
    return jsonify(data=playlist)

@app.route('/edit_playlist', methods=['GET', 'POST'])
def edit_playlist():
    mode = request.form['mode']
    vid = request.form['video_id']
    if mode == 'add':
        video_title = request.form['video_title']
        #playlist.append({'video_id': vid, 'video_title': video_title})
        video = Video(video_id=vid, title=video_title)
        db.session.add(video)
    elif mode == 'remove':
        #playlist = [video for video in playlist if video['video_id'] != vid]
        video = Video.query.filter(Video.video_id == vid).delete()
    try:
        db.session.commit()
    except:
        db.session.rollback()

    playlist = [{'video_id': video.video_id, 'video_title': video.title} for video in Video.query.all()]
    app.logger.debug('Current playlist')
    app.logger.debug(playlist)
    return jsonify(data=playlist)

@app.route('/reorder_playlist', methods=['GET', 'POST'])
def reorder_playlist():
    video_ids = request.form.getlist('video_ids[]')
    playlist = [{'video_id': video.video_id, 'video_title': video.title} for video in Video.query.all()]
    new_playlist = [list(filter(lambda v: v['video_id'] == video_id, playlist))[0] for video_id in video_ids]
    
    try:
        db.session.query(Video).delete()
        for video in new_playlist:
            v = Video(video_id=video['video_id'], title=video['video_title'])
            db.session.add(v)
        db.session.commit()
    except:
        db.session.rollback()

    app.logger.debug('reorder_playlist')
    app.logger.debug(new_playlist)

    return jsonify(data=new_playlist)

@app.route('/export_playlist', methods=['GET'])
def export_pl():
    playlist_title = 'Onhwa Cafe'
    description = 'Onhwa Cafe Playlist'
    playlist = [{'video_id': video.video_id, 'video_title': video.title} for video in Video.query.all()]
    export_playlist(playlist_title, description, playlist)
    return jsonify(data='OK')