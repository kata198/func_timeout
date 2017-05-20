
# vim: set ts=4 sw=4 expandtab :

'''
    Copyright (c) 2017 Tim Savannah All Rights Reserved.

    Licensed under the Lesser GNU Public License Version 3, LGPLv3. You should have recieved a copy of this with the source distribution as
    LICENSE, otherwise it is available at https://github.com/kata198/func_timeout/LICENSE

    TestUtils.py - Common functions and types used across unit tests
'''

import copy
import sys
import time
import uuid

__all__ = ('ARG_NO_DEFAULT', 'getSleepLambda', 'getSleepLambdaWithArgs', 'compareTimes')

class ARG_NO_DEFAULT_TYPE(object):

    def __eq__(self, other):
        '''
            __eq__ - Equal operator ( == ). Returns True if both are instances of ARG_NO_DEFAULT_TYPE,
                or either is the type itself.

              @param other <anything, preferably an ARG_NO_DEFAULT_TYPE instance> - The other item to compare
                 against this item.

              @return <bool> - True if both objects are instances of ARG_NO_DEFAULT_TYPE,
                 or either are the type itself.
        '''
        
        # Is self == ARG_NO_DEFAULT_TYPE ever going to be True? Just in case...
        if issubclass(other.__class__, ARG_NO_DEFAULT_TYPE) or (other == ARG_NO_DEFAULT_TYPE or self == ARG_NO_DEFAULT_TYPE):
            return True

        return False

    def __ne__(self, other):
        '''
            __ne__ - Not-equal operator ( != ). Equivilant to not ==.

              @see ARG_NO_DEFAULT_TYPE.__eq__
        '''

        return not self.__eq__(other)

    def __cmp__(self, other):
        '''
            __cmp__ - Perform a "cmp" operation between self and other.

                Added for completeness, like python2 sorting etc.

              @param other <anything> - Another object, preferably one of ARG_NO_DEFAULT_TYPE.

              @return <int> -  Returns 0 if the objects are both 
                    equal (both instances of ARG_NO_DEFAULT_TYPE),
                     otherwise to prevent recursion in sorting etc, 
                     the id (location in memory) is compared.

        '''
        if self.__eq__(other):
            return 0

        if id(self) > id(other):
            return 1

        return -1

ARG_NO_DEFAULT = ARG_NO_DEFAULT_TYPE()

def getUniqueID(prefix):
    uniqueName = prefix + '_' + str(uuid.uuid4().hex)
    return uniqueName

def getSleepLambda(sleepTime):
    '''
        getSleepLambda - Get a lambda that takes two integer arguments (a, b) 
           and sleeps for a given number of seconds before returning the sum

          @param sleepTime <float> - The number of seconds to sleep

          @return lambda takes two integer argumennts, "a" and "b".

          NOTE: Lambda's are usually to functions, as functions may get their scope/closure overridden

          @see getSleepLambdaWithArgs
    '''

    # Ensure we don't get a strange reference override on somne versions of python
    _sleepTime = copy.copy(sleepTime) 

    

    return eval('''lambda a, b : int(bool(time.sleep(%f))) + a + b''' %(_sleepTime,))


def getSleepLambdaWithArgs(sleepTime, args):
    '''
        getSleepLambdaWithArgs - Get a lambda that takes a variable collection of arguments
           and sleeps for a given number of seconds before returning the sum of arguments

          @param sleepTime <float> - The number of seconds to sleep

          @param args list <tuple < str, (int) > - A list that represents the arguments to
            the returned lambda. Should be a list of tuples.
            
            The first tuple element is the name of the parameter. If a second paramater is present,
             it will be used as the default value for that argument.

             Keep in mind order is important ( i.e. no args with default following args without default),
              as they will be used in the order provided.

             All arguments should expect integer values.

          @return lambda with the provided arguments

          NOTE: Lambda's are usually to functions, as functions may get their scope/closure overridden

          @see getSleepLambda
    '''
    
    # Ensure we don't get a strange reference override on somne versions of python
    _sleepTime = copy.copy(sleepTime)

    if not args:
        raise ValueError('Empty "args" param. See docstring for usage details. Got: ' + repr(args))

    _args = copy.deepcopy(args)

    argStrs = []
    argNames = []
    for arg in _args:
        argNames.append(arg[0])

        if len(arg) == 1:
            argStrs.append(arg[0])
        else:
            argStrs.append('%s=%d' %( arg[0], arg[1] ) )

    argStr = ', '.join(argStrs)

    sumStr = ' + '.join(argNames)


#    print ( 'Function is: %s' %('''lambda %s : int(bool(time.sleep(%f))) + %s''' %(argStr, sleepTime, sumStr, )  ) )
    return eval('''lambda %s : int(bool(time.sleep(%f))) + %s''' % (argStr, sleepTime, sumStr, ) )


def compareTimes(timeEnd, timeStart, cmpTime, roundTo=None, deltaFixed=.05, deltaPct=None):
    '''
        compareTimes - Compare two times, with support for max error

        @param timeEnd <float> - End time
        @param timeStart<float> - Start time

        @param cmpTime <float> - Time to compare against

        @param roundTo <None/int> - Number of digits to round-off to

        @param deltaFixed <float/None> Default .05, If provided and if difference is within this much, the two values are considered equal
        @param deltaPct   <float/None> Default None, if provided and if difference is within this much, the two values are considered equal. 1 = 100%, .5 = 50%

        Example: if trying to determine if function ran for 2 seconds with an error of .05 seconds,

            if compareTimes( timeEnd, timeStart, 2, deltaFixed=.05, deltaPct=None) == 0

        @return <int> cmp style, < 0 if time delta is less than #cmpTime
                                 = 0 if time delta is equal (taking into account #deltaFixed and #deltaPct)
                                 > 0 if time delta is greater than #cmpTime
    '''
    
    timeDiff = timeEnd - timeStart

    delta = timeDiff - cmpTime
    if roundTo is not None:
        delta = round(delta, roundTo)
    absDelta = abs(delta)

    if deltaFixed and absDelta <= deltaFixed:
        return 0

    if deltaPct and absDelta <= (cmpTime * float(deltaPct)):
        return 0

    return delta

# vim: set ts=4 sw=4 expandtab :
