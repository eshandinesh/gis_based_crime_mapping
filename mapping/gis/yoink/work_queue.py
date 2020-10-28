import threadpool

class WorkQueue(object):
    '''A simple thread-pool work queue implementation.
    '''
    def __init__(self):
        self.pool = threadpool.ThreadPool(10)

    def add_job(self, job):
        '''Add a new callable to the queue.

        Args:
          * j: A thunk (no-variable callable) that will be put in the
              work queue.
        '''
        self.pool.putRequest(threadpool.WorkRequest(job))

    def wait(self):
        '''Wait for the queue to be empty.
        '''
        self.pool.wait()

work_queue = WorkQueue()