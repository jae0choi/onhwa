import os
import traceback

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow

from app import app
app.logger.debug('Current environment: %s', app.env)

def youtube_search(query):
    videos = []
    youtube = build(os.getenv('YOUTUBE_API_SERVICE_NAME'), os.getenv('YOUTUBE_API_VERSION'), developerKey=os.getenv('DEVELOPER_KEY'), cache_discovery=False)
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
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    if app.env == 'development':
      os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    
    scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]
    flow = InstalledAppFlow.from_client_secrets_file(
                os.getenv('CLIENT_SECRET_FILE'), scopes)
    credentials = flow.run_console()
    youtube = build(
        os.getenv('YOUTUBE_API_SERVICE_NAME'), os.getenv('YOUTUBE_API_VERSION'), credentials=credentials)

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
    app.logger.debug(response)
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
        app.logger.debug(response)
