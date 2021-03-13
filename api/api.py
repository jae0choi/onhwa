import os

from flask import Flask
from flask import render_template

from forms import SearchForm

import pprint
pp = pprint.PrettyPrinter(indent=4)

from yt import youtube_search

app = Flask(__name__)

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

@app.route('/', methods=['GET', 'POST'])
def main():
    form = SearchForm()
    if form.validate_on_submit():
        q = form.query.data
        videos = youtube_search(q)         
        #pp.pprint(videos)
        return render_template('index.html', form=form, videos=videos)
    else:
        return render_template('index.html', form=form, videos=[])

    

