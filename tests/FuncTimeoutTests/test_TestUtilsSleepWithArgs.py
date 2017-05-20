#!/usr/bin/env python
# vim: set ts=4 sw=4 expandtab :

'''
    Copyright (c) 2017 Tim Savannah All Rights Reserved.

    Licensed under the Lesser GNU Public License Version 3, LGPLv3. You should have recieved a copy of this with the source distribution as
    LICENSE, otherwise it is available at https://github.com/kata198/func_timeout/LICENSE
'''

import copy
import sys
import subprocess
import time

from func_timeout import func_timeout, FunctionTimedOut, func_set_timeout

from TestUtils import ARG_NO_DEFAULT, ARG_NO_DEFAULT_TYPE, getSleepLambda, getSleepLambdaWithArgs, compareTimes

class TestBasicSleepWithArgs(object):
    '''
        TestBasicSleepWithArgs - Perform test on the sleep generator with args function.

            Seperate file so runs in separate GoodTests process ( for performance reasons )
    '''


    def test_getSleepLambdaWithArgs(self):
        
        sleepLambda = getSleepLambdaWithArgs(2, [ ('a', ), ('b', ), ('c', 4) ] )
        startTime = time.time()
        try:
            sleepLambda(1, 2)
        except:
            raise AssertionError('Expected to have 1 default arg and 2 standard. Tried 3 args')
        endTime = time.time()

        assert compareTimes(endTime, startTime, 2, 2, deltaFixed=.1, deltaPct=None) == 0 , 'Expected getSleepLambdaWithArgs(2) to take 2 seconds.'

        try:
            sleepLambda(4, 7, 12)
        except:
            raise AssertionError('Expected to have 1 default arg and 2 standard. Tried 3 args.')



        expectedResult = 2 + 3
        sleepLambda = getSleepLambdaWithArgs(1.75, [ ('a', ), ('xxx', )] )
        startTime = time.time()
        try:
            result = sleepLambda(xxx=2, a=3)
        except:
            raise AssertionError('Expected to be able to use provided field names when calling function')
        endTime = time.time()

        assert result == expectedResult , 'Got wrong result'
        assert compareTimes(endTime, startTime, 1.75, 2, deltaFixed=.1, deltaPct=None) == 0 , 'Expected getSleepLambdaWithArgs(1.75) to take 1.75 seconds.'

        expectedResult = 5 + 13

        startTime = time.time()
        result = sleepLambda(5, 13)
        endTime = time.time()

        assert result == expectedResult , 'Did not get return from sleepFunction'
        assert compareTimes(endTime, startTime, 1.75, 2, deltaFixed=.1, deltaPct=None) == 0 , 'Expected getSleepLambda(1.75) to take 1.75 seconds.'
    
if __name__ == '__main__':
    sys.exit(subprocess.Popen('GoodTests.py -n1 "%s" %s' %(sys.argv[0], ' '.join(['"%s"' %(arg.replace('"', '\\"'), ) for arg in sys.argv[1:]]) ), shell=True).wait())

# vim: set ts=4 sw=4 expandtab :
