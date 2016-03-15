'''
    Copyright (c) 2016 Tim Savannah All Rights Reserved.

    Licensed under the Lesser GNU Public License Version 3, LGPLv3. You should have recieved a copy of this with the source distribution as
    LICENSE, otherwise it is available at https://github.com/kata198/func_timeout/LICENSE
'''

import sys
import threading
import time

__version__ = '1.0.0'
__version_tuple__ = (1, 0, 0)

__all__ = ('func_timeout', 'FunctionTimedOut')

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

    def funcwrap(args2, kwargs2):
        sys.stdout.write('Args2: %s\nkwargs2: %s\n' %(str(args2), str(kwargs2)))
        try:
            ret.append( func(*args2, **kwargs2) )
        except Exception as e:
            exception.append(e)

    thread = threading.Thread(target=funcwrap, args=(args, kwargs))

    thread.start()
    thread.join(timeout)

    if thread.isAlive():
        doRaiseCantStop = False
        thread.isDaemon = True
        try:
            if hasattr(thread, '_tstate_lock'):
                # 3.5
                thread._tstate_lock.release()
            elif hasattr(thread, '_Thread__stop'):
                # 2.7
                thread._Thread__stop()
            else:
                doRaiseCantStop = True
        except:
            pass
        if doRaiseCantStop is True:
            raise NotImplementedError('function timeouts not supported on this system.\n')

    if exception:
        raise exception[0]

    if ret:
        return ret[0]

    raise FunctionTimedOut('Function %s (args=%s) (kwargs=%s) timed out after %f seconds.\n' %(func.__name__, str(args), str(kwargs), timeout))

class FunctionTimedOut(Exception):
    pass
