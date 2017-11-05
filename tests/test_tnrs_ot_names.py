# 3 (continued). tnrs/ot/names

# This service seems to be the same as tnrs/ot/resolve, but with POST 
# instead of GET.
# Maybe we should just run the same tests?

"""
__Parameters:__  			
* *Name:* 	 	scientificNames 
* *Category:*  	mandatory
* *Data Type:*  list of string
* *Description:*  list of scientific names to be resolved
__Citation:__  	 		https://github.com/OpenTreeOfLife/opentree/wiki/Open-Tree-of-Life-APIs#tnrs
"""

import sys, unittest, json
sys.path.append('./')
sys.path.append('../')
import webapp
from test_tnrs_ot_resolve import TnrsTester

service = webapp.get_service(5004, 'tnrs/ot/names')

class TestTnrsOtNames(TnrsTester):
    @classmethod
    def get_service(cls):
        return service

    @classmethod
    def http_method(cls):
        return 'POST'

    @classmethod
    def namelist(cls, x):
        return x.json()[u'scientificNames']

    @classmethod
    def tnrs_request(cls, names):
        return service.get_request('POST', {'scientificNames': names})

    # Edge case: names= is supplied, but there are no names.
    # In this case, the deployed web service says that there is no names
    # parameter.  (The difference between missing and supplied 
    # but null is academic?  Depends on taste.)
    def test_2(self):
        request = self.__class__.tnrs_request([])
        x = request.exchange()
        # 204 = no content (from open tree)
        # message = "Could not resolve any name"
        # Changed: now returns 400, not 204.  Better.
        # As of 2017-11-01, we get 500, not 400.  Issue.
        self.assert_response_status(x, 400)

    # Insert here: edge case tests
    # Insert here: inputs out of range, leading to error or long delay
    # Insert here: error-generating conditions
    # (See ../README.md)

    def test_example_8(self):
        x = self.start_request_tests(example_8)
        # Insert: whether result is what it should be according to docs
        self.assert_success(x)

null=None; false=False; true=True

example_8 = service.get_request('POST', {u'scientificNames': [u'Formica exsectoides', u'Formica pecefica', u'Formica polyctena']})

if __name__ == '__main__':
    webapp.main()
