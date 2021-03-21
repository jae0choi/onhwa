from app import db
from app import login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class Video(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    video_id = db.Column(db.String(20), index=True, unique=True)
    title = db.Column(db.String(256), index=True)
    
    artist = db.Column(db.String(256), index=True)
    song_title = db.Column(db.String(256), index=True)
    requester = db.Column(db.String(256), index=True)

    def __repr__(self):
        return '<{} : {}>'.format(self.video_id, self.title, self.artist, self.song_title, self.requester)
    
class Request(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    artist = db.Column(db.String(256), index=True)
    title = db.Column(db.String(256), index=True)
    requester = db.Column(db.String(256), index=True)

    def __repr__(self):
        return '<Requester: {}, Title: {}, Artist: {}'.format(self.requester, self.title, self.artist)

    def get_dict(self):
        return {'requester': self.requester, 'artist': self.artist, 'title': self.title}

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username) 

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class ServerSetting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    request_open = db.Column(db.Boolean, default=False, nullable=False)        
       

@login.user_loader
def load_user(id):
    return User.query.get(int(id))