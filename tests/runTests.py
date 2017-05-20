#!/usr/bin/env python
#
#  Copyright (c) 2015, 2016, 2017 Tim Savannah under following terms:
#   You may modify and redistribe this script with your project
#
# It will download the latest GoodTests.py and use it to execute the tests.
#
#  This should be placed in a directory, "tests", at the root of your project. It assumes that ../$MY_PACKAGE_MODULE is the path to your test module, and will create a symlink to it in order to run tests.
#  The tests should be found in $MY_TEST_DIRECTORY in given "tests" folder.


# NOTE: Since version 1.2.3, you can also import this (like from a graphical application) and call the "main()" function.
#  All of the following globals are the defaults,  but can be overridden when calling main() (params have the same name as the globals).

import imp
import os

import subprocess
import sys

# URL to current version of GoodTests.py - You only need to change this if you host an internal copy.
GOODTESTS_URL = 'https://raw.githubusercontent.com/kata198/GoodTests/master/GoodTests.py'

# This should be your module name, and can be any relative or absolute path, or just a module name. 
# If just a module name is given, the directory must be in current directory or parent directory.
MY_PACKAGE_MODULE = 'func_timeout'

#  Normally, you want to test the codebase during development, so you don't care about the site-packages installed version.
#     If you want to allow testing with any module by @MY_PACKAGE_MODULE in the python path, change this to True.
ALLOW_SITE_INSTALL = False

# This is the test directory that should contain all your tests. This should be a directory in your "tests" folder
MY_TEST_DIRECTORY = 'FuncTimeoutTests'

__version__ = '2.1.1'
__version_tuple__ = (2, 1, 1)

def findGoodTests():
    '''
        findGoodTests - Tries to find GoodTests.py

        @return <dict> {
            'path' <str> -> Path to GoodTests.py (for execution)
            'success' <bool> -> True/False if we successfully found GoodTests.py
        }
    '''
    pathSplit = os.environ['PATH'].split(':')
    if '.' not in pathSplit:
        pathSplit = ['.'] + pathSplit
        os.environ['PATH'] = ':'.join(pathSplit)

    result = ''
    success = False
    for path in pathSplit:
        if path.endswith('/'):
            path = path[:-1]
        guess = path + '/GoodTests.py'
        if os.path.exists(guess):
            success = True
            result = guess
            break

    return {
        'path'    : result,
        "success" : success 
    }

def try_pip_install():
    pipe = subprocess.Popen('pip install GoodTests', shell=True)
    res = pipe.wait()
    
    return res

def download_goodTests(GOODTESTS_URL=None):
    '''
        download_goodTests - Attempts to download GoodTests, using the default global url (or one provided).
    
        @return <int> - 0 on success (program should continue), otherwise non-zero (program should abort with this exit status)
    '''
    if GOODTESTS_URL is None:
        GOODTESTS_URL = globals()['GOODTESTS_URL']

    validAnswer = False
    while validAnswer == False:
        sys.stdout.write('GoodTests not found. Would you like to install it to local folder? (y/n): ')
        sys.stdout.flush()
        answer = sys.stdin.readline().strip().lower()
        if answer not in ('y', 'n', 'yes', 'no'):
            continue
        validAnswer = True
        answer = answer[0]

    if answer == 'n':
        sys.stderr.write('Cannot run tests without installing GoodTests. http://pypi.python.org/pypi/GoodTests or https://github.com/kata198/Goodtests\n')
        return 1
    try:
        import urllib2 as urllib
    except ImportError:
        try:
            import urllib.request as urllib
        except:
            sys.stderr.write('Failed to import urllib. Trying pip.\n')
            res = try_pip_install()
            if res != 0:
                sys.stderr.write('Failed to install GoodTests with pip or direct download. aborting.\n')
                return 1
    try:
        response = urllib.urlopen(GOODTESTS_URL)
        contents = response.read()
        if str != bytes:
            contents = contents.decode('ascii')
    except Exception as e:
        sys.stderr.write('Failed to download GoodTests.py from "%s"\n%s\n' %(GOODTESTS_URL, str(e)))
        sys.stderr.write('\nTrying pip.\n')
        res = try_pip_install()
        if res != 0:
            sys.stderr.write('Failed to install GoodTests with pip or direct download. aborting.\n')
            return 1
    try:
        with open('GoodTests.py', 'w') as f:
            f.write(contents)
    except Exception as e:
        sys.stderr.write('Failed to write to GoodTests.py\n%s\n' %(str(e,)))
        return 1
    try:
        os.chmod('GoodTests.py', 0o775)
    except:
        sys.stderr.write('WARNING: Failed to chmod +x GoodTests.py, may not be able to be executed.\n')

    try:
        import GoodTests
    except ImportError:
        sys.stderr.write('Seemed to download GoodTests okay, but still cannot import. Aborting.\n')
        return 1

    return 0


