from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class Form(FlaskForm):
    query = StringField('Search YouTube', validators=[DataRequired()])
    #submit = SubmitField('Go!')
    
class RequestForm(FlaskForm):
    artist = StringField('Artist')
    title = StringField('Title')
    requester = StringField('Requester')