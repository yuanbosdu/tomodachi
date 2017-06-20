Changes
=======

0.2.12 (2017-06-18)
-------------------

- Type hinted code base and minor bug fixes for internal functions.


0.2.11 (2017-06-09)
-------------------

- Invoker methods can now be called directly without the need to mock the
  invoker decorator function.


0.2.10 (2017-06-08)
-------------------

- Added ``@functools.wraps`` decorator to invoked functions of service classes.


0.2.9 (2017-06-06)
------------------

- Added a list of safe modules that may never be removed from the list of
  already loaded modules. Removing the module 'typing' from the list would
  cause a RecursionError exception since Python 3.6.1.


0.2.8 (2017-05-23)
------------------

- Additional improvements to network connectivity issues to not get stuck in
  waiting state.


0.2.7 (2017-05-23)
------------------

- Improved SNS+SQS draining / restart when network connectivity has been lost
  or temporarily suspended. Would improve situations when development machine
  has been in hibernation.

- Replaced deprecated logging functions to rid warnings.


0.2.6 (2017-05-22)
------------------

- Support for a "generic" aws dictonary in options that can hold region,
  access key id and secret to be shared among other AWS resources/services.

- Updated aiobotocore / botocore dependencies.

- Gracefully handle and discard invalid SNS/SQS messages not in JSON format.

- Corrected issue where watched directories with "similar" names as settings
  would be ignored.


0.2.5 (2017-05-16)
------------------

- Updated issues with function caching due to keepalive when hot reloading in
  development. Currently disables keepalive entirely.

- Fixed issue with updated file logging for watcher.


0.2.4 (2017-05-12)
------------------

- Downgraded botocore to meet requirements and to make the installed
  ``tomodachi`` script runnable again.


0.2.3 (2017-05-10)
------------------

- Watcher is now configurable to ignore specific directories dependant on the
  service. (github: **smaaland**)

- Fixed issue where using ``--config`` instead of ``-c`` would result in a
  raised exception. (github: **smaaland**)


0.2.2 (2017-05-04)
------------------

- ``tomodachi.transport.http`` has its own Response object that works better
  with default content types and charsets - examples/http_service.py updated.

- No automatic conversion will be tried if the returned response of an http
  method is of ``bytes`` type.

0.2.1 (2017-05-03)
------------------

- Improved handling of how charsets and encodings work with aiohttp.

- Fixed an issue where ``Content-Type`` header would always be included twice
  for aiohttp.web.Response objects.


0.2.0 (2017-05-02)
------------------

- Watcher now only reacts to files with file endings ``.py``, ``.json``,
  ``.yml``, ``.html`` or ``.html`` and ignores to look at paths
  ``__pycache__``, ``.git``, ``.svn``, ``__ignored__``, ``__temporary__`` and
  ``__tmp__``.

- HTTP transport may now respond with an aiohttp.web.Response object for more
  complex responses.

- HTTP transport response headers can now use the multidict library.


0.1.11 (2017-04-02)
-------------------

- Working PyPI release.

- Added unit tests.

- Works with aiohttp 2 and aiobotocore 0.3.

- Service classes must be decorated with ``@tomodachi.service``.