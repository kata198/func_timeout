'''
    Copyright (c) 2016, 2017 Tim Savannah All Rights Reserved.

    Licensed under the Lesser GNU Public License Version 3, LGPLv3. You should have recieved a copy of this with the source distribution as
    LICENSE, otherwise it is available at https://github.com/kata198/func_timeout/LICENSE
'''
import threading
import time

from .exceptions import FunctionTimedOut
from .StoppableThread import StoppableThread

__all__ = ('set_timeout', 'func_timeout')


def set_timeout(timeout):
    '''
        set_timeout - Wrapper to run a function with a given timeout (max execution time)

        @param timeout <float> - Number of seconds max to allow function to execute

        @throws FunctionTimedOut If time alloted passes without function returning naturally

        @see func_timeout
        @see set_modifiable_timeout
    '''
    def _function_decorator(func):
        def _function_wrapper(*args, **kwargs):
            return func_timeout(timeout, func, args=args, kwargs=kwargs)
        return _function_wrapper

    return _function_decorator

def set_modifiable_timeout(timeout):
    '''
        set_modifiable_timeout - Wrapper to run a function with a given timeout (max execution time)
            which can be overriden by passing "forceTimeout" to the function being decorated

        @param timeout <float> - Default Number of seconds max to allow function to execute

        @throws FunctionTimedOut If time alloted passes without function returning naturally

        @see func_timeout
        @see set_timeout
    '''
    def _function_decorator(func):
        def _function_wrapper(*args, **kwargs):
            if 'forceTimeout' in kwargs:
                useTimeout = kwargs.pop('forceTimeout')
            else:
                useTimeout = timeout

            return func_timeout(useTimeout, func, args=args, kwargs=kwargs)
        return _function_wrapper
    return _function_decorator

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


