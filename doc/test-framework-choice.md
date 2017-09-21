Choice of test framework
========================

* [Web site about python testing frameworks](http://pythontesting.net/start-here/)
* [Good Python testing overview from 2009](https://www.ibm.com/developerworks/aix/library/au-python_test/index.html/)
* [Unit test example from Open Tree](https://github.com/OpenTreeOfLife/phylesystem-api/blob/master/modules/test_gitdata.py)

* Mark Holder (peyotl, otcetera, etc.) likes nose, but nose and nose2 seem to be abandonware.
* Duke Leto used unittest for phylesystem back in December 2013
* pytest requires an install step.  Might make the test files more succinct.
  Has things we don't need.
* unittest is sort of clunky but is built into the python distribution.
  No install step is required and there is no shell command.
* Open Tree has [web API testing code that we can use](https://github.com/OpenTreeOfLife/germinator/tree/master/ws-tests).  The framework is nonstandard but we don't have to use it.

Strategy: unittest + open tree utilities; upgrade later from unittest
to pytest if unittest ends up being inadequate.

