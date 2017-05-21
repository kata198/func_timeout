# func\_timeout
Python module to support running any existing function with a given timeout.


Package Includes
----------------

**func\_timeout**

This is the function wherein you pass the timeout, the function you want to call, and any arguments, and it runs it for up to #timeout# seconds, and will return/raise anything the passed function would otherwise return or raise.

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

**func\_set\_timeout**

This is a decorator you can use on functions to apply func\_timeout.

Takes two arguments, "timeout" and "allowOverride"

If "allowOverride" is present, an optional keyword argument is added to the wrapped function, 'forceTimeout'. When provided, this will override the timeout used on this function.


The "timeout" parameter can be either a number (for a fixed timeout), or a function/lambda. If a function/lambda is used, it will be passed the same arguments as the called function was passed. It should return a number which will be used as the timeout for that paticular run. For example, if you have a method that calculates data, you'll want a higher timeout for 1 million records than 50 records.

Example:

	@func_set_timeout(2.5)
	def myFunction(self, arg1, arg2):
		...


**FunctionTimedOut**

Exception raised if the function times out.


Has a "retry" method which takes the following arguments:

	* No argument - Retry same args, same function, same timeout
	* Number argument - Retry same args, same function, provided timeout
	* None - Retry same args, same function, no timeout


Example
-------
So, for esxample, if you have a function "doit('arg1', 'arg2')" that you want to limit to running for 5 seconds, with func\_timeout you can call it like this:


	from func_timeout import func_timeout, FunctionTimedOut

	...

	try:

		doitReturnValue = func_timeout(5, doit, args=('arg1', 'arg2'))

	except FunctionTimedOut:
		print ( "doit('arg1', 'arg2') could not complete within 5 seconds and was terminated.\n")
	except Exception as e:
		# Handle any exceptions that doit might raise here


How it works
------------

func\_timeout will run the specified function in a thread with the specified arguments until it returns, raises an exception, or the timeout is exceeded.
If there is a return or an exception raised, it will be returned/raised as normal.

If the timeout has exceeded, the "FunctionTimedOut" exception will be raised in the context of the function being called, as well as from the context of "func\_timeout". You should have your function catch the "FunctionTimedOut" exception and exit cleanly if possible. Every 2 seconds until your function is terminated, it will continue to raise FunctionTimedOut. The terminating of the timed-out function happens in the context of the thread and will not block main execution.

Support
-------

I've tested func\_timeout with python 2.7, 3.4, 3.5, 3.6. It should work on other versions as well.

Works on windows, linux/unix, cygwin, mac

ChangeLog can be found at https://raw.githubusercontent.com/kata198/func_timeout/master/ChangeLog 

Pydoc can be found at: http://htmlpreview.github.io/?https://github.com/kata198/func_timeout/blob/master/doc/func_timeout.html?vers=1
