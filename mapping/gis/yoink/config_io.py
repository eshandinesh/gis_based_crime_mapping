'''Loading and saving of Config objects.
'''

import ConfigParser
import datetime, logging, os

from ordereddict import OrderedDict

from .config import Config
from .feed import Feed
from .util import fullpath

logger = logging.getLogger('yoink.config_io')


def _make_feed(config, cp, section):
    '''Construct a Feed object from the data in a feed: section of the
    config.
    '''
    assert section.startswith('feed:')

    # If the timestamp is not stored in the config file, then We
    # construct the earliest timestamp that datetime.datetime.strftime
    # will work with (for some reason it doesn't like years before
    # 1900.)
    try:
        timestamp = cp.get(section, 'timestamp')
        timestamp = datetime.datetime.strptime(
            cp.get(section, 'timestamp'),
            Feed.TIME_FORMAT)

        if timestamp.year < 1900:
            timestamp = datetime.datetime(1900, 1, 1)

    except ConfigParser.NoOptionError:
        timestamp = datetime.datetime(1900, 1, 1)

    return Feed(
        name=section,
        url=cp.get(section, 'url'),
        folder=fullpath(
            os.path.join(
                cp.get('config', 'folder'),
                cp.get(section, 'folder'))),
        timestamp=timestamp,
        config=config)


class ConfigIO(object):
    '''A context-manager for loading and saving Configs.

    Generally just use this as a context-manager. Note that the value
    bound in the with-statement when using a `ConfigIO` is a `Config`
    object, not the ConfigIO. For example::

      with ConfigIO(filename='my_config', preview=True) as config:
        ...

      # On non-exceptional __exit__, the ConfigIO saves the config.
    '''

    def __init__(self, filename, preview=False):
        self.config_file = fullpath(filename)
        self.cp = ConfigParser.ConfigParser(dict_type=OrderedDict)
        self.preview = preview

        logger.info('loading config file: {0}'.format(self.config_file))

        self.cp.read(self.config_file)

        self.config = Config(preview)

        # Make one Feed instance for each feed: section
        for section in (s for s in self.cp.sections() if s.startswith('feed:')):
            self.config.feeds.append(
                _make_feed(
                    self.config, self.cp, section))

    def add_feed(self, feed):
        self.cp.add_section(feed.name)
        self.cp.set(feed.name,
                    'url',
                    feed.url)
        self.cp.set(feed.name,
                    'folder',
                    feed.folder)
        self.cp.set(feed.name,
                    'timestamp',
                    feed.timestamp.strftime(Feed.TIME_FORMAT))

    def save(self):
        # clear old feeds
        for section in (s for s in self.cp.sections() if s.startswith('feed:')):
            self.cp.remove_section(section)

        for feed in self.config.feeds:
            self.add_feed(feed)

        # Save the config.
        with open(self.config_file, 'w') as f:
            logger.info('writing config file: {0}'.format(self.config_file))
            self.cp.write(f)

    def __enter__(self):
        return self.config

    def __exit__(self, t, v, tb):
        if not t: self.save()