def main(thisDir=None, additionalArgs=[], MY_PACKAGE_MODULE=None, ALLOW_SITE_INSTALL=None, MY_TEST_DIRECTORY=None, GOODTESTS_URL=None):
    '''
        Do the work - Try to find GoodTests.py, else prompt to download it, then run the tests.

        @param thisDir <None/str> - None to use default (directory this test file is in, or if not obtainable, current directory).
        @param additionalArgs <list> - Any additional args to pass to GoodTests.py

        Remainder of params take their global (top of file) defaults unless explicitly set here. See top of file for documentation.

        @return <int> - Exit code of application. 0 on success, non-zero on failure.

            TODO: Standardize return codes so external applications can derive failure without parsing error strings.
    '''

    if MY_PACKAGE_MODULE is None:
        MY_PACKAGE_MODULE = globals()['MY_PACKAGE_MODULE']
    if ALLOW_SITE_INSTALL is None:
        ALLOW_SITE_INSTALL = globals()['ALLOW_SITE_INSTALL']
    if MY_TEST_DIRECTORY is None:
        MY_TEST_DIRECTORY = globals()['MY_TEST_DIRECTORY']
    if GOODTESTS_URL is None:
        GOODTESTS_URL = globals()['GOODTESTS_URL']
   

    if not thisDir:
        thisDir = os.path.dirname(__file__)

    if not thisDir:
        thisDir = str(os.getcwd())
    elif not thisDir.startswith('/'):
        thisDir = str(os.getcwd()) + '/' + thisDir

    # If GoodTests is in current directory, make sure we find it later
    if os.path.exists('./GoodTests.py'):
        os.environ['PATH'] = str(os.getcwd()) + ':' + os.environ['PATH']

    os.chdir(thisDir)

    goodTestsInfo = findGoodTests()
    if goodTestsInfo['success'] is False:
        downloadRet = download_goodTests(GOODTESTS_URL)
        if downloadRet != 0:
            return downloadRet
        goodTestsInfo = findGoodTests()
        if goodTestsInfo['success'] is False:
            sys.stderr.write('Could not download or find GoodTests.py. Try to download it yourself using "pip install GoodTests", or wget %s\n' %( GOODTESTS_URL,))
            return 1

    baseName = os.path.basename(MY_PACKAGE_MODULE)
    dirName = os.path.dirname(MY_PACKAGE_MODULE)
    
    newPath = None
    if dirName not in ('.', ''):
        if dirName.startswith('.'):
            dirName = os.getcwd() + os.sep + dirName + os.sep
        newPath = dirName
    elif dirName == '':
        inCurrentDir = False
        try:
            imp.find_module(MY_PACKAGE_MODULE)
            inCurrentDir = True
        except ImportError:
            # COMPAT WITH PREVIOUS runTests.py: Try plain module in parent directory
            foundIt = False
            oldSysPath = sys.path[:]
            sys.path = [os.path.realpath(os.getcwd() + os.sep + '..' + os.sep)]
            try:
                imp.find_module(MY_PACKAGE_MODULE)
                foundIt = True
                sys.path = oldSysPath
            except ImportError as e:
                sys.path = oldSysPath
                if not ALLOW_SITE_INSTALL:
                    sys.stderr.write('Cannot find "%s" locally.\n' %(MY_PACKAGE_MODULE,))
                    return 2
                else:
                    try:
                        __import__(baseName)
                    except:
                        sys.stderr.write('Cannot find "%s" locally or in global python path.\n' %(MY_PACKAGE_MODULE,))
                        return 2

            if foundIt is True:
                newPath = os.path.realpath(os.getcwd() + os.sep + '..' + os.sep)
        if inCurrentDir is True:
            newPath = os.path.realpath(os.getcwd() + os.sep + '..' + os.sep)
    
    if newPath:
        newPythonPath = [newPath] + [x for x in os.environ.get('PYTHONPATH', '').split(':') if x]
        os.environ['PYTHONPATH'] = ':'.join(newPythonPath)
        sys.path = [newPath] + sys.path

    try:
        __import__(baseName)
    except ImportError as e:
        if baseName.endswith(('.py', '.pyc', '.pyo')):
            MY_PACKAGE_MODULE = baseName[ : baseName.rindex('.')]

        if e.name != MY_PACKAGE_MODULE:
            sys.stderr.write('Error while importing %s: %s\n Likely this is another dependency that needs to be installed\nPerhaps run "pip install %s" or install the providing package.\n\n' %(e.name, str(e), e.name))
            return 1
        sys.stderr.write('Could not import %s. Either install it or otherwise add to PYTHONPATH\n%s\n' %(MY_PACKAGE_MODULE, str(e)))
        return 1

    if not os.path.isdir(MY_TEST_DIRECTORY):
        if not os.path.exists(MY_TEST_DIRECTORY):
            sys.stderr.write('Cannot find test directory: %s\n' %(MY_TEST_DIRECTORY,))
        else:
            sys.stderr.write('Provided test directory, "%s" is not a directory.\n' %(MY_TEST_DIRECTORY,))
        return 3

    sys.stdout.write('Starting test..\n')
    sys.stdout.flush()
    sys.stderr.flush()


    didTerminate = False

    pipe = subprocess.Popen([goodTestsInfo['path']] + additionalArgs + [MY_TEST_DIRECTORY], env=os.environ, shell=False)
    while True:
        try:
            pipe.wait()
            break
        except KeyboardInterrupt:
            if not didTerminate:
                pipe.terminate()
                didTerminate = True
            else:
                pipe.kill()
                break

    return 0


if __name__ == '__main__':
    ret = main(None, sys.argv[1:])
    sys.exit(ret)
