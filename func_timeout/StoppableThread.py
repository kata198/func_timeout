
import ctypes
import threading
import time

class StoppableThread(threading.Thread):
    '''
        StoppableThread - A thread that can be stopped by forcing an exception in the execution context.
    '''


    def _stopThread(self, exception):
        if self.isAlive() is False:
            return True

        joinThread = JoinThread(self, exception)
        joinThread.start()

class JoinThread(threading.Thread):
    '''
        JoinThread - The workhouse that stops the StoppableThread
    '''

    def __init__(self, otherThread, exception):
        threading.Thread.__init__(self)
        self.otherThread = otherThread
        self.exception = exception
        self.daemon = True

    def run(self):
        while self.otherThread.isAlive():
            # We loop raising exception incase it's caught hopefully this breaks us far out.
            ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(self.otherThread.ident), ctypes.py_object(self.exception))
            self.otherThread.join(2)

