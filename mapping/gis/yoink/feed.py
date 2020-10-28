import ConfigParser, datetime, logging, os, time

import feedparser

from .download import download
from .util import catching

logger = logging.getLogger('yoink.feed')


class Feed(object):
    '''Represents a single feed from which files are downloaded.
    '''
    TIME_FORMAT = '%Y-%m-%dT%H:%M:%S'

    def __init__(self,
                 name,
                 url,
                 folder,
                 timestamp,
                 config):
        self.name = name
        self.url = url
        self.folder = folder
        self.timestamp = timestamp
        self.config = config

    @catching(handler=lambda e: logger.error('Error processing feed: {0}'.format(e)))
    def update(self):
        '''Read latest feed data and schedule new files for download.
        '''
        logger.info('reading feed: {0}'.format(self.url))

        # read the feed
        parsed = feedparser.parse(self.url)

        # grab the entries
        entries = parsed['entries']

        # filter out entries older than the feed timestamp
        entries = filter(lambda e: e['updated_parsed'][:8] > self.timestamp.timetuple()[:8],
                         entries)

        # process each entry (in timestamp order)
        map(self.process_entry, entries)

    @catching(exception_type=KeyError, handler=lambda e: logger.error('Entry is missing a field: {0}'.format(e)))
    def process_entry(self, entry):
        '''Look for all enclosures in `entry` and download anything
        that meets the Feed's criteria.
        '''

        # Download the entry if it's timestamp is greater than the
        # feed's
        for enc in entry['enclosures']:
            if enc['type'].startswith('audio/'):
                url = enc['href']

                if self.config.preview:
                    logger.info('[PREVIEW] Downloading {0}'.format(url))

                else:
                    # Schedule the URL for download
                    download(url, self.folder)

                    # Update the feed's timestamp
                    self.timestamp = max(
                        self.timestamp,
                        datetime.datetime.strptime(
                            time.strftime(
                                Feed.TIME_FORMAT,
                                entry['updated_parsed']),
                            Feed.TIME_FORMAT))