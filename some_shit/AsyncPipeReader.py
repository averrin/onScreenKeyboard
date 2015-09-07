__author__ = 'tsa'

class AsyncPipeReader(threading.Thread):
    '''
    Helper class to implement asynchronous reading of a pipe
    in a separate thread. Pushes read lines on a queue to
    be consumed in another thread.
    '''

    def __init__(self, my_pipe, queue):
        assert isinstance(queue, Queue.Queue)
        assert callable(my_pipe.readline)
        threading.Thread.__init__(self)
        self._pipe = my_pipe
        self._queue = queue

    def run(self):
        '''The body of the tread: read lines and put them on the queue.'''
        for line in iter(self._pipe.readline, ''):
            self._queue.put(line)

    def eof(self):
        '''Check whether there is no more content to expect.'''
        return not self.is_alive() and self._queue.empty()