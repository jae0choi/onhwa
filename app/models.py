from app import db

class Video(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    video_id = db.Column(db.String(20), index=True, unique=True)
    title = db.Column(db.String(256), index=True)

    def __repr__(self):
        return '<{} : {}>'.format(self.video_id, self.title)
    
class Request(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    artist = db.Column(db.String(256), index=True)
    title = db.Column(db.String(256), index=True)
    requester = db.Column(db.String(256), index=True)

    def __repr__(self):
        return '<Requester: {}, Title: {}, Artist: {}'.format(self.requester, self.title, self.artist)
