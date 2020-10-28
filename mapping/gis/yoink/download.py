import logging, os, urllib, urlparse

from .work_queue import work_queue

logger = logging.getLogger('yoink.download')

def _download(url, folder):
    '''Download a single url.
    '''
    #if self.config.preview:
    #    logger.info('[PREVIEW] Downloading {0}'.format(url))
    #    return

    try:
        os.makedirs(folder)
    except OSError:
        pass

    filename = os.path.split(
        urlparse.urlparse(url).path)[1]

    dest = os.path.join(folder, filename)

    logger.info('Downloading {0} to {1}'.format(url, dest))

    try:
        urllib.urlretrieve(url, dest)

    except Exception as e:
        logger.error('Error downloading entry {0}: {1}'.format(url, e))

def download(url, folder):
    '''Schedule the download of a URL.

    This just puts a new item in the work queue.

    Args:
      * url: The URL to download.
      * The folder into which to save the URL.
    '''
    work_queue.add_job(
        lambda : _download(url, folder))