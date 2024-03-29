from app import app, db
from app.models import Video, Request, User, ServerSetting


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Video': Video, 'Request': Request, 'User': User, 'ServerSetting': ServerSetting}


