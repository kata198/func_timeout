func_timeout
=============
Python module to support running any existing function with a given timeout.


Package Includes
----------------

**func_timeout**

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

**FunctionTimedOut**

Exception raised if the function times out


Example
-------
So, for esxample, if you have a function "doit('arg1', 'arg2')" that you want to limit to running for 5 seconds, with func_timeout you can call it like this:


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

func_timeout will run the specified function in a thread with the specified arguments until it returns, raises an exception, or the timeout is exceeded.
If there is a return or an exception raised, it will be returned/raised as normal.

If the timeout has exceeded, the "FunctionTimedOut" exception will be raised in the context of the function being called, as well as from the context of "func_timeout". You should have your function catch the "FunctionTimedOut" exception and exit cleanly if possible. Every 2 seconds until your function is terminated, it will continue to raise FunctionTimedOut. The terminating of the timed-out function happens in the context of the thread and will not block main execution.


Support
-------

I've tested func\_timeout with python 2.7, 3.4, and 3.5. It should work on other versions as well.

ChangeLog can be found at https://raw.githubusercontent.com/kata198/func_timeout/master/ChangeLog 

Pydoc can be found at: http://htmlpreview.github.io/?https://github.com/kata198/func_timeout/blob/master/doc/func_timeout.html?vers=1
