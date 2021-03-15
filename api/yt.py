import os
import traceback

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow


#DEVELOPER_KEY ='AIzaSyC1LLUmK0oAoglnUwPEd9q3a64OU3kRbGY'
DEVELOPER_KEY = 'AIzaSyDl3jE7r52FaATNMQ-pXdtwHDSB59tqTjA'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'
CLIENT_SECRET_FILE = 'client_secret.json'
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]

import pprint
pp=pprint.PrettyPrinter(indent=4)


def youtube_search(query):
    videos = []
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)
    try:
        resp = youtube.search().list(
                                     q=query,
                                     part='id,snippet',
                                     maxResults=8,
                                     type='video',
                                     videoEmbeddable='true',
                                     order='relevance'
                                     ).execute()
        #pp.pprint(resp)
        for result in resp.get('items', []):
            if result['id']['kind'] == 'youtube#video':
                feed = {'video_id': result['id']['videoId'], 'video_title': result['snippet']['title']}
                videos.append(feed)

    except Exception:
        traceback.print_exc()

    return videos

def export_playlist(title, description, playlist):
    flow = InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRET_FILE, scopes)
    credentials = flow.run_console()
    youtube = build(
        YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, credentials=credentials)

    body = dict(
        snippet=dict(
            title=title,
            description=description
        ),
        status=dict(
            privacyStatus='private'
        ) 
    )
    request = youtube.playlists().insert(part='snippet, status',
                               body=body
                               )
    response = request.execute()
    print(response)
    playlist_id = response['id']
    for video in playlist:
        video_id = video['video_id']
        request = youtube.playlistItems().insert(
            part="snippet",
            body={
              "snippet": {
                "playlistId": playlist_id,
                "position": 0,
                "resourceId": {
                  "kind": "youtube#video",
                  "videoId": video_id
                }
              }
            }
        )
        response = request.execute()
        print(response)
