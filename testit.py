#!/usr/bin/env python

from func_timeout import func_timeout, set_timeout, FunctionTimedOut
import time
import sys

@set_timeout(2.5)
def doit(howmany):
    time.sleep(3)
    return 17 + howmany

if __name__ == '__main__':

    print ( "Should get return value of 23:" )
#    print ( "\tGot Return: %s\n" %(str(func_timeout(4, doit, args=(6,))),) )

    print ( "\nShould time out (exception):" )
    try:
        print ( "\tGot Return: %s\n", str(doit(16)) )
#        print ("\tGot Return: %s\n" %(str(func_timeout(4, doit, kwargs={'howmany' : 16})),))
    except FunctionTimedOut as e:
        sys.stderr.write('\tGot Exception: %s\n' %(str(e),))
        pass
