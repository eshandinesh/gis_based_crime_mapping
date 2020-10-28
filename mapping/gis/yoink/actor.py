from pykka import Actor
from feed import*

class Config(Actor):
    def __init__(self, cfg):
        self.cfg = cfg

    def react(self, msg):
        if msg.get(('command') == 'download'):
            feeds = [Feed(f) for f in config.feeds.values()]
            map(Feed.start, feeds)
            for f in feeds:
                feed.send_one_way({'command' : 'download'})
            map(Feed.stop, feeds)