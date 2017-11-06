# 4 (continued). tnrs/gnr/resolve (POST version of service)

import sys, unittest, json
sys.path.append('./)
sys.path.append('../')
import webapp
from test_tnrs_ot_resolve import TnrsTester

service = webapp.get_service(5004, 'tnrs/gnr/names')

class TestTnrsGnrNames(webapp.TnrsTester):
    @classmethod
    def get_service(self):
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

    # Insert here: edge case tests
    # Insert here: inputs out of range, leading to error or long delay
    # Insert here: error-generating conditions
    # (See ../README.md)

    def test_example_11(self):
        x = self.start_request_tests(example_11)
        self.assert_success(x)
        # Insert: whether result is what it should be according to docs

null=None; false=False; true=True

example_11 = service.get_request('POST', {u'scientificNames': [u'Formica exsectoides', u'Formica pecefica', u'Formica polyctena']})

if __name__ == '__main__':
    webapp.main()
