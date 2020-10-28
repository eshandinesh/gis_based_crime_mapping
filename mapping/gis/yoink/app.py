import datetime, logging, sys

import baker

from .config_io import ConfigIO
from .feed import Feed
from .work_queue import work_queue

logger = logging.getLogger('yoink.app')

def initializeLogger(debug):
    logging.basicConfig(level=logging.DEBUG if debug else logging.WARNING,
                        stream=sys.stdout,
                        format='%(message)s')

@baker.command(default=True)
def update(config_file='~/.yoink.conf', preview=False, debug=False):
    '''Update all feeds, downloading new files as available, and
    updating the config file's timestamps appropriately.
    '''

    initializeLogger(debug)

    with ConfigIO(config_file, preview) as config:
        # Queue up the feeds
        for feed in config.feeds:
            work_queue.add_job(feed.update)

        # Wait for everything to finish
        work_queue.wait()

@baker.command
def list(config_file='~/.yoink.conf', debug=False):
    '''List all of the feeds currently configured.
    '''
    initializeLogger(debug)

    with ConfigIO(config_file, preview=True) as config:
        for idx, feed in enumerate(config.feeds):
            print(
                '[{id}] {name} -- {url}'.format(
                    id=idx,
                    name=feed.name,
                    url=feed.url)
                )

@baker.command
def add(config_file='~/.yoink.conf', debug=False):
    '''Add a new feed.
    '''

    initializeLogger(debug)

    name = raw_input('Name: ')
    url = raw_input('URL: ')
    folder = raw_input('Folder: ')

    name = 'feed:' + name

    with ConfigIO(config_file, preview=True) as config:
        f = Feed(
            name=name,
            url=url,
            folder=folder,
            timestamp=datetime.datetime(1900, 1, 1),
            config=config)
        config.feeds.append(f)

@baker.command
def remove(index, config_file='~/.yoink.conf', debug=False):
    '''Remove a feed.
    '''
    with ConfigIO(config_file, preview=True) as config:
        del config.feeds[int(index)]

def main():
    baker.run()

if __name__ == '__main__':
    main()