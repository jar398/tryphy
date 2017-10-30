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
from test_tnrs_ot_resolve import TnrsOtTester

url = 'http://phylo.cs.nmsu.edu:5004/phylotastic_ws/tnrs/ot/names'
service = webapp.get_service(url)

class TestTnrsOtNames(TnrsOtTester):
    @classmethod
    def get_service(cls):
        return service
    @classmethod
    def http_method(cls):
        return 'POST'

    # Insert here: edge case tests
    # Insert here: inputs out of range, leading to error or long delay
    # Insert here: error-generating conditions
    # (See ../README.md)

    def test_example_8(self):
        x = self.start_request_tests(example_8)
        # Insert: whether result is what it should be according to docs

null=None; false=False; true=True

example_8 = service.get_request('POST', {u'scientificNames': [u'Formica exsectoides', u'Formica pecefica', u'Formica polyctena']})

if __name__ == '__main__':
    webapp.read_requests('work/requests.json')
    webapp.read_exchanges('work/exchanges.json')
    unittest.main()
