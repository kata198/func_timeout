'''
    Copyright (c) 2016 Tim Savannah All Rights Reserved.

    Licensed under the Lesser GNU Public License Version 3, LGPLv3. You should have recieved a copy of this with the source distribution as
    LICENSE, otherwise it is available at https://github.com/kata198/func_timeout/LICENSE
'''
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

        If the timeout is exceeded, FunctionTimedOut will be raised within the context of the called function every two seconds until it terminates,
        but will not block the calling thread (a new thread will be created to perform the join). If possible, you should try/except FunctionTimedOut
        to return cleanly, but in most cases it will 'just work'.

        Be careful of code like:
        def myfunc():
            while True:
                try:
                    dosomething()
                except Exception:
                    continue

        because it will never terminate.

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
        stopException = FunctionTimedOut 
        thread._stopThread(stopException)
        thread.join(.1)
        raise FunctionTimedOut('Function %s (args=%s) (kwargs=%s) timed out after %f seconds.\n' %(func.__name__, str(args), str(kwargs), timeout))

    if exception:
        raise exception[0]

    if ret:
        return ret[0]


