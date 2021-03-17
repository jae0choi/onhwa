from flask import render_template
from flask import jsonify
from flask import request  
from flask import redirect, url_for
from flask_login import current_user, login_user
from flask_login import logout_user
from flask_login import login_required
#from flask_sse import sse
from werkzeug.urls import url_parse

from app import app
from app import db
from app.forms import Form, RequestForm
from app.yt import youtube_search, export_playlist
from app.models import Video, Request, User, ServerSetting

from distutils.util import strtobool

@app.route('/', methods=['GET'])
def main():
    form = RequestForm()
    return render_template('main.html',  form=form)

@app.route('/dj', methods=['GET'])
# @login_required
def dj():
    form = Form()
    return render_template('index.html', form=form)

'''
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
'''

@app.route('/search_youtube', methods=['GET', 'POST'])
def search_youtube():
    form = Form()
    q = form.query.data
    return jsonify(data=youtube_search(q))

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
    playlist_title = 'Onhwa Cafe '
    description = 'Onhwa Cafe DJ Playlist'
    playlist = [{'video_id': video.video_id, 'video_title': video.title} for video in Video.query.all()]
    export_playlist(playlist_title, description, playlist)
    return jsonify(data='OK')

@app.route('/request_song', methods=['GET', 'POST'])
def request_song():
    form = RequestForm()
    artist = form.artist.data
    title = form.title.data
    requester = form.requester.data
    app.logger.debug('Request received %s - %s - %s', requester, artist, title)
    request = Request(requester=requester, artist = artist, title = title)
    try:    
        db.session.add(request)
        db.session.commit()
    except:
        db.session.rollback()
    return redirect(url_for('main'))

@app.route('/get_requests', methods=['GET'])
def get_requests():
    requests = [req.get_dict() for req in Request.query.all()]
    app.logger.debug('get requests')
    app.logger.debug(requests)
    return jsonify(data=requests)

@app.route('/check_open_for_request', methods=['GET'])
def check_open_for_request():
    is_request_opened = ServerSetting.query.get(1).request_open
    return jsonify(data=is_request_opened)

@app.route('/send_request_status', methods=["POST"])
def send_request_status():
    is_request_open = request.form['is_request_open']
    app.logger.debug(is_request_open)
    ServerSetting.query.get(1).request_open = strtobool(is_request_open)
    db.session.commit()
    return 'OK'
