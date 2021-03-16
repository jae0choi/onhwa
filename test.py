import pprint
import yt
import argparse

pp = pprint.PrettyPrinter(indent=4)

def test():
    videos = yt.youtube_search('Michael Jackson')
    pp.pprint(videos)

def test_list(args):
    yt.export_playlist(args)

if __name__ == '__main__':
           
  parser = argparse.ArgumentParser()
  parser.add_argument('--title',
      default='Test Playlist',
      help='The title of the new playlist.')
  parser.add_argument('--description',
      default='A private playlist created with the YouTube Data API.',
      help='The description of the new playlist.')
    
  args = parser.parse_args()
  test_list(args)