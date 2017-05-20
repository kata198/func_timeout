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

class TestTestUtils(object):
    '''
        TestTestUtils - Perform tests using the basic func_timeout function
    '''


    def test_ArgNoDefault(self):
        
        assert ARG_NO_DEFAULT == ARG_NO_DEFAULT , 'Expected ARG_NO_DEFAULT to equal itself'
        assert (ARG_NO_DEFAULT != ARG_NO_DEFAULT) is False , 'Expected ARG_NO_DEFAULT to not not equal itself'

    
        assert ARG_NO_DEFAULT == ARG_NO_DEFAULT_TYPE , 'Expected ARG_NO_DEFAULT to equal ARG_NO_DEFAULT_TYPE'
        assert ARG_NO_DEFAULT_TYPE == ARG_NO_DEFAULT , '2Expected ARG_NO_DEFAULT to equal ARG_NO_DEFAULT_TYPE'

        otherInstance = ARG_NO_DEFAULT_TYPE()

        assert otherInstance == ARG_NO_DEFAULT , 'Assert ARG_NO_DEFAULT_TYPE instances equal eachother'
        assert not (otherInstance != ARG_NO_DEFAULT) , 'Assert ARG_NO_DEFAULT_TYPE instances not not-equal eachother'


    def test_compareTimes(self):

        startTime = 50.00
        endTime   = 52.03

        assert compareTimes(endTime, startTime, 2, roundTo=2, deltaFixed=.05, deltaPct=None) == 0 , 'Expected deltaFixed to be > abs(delta) to show times equal'

        assert compareTimes(endTime, startTime, 2, roundTo=2, deltaFixed=.01, deltaPct=None) == .03 , 'Expected when deltaFixed is less than the abs delta, actual diff to be returned.'

        assert compareTimes(endTime, startTime, 2, roundTo=2, deltaFixed=None, deltaPct=.2) == 0 , 'Expected deltaPct * cmpTime when greater than abs delta to be equal'

        assert compareTimes(endTime, startTime, 2, roundTo=2, deltaFixed=None, deltaPct=.0002) == .03 , 'Expected deltaPct * cmpTime when less than abs delta to be actual diff'


if __name__ == '__main__':
    sys.exit(subprocess.Popen('GoodTests.py -n1 "%s" %s' %(sys.argv[0], ' '.join(['"%s"' %(arg.replace('"', '\\"'), ) for arg in sys.argv[1:]]) ), shell=True).wait())

# vim: set ts=4 sw=4 expandtab :
