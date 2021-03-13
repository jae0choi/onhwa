import os
import traceback

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


DEVELOPER_KEY ='AIzaSyC1LLUmK0oAoglnUwPEd9q3a64OU3kRbGY'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

import pprint
pp=pprint.PrettyPrinter(indent=4)

def youtube_search(query):
    videos = []
    try:
        youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

        resp = youtube.search().list(
                                     q=query,
                                     part='id,snippet',
                                     maxResults=5,
                                     type='video',
                                     videoEmbeddable='true',
                                     order='relevance'
                                     ).execute()
        #pp.pprint(resp)
        for result in resp.get('items', []):
            if result['id']['kind'] == 'youtube#video':
                feed = {'id': result['id']['videoId'], 'title': result['snippet']['title']}
                videos.append(feed)

    except Exception, e:
        traceback.print_exc()

    return videos

