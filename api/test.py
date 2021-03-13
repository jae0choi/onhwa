import pprint

pp = pprint.PrettyPrinter(indent=4)

def test():
    import yt

    videos = yt.youtube_search('Michael Jackson')
    pp.pprint(videos)


if __name__ == '__main__':
    test()
