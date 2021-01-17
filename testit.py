#!/usr/bin/env python
'''
    testit.py - Example code for ad-hoc function timeouts.

        Newer tests for all features found in "tests" directory.
'''

from func_timeout import func_timeout, FunctionTimedOut
import time
import sys


def doit(howmany):
    time.sleep(2)
    return 17 + howmany

if __name__ == '__main__':

    print ( "Should get return value of 23:" )
    print ( f"\tGot Return: {str(func_timeout(4, doit, args=(6,)))}\n" )

    print ( "\nShould time out (exception):" )
    myException = None
    try:
        print (f"\tGot Return: {str(func_timeout(1, doit, kwargs={'howmany': 16}))}\n")
    except FunctionTimedOut as e:
        sys.stderr.write(f'\tGot Exception: {str(e)}\n')
        myException = e
        pass

    print ( "\nRetrying with longer timeout, should get 16+17=33:" )
    if myException is not None:
        print ( f"\nGot: {str(myException.retry(2.5))}\n" )
    else:
        sys.stderr.write('Did not get exception before?\n')
