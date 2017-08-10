#!/usr/bin/env python
# vim: set ts=4 sw=4 expandtab :

'''
    Copyright (c) 2017 Tim Savannah All Rights Reserved.

    Licensed under the Lesser GNU Public License Version 3, LGPLv3. You should have recieved a copy of this with the source distribution as
    LICENSE, otherwise it is available at https://github.com/kata198/func_timeout/LICENSE
'''

import copy
import gc
import sys
import time
import threading
import subprocess

from func_timeout import func_timeout, FunctionTimedOut, func_set_timeout

from TestUtils import ARG_NO_DEFAULT, getSleepLambda, getSleepLambdaWithArgs, compareTimes

SLEEP_TIME = .5

def doSleep(a, b):
    time.sleep(a)
    return a + b

def calculateSleep(a, b):
    return a * 1.15

class TestDecorator(object):
    '''
        TestDecorator - Perform tests using the func_set_timeout wrapper
    '''

    

    def test_funcSetTimeout(self):
        
        @func_set_timeout(SLEEP_TIME)
        def doSleepFunc(a, b):
            time.sleep(a)
            return a + b

        expected = SLEEP_TIME * 1.3 + 4
        gotException = False
        startTime = time.time()
        try:
            result = doSleepFunc(SLEEP_TIME * 1.3, 4)
        except FunctionTimedOut as fte:
            gotException = True
        endTime = time.time()

        assert gotException , 'Expected to get exception at sleep time'
        assert compareTimes(endTime, startTime, SLEEP_TIME, None, .1) == 0 , 'Expected to sleep up to sleep time'

        expected = SLEEP_TIME * .8 + 4
        gotException = False
        startTime = time.time()
        try:
            result = doSleepFunc(SLEEP_TIME * .8, 4)
        except FunctionTimedOut as fte:
            gotException = True
        endTime = time.time()

        assert not gotException , 'Expected not to get exception at 80% sleep time'
        assert compareTimes(endTime, startTime, SLEEP_TIME * .8, None, .1) == 0 , 'Expected to only sleep for 80% of sleep time'
        assert result == expected , 'Got wrong result'

    def test_funcSetTimeoutOverride(self):
        @func_set_timeout(SLEEP_TIME, allowOverride=True)
        def doSleepFunc(a, b):
            time.sleep(a)
            return a + b

        expected = SLEEP_TIME * 1.3 + 4
        gotException = False
        startTime = time.time()
        try:
            result = doSleepFunc(SLEEP_TIME * 1.3, 4, forceTimeout=SLEEP_TIME * 1.2)
        except FunctionTimedOut as fte:
            gotException = True
        except Exception as e:
            raise AssertionError('Expected to be able to override forceTimeout when allowOverride=True')
        endTime = time.time()

        assert gotException , 'Expected to get exception at 130% sleep time'
        assert compareTimes(endTime, startTime, SLEEP_TIME * 1.2, None, .1) == 0 , 'Expected to sleep up to 120% of sleep time'

        @func_set_timeout(SLEEP_TIME, allowOverride=False)
        def doSleepFuncNoOverride(a, b):
            time.sleep(a)
            return a + b

        gotException = False
        try:
            doSleepFuncNoOverride(SLEEP_TIME * 1.3, 4, forceTimeout=SLEEP_TIME * 1.2)
        except Exception as e:
            gotException = True
        except FunctionTimedOut as fte:
            raise AssertionError('Expected to NOT be able to pass forceTimeout when allowOverride=False, but got FunctionTimedOut exception')

        assert gotException , 'Expected to NOT be able to pass forceTimeout when allowOverride=False, but did not get exception'
            

        expected = SLEEP_TIME + 4
        gotException = False
        startTime = time.time()
        try:
            result = doSleepFunc(SLEEP_TIME, 4, forceTimeout=SLEEP_TIME * 1.15)
        except FunctionTimedOut as fte:
            gotException = True
        endTime = time.time()

        assert not gotException , 'Expected not to get exception with forced 115% sleep time'
        assert compareTimes(endTime, startTime, SLEEP_TIME, None, .1) == 0 , 'Expected to sleep for SLEEP_TIME'
        assert result == expected , 'Got wrong result'

    def test_funcSetTimeCalculate(self):

        def calculateSleepOver(a, b):
            return a * 1.2

        def calculateSleepUnder(a, b):
            return a * .8

        def calculateSleepOverArgs(*args, **kwargs):
            return args[0] * 1.2

        def calculateSleepUnderArgs(*args, **kwargs):
            return args[0] * .8

        @func_set_timeout(calculateSleepOver, allowOverride=False)
        def doSleepFuncOver(a, b):
            time.sleep(a)
            return a + b

        expected = SLEEP_TIME + 4
        gotException = False
        startTime = time.time()
        try:
            result = doSleepFuncOver(SLEEP_TIME, 4)
        except FunctionTimedOut as fte:
            gotException = True
        endTime = time.time()

        assert not gotException , 'Expected not to get exception with calculated 120% timeout on sleep time'
        assert compareTimes(endTime, startTime, SLEEP_TIME, None, .1) == 0 , 'Expected to sleep for SLEEP_TIME'
        assert result == expected , 'Got wrong result'

        
        @func_set_timeout(calculateSleepUnder, allowOverride=False)
        def doSleepFuncUnder(a, b):
            time.sleep(a)
            return a + b

        expected = SLEEP_TIME + 4
        gotException = False
        startTime = time.time()
        try:
            result = doSleepFuncUnder(SLEEP_TIME, 4)
        except FunctionTimedOut as fte:
            gotException = True
        endTime = time.time()

        assert gotException , 'Expected to get exception with calculated 80% timeout on sleep time'
        assert compareTimes(endTime, startTime, SLEEP_TIME * .8, None, .1) == 0 , 'Expected to sleep for 80% SLEEP_TIME'

        @func_set_timeout(calculateSleepOverArgs, allowOverride=False)
        def doSleepFuncOverArgs(a, b):
            time.sleep(a)
            return a + b

        expected = SLEEP_TIME + 4
        gotException = False
        startTime = time.time()
        try:
            result = doSleepFuncOverArgs(SLEEP_TIME, 4)
        except FunctionTimedOut as fte:
            gotException = True
        endTime = time.time()

        assert not gotException , 'Expected not to get exception with calculated 120% timeout on sleep time using *args'
        assert compareTimes(endTime, startTime, SLEEP_TIME, None, .1) == 0 , 'Expected to sleep for SLEEP_TIME using *args'
        assert result == expected , 'Got wrong result'

        @func_set_timeout(calculateSleepUnderArgs, allowOverride=False)
        def doSleepFuncUnderArgs(a, b):
            time.sleep(a)
            return a + b

        expected = SLEEP_TIME + 4
        gotException = False
        startTime = time.time()
        try:
            result = doSleepFuncUnderArgs(SLEEP_TIME, 4)
        except FunctionTimedOut as fte:
            gotException = True
        endTime = time.time()

        assert gotException , 'Expected to get exception with calculated 80% timeout on sleep time using *args'
        assert compareTimes(endTime, startTime, SLEEP_TIME * .8, None, .1) == 0 , 'Expected to sleep for 80% SLEEP_TIME using *args'


    def test_funcSetTimeCalculateWithOverride(self):

        def calculateSleepOver(a, b):
            return a * 1.2

        def calculateSleepUnder(a, b):
            return a * .8

        def calculateSleepOverArgs(*args, **kwargs):
            return args[0] * 1.2

        def calculateSleepUnderArgs(*args, **kwargs):
            return args[0] * .8

        @func_set_timeout(calculateSleepOver, allowOverride=True)
        def doSleepFuncOver(a, b):
            time.sleep(a)
            return a + b

        expected = SLEEP_TIME + 4
        gotException = False
        startTime = time.time()
        try:
            result = doSleepFuncOver(SLEEP_TIME, 4)
        except FunctionTimedOut as fte:
            gotException = True
        endTime = time.time()

        assert not gotException , 'Expected not to get exception with calculated 120% timeout on sleep time'
        assert compareTimes(endTime, startTime, SLEEP_TIME, None, .1) == 0 , 'Expected to sleep for SLEEP_TIME'
        assert result == expected , 'Got wrong result'

        expected = SLEEP_TIME + 4
        gotException = False
        startTime = time.time()
        try:
            result = doSleepFuncOver(SLEEP_TIME, 4, forceTimeout= SLEEP_TIME * 1.5)
        except FunctionTimedOut as fte:
            gotException = True
        endTime = time.time()

        assert not gotException , 'Expected not to get exception with calculated 120% timeout on sleep time but 150% timeout on override'
        assert compareTimes(endTime, startTime, SLEEP_TIME, None, .1) == 0 , 'Expected to sleep for SLEEP_TIME with 150% timeout on override'
        assert result == expected , 'Got wrong result'

        
        expected = SLEEP_TIME + 4
        gotException = False
        startTime = time.time()
        try:
            result = doSleepFuncOver(SLEEP_TIME, 4, forceTimeout=SLEEP_TIME * .7)
        except FunctionTimedOut as fte:
            gotException = True
        endTime = time.time()

        assert gotException , 'Expected to get exception with calculated 120% timeout on sleep time but 70% timeout on override'
        assert compareTimes(endTime, startTime, SLEEP_TIME * .7, None, .1) == 0 , 'Expected to sleep for 70% SLEEP_TIME with 70% timeout on override'
        
        
        @func_set_timeout(calculateSleepUnder, allowOverride=True)
        def doSleepFuncUnder(a, b):
            time.sleep(a)
            return a + b

        expected = SLEEP_TIME + 4
        gotException = False
        startTime = time.time()
        try:
            result = doSleepFuncUnder(SLEEP_TIME, 4)
        except FunctionTimedOut as fte:
            gotException = True
        endTime = time.time()

        assert gotException , 'Expected to get exception with calculated 80% timeout on sleep time'
        assert compareTimes(endTime, startTime, SLEEP_TIME * .8, None, .1) == 0 , 'Expected to sleep for 80% SLEEP_TIME'

        expected = SLEEP_TIME + 4
        gotException = False
        startTime = time.time()
        try:
            result = doSleepFuncUnder(SLEEP_TIME, 4, forceTimeout=SLEEP_TIME * 1.2)
        except FunctionTimedOut as fte:
            gotException = True
        endTime = time.time()

        assert not gotException , 'Expected not to get exception with calculated 80% timeout on sleep time but 120% timeout on override'
        assert compareTimes(endTime, startTime, SLEEP_TIME , None, .1) == 0 , 'Expected to sleep for SLEEP_TIME with 120% timeout on override'


    def test_setFuncTimeoutetry(self):
        def calculateSleepOver(a, b):
            return a * 1.2

        def calculateSleepUnder(a, b):
            return a * .8

        def calculateSleepOverArgs(*args, **kwargs):
            return args[0] * 1.2

        def calculateSleepUnderArgs(*args, **kwargs):
            return args[0] * .8

        @func_set_timeout(calculateSleepUnder, allowOverride=True)
        def doSleepFuncUnder(a, b):
            time.sleep(a)
            return a + b


        expected = SLEEP_TIME + 4
        gotException = False
        functionTimedOut = None
        startTime = time.time()
        try:
            result = doSleepFuncUnder(SLEEP_TIME, 4)
        except FunctionTimedOut as fte:
            gotException = True
            functionTimedOut = fte
        endTime = time.time()

        assert gotException , 'Expected to get exception with calculated 80% timeout'
        assert compareTimes(endTime, startTime, SLEEP_TIME * .8, None, .1) == 0 , 'Expected to sleep for 80% SLEEP_TIME with 80% timeout'

        gotException = False
        startTime = time.time()
        try:
            functionTimedOut.retry()
        except FunctionTimedOut as fte2:
            gotException = True
        except Exception as e:
            raise AssertionError('Got exception trying to retry with same timeout:  < %s > : %s' %(e.__name__, str(e)))
        endTime = time.time()

        assert gotException , 'Expected to get exception with calculated same 80% timeout on retry'
        assert compareTimes(endTime, startTime, SLEEP_TIME * .8, None, .1) == 0 , 'Expected to sleep for 80% SLEEP_TIME with same 80% timeout on retry'

        result = None
        gotException = False
        startTime = time.time()
        try:
            result = functionTimedOut.retry(None)
        except FunctionTimedOut as fte2:
            gotException = True
        except Exception as e:
            raise AssertionError('Got exception trying to retry with same timeout:  < %s > : %s' %(e.__name__, str(e)))
        endTime = time.time()

        assert not gotException , 'Expected to get exception with calculated 80% timeout on retry ( None ) [ No timeout ]'
        assert compareTimes(endTime, startTime, SLEEP_TIME, None, .1) == 0 , 'Expected to sleep for 100% SLEEP_TIME with 80% timeout overriden on retry ( None ) [ No timeout ]'
        assert result == expected , 'Got wrong result'



        gotException = False
        startTime = time.time()
        try:
            functionTimedOut.retry(SLEEP_TIME * .6)
        except FunctionTimedOut as fte2:
            gotException = True
        except Exception as e:
            raise AssertionError('Got exception trying to retry with same timeout:  < %s > : %s' %(e.__name__, str(e)))
        endTime = time.time()

        assert gotException , 'Expected to get exception with calculated 80% timeout overriden by 60% timeout on retry'
        assert compareTimes(endTime, startTime, SLEEP_TIME * .6, None, .1) == 0 , 'Expected to sleep for 60% SLEEP_TIME with 80% timeout overriden on retry ( SLEEP_TIME * .6 ) [ 60% timeout ]'
        
        result = None
        gotException = False
        startTime = time.time()
        try:
            result = functionTimedOut.retry(SLEEP_TIME * 1.5)
        except FunctionTimedOut as fte2:
            gotException = True
        except Exception as e:
            raise AssertionError('Got exception trying to retry with same timeout:  < %s > : %s' %(e.__name__, str(e)))
        endTime = time.time()

        assert not gotException , 'Expected to get exception with calculated 80% timeout overriden by 150% timeout on retry'
        assert compareTimes(endTime, startTime, SLEEP_TIME , None, .1) == 0 , 'Expected to sleep for 100% SLEEP_TIME with 80% timeout overriden on retry ( SLEEP_TIME * 1.5 ) [ 150% timeout ]'
        assert result == expected
        
        threadsCleanedUp = False

        for i in range(5):
            time.sleep(1)
            gc.collect()

            if threading.active_count() == 1:
                threadsCleanedUp = True
                break

                
        assert threadsCleanedUp , 'Expected other threads to get cleaned up after gc collection'
    
    def test_nameRetained(self):
        
        # Case of just timeout
        @func_set_timeout(2, allowOverride=False)
        def hello():
            pass

        assert hello.__name__ == 'hello'

        del hello
        
        def getTimeoutFunc():
            return 2

        # Timeout is function
        @func_set_timeout(getTimeoutFunc, allowOverride=False)
        def hello2():
            pass

        assert hello2.__name__ == 'hello2'

        del hello2

        # Now the same with allowOverride=True

        @func_set_timeout(2, allowOverride=True)
        def hello3():
            pass

        assert hello3.__name__ == 'hello3'

        del hello3

        @func_set_timeout(getTimeoutFunc, allowOverride=True)
        def hello4():
            pass

        assert hello4.__name__ == 'hello4'


if __name__ == '__main__':
    sys.exit(subprocess.Popen('GoodTests.py -n1 "%s" %s' %(sys.argv[0], ' '.join(['"%s"' %(arg.replace('"', '\\"'), ) for arg in sys.argv[1:]]) ), shell=True).wait())

# vim: set ts=4 sw=4 expandtab :
