import ConfigParser
import datetime, logging, os

from .feed import Feed
from .util import fullpath

logger = logging.getLogger('yoink.config')

class Config(object):
    '''Represents set of feeds to read and the parameters used to
    manage their reading.

    Args:
      * preview: Whether operations should be performed in "preview"
          mode (i.e. nothing is actually done.)
    '''

    def __init__(self, preview, feeds=None):
        self.preview = preview

        # Make one Feed instance for each feed: section
        self.feeds = feeds or []