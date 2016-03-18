import threading
import time

from .exceptions import FunctionTimedOut
from .StoppableThread import StoppableThread

def func_timeout(timeout, func, args=(), kwargs=None):
    '''
        func_timeout - Runs the given function for up to #timeout# seconds.

        Raises any exceptions #func# would raise, returns what #func# would return (unless timeout is exceeded), in which case it raises FunctionTimedOut

        @param timeout <float> - Maximum number of seconds to run #func# before terminating
        @param func <function> - The function to call
        @param args    <tuple> - Any ordered arguments to pass to the function
        @param kwargs  <dict/None> - Keyword arguments to pass to the function.

        @raises - FunctionTimedOut if #timeout# is exceeded, otherwise anything #func# could raise will be raised

        @return - The return value that #func# gives
    '''

    if not kwargs:
        kwargs = {}
    if not args:
        args = ()

    ret = []
    exception = []
    isStopped = False

    def funcwrap(args2, kwargs2):
        try:
            ret.append( func(*args2, **kwargs2) )
        except Exception as e:
            if isStopped is False:
                # Don't capture stopping exception
                exception.append(e)

    thread = StoppableThread(target=funcwrap, args=(args, kwargs))
    thread.daemon = True

    thread.start()
    thread.join(timeout)

    stopException = None
    if thread.isAlive():
        isStopped = True
        stopException = FunctionTimedOut('Function %s (args=%s) (kwargs=%s) timed out after %f seconds.\n' %(func.__name__, str(args), str(kwargs), timeout))
        thread._stopThread(stopException)
        thread.join(.1)
        raise stopException

    if exception:
        raise exception[0]

    if ret:
        return ret[0]


