#!/usr/bin/env python

from func_timeout import func_timeout, FunctionTimedOut
import time
import sys


def doit(howmany):
    time.sleep(2)
    return 17 + howmany

if __name__ == '__main__':

    print ( "Should get return value of 23:" )
    print ( "\tGot Return: %s\n" %(str(func_timeout(4, doit, args=(6,))),) )

    print ( "\nShould time out (exception):" )
    myException = None
    try:
        print ("\tGot Return: %s\n" %(str(func_timeout(1, doit, kwargs={'howmany' : 16})),))
    except FunctionTimedOut as e:
        sys.stderr.write('\tGot Exception: %s\n' %(str(e),))
        myException = e
        pass

    if myException is not None:
        print ( "\nGot: %s\n" %( str(myException.retry(2.5)), ) )
    else:
        sys.stderr.write('Did not get exception before?\n')
