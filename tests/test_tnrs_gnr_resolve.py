# 4. tnrs/gnr/resolve

import sys, unittest, json
sys.path.append('./')
sys.path.append('../')
import webapp
from test_tnrs_ot_resolve import TnrsTester

url = 'http://phylo.cs.nmsu.edu:5004/phylotastic_ws/tnrs/gnr/resolve'
service = webapp.get_service(url)

class TestTnrsGnrResolve(TnrsTester):
    @classmethod
    def get_service(self):
        return service

    @classmethod
    def http_method(cls):
        return 'GET'

    @classmethod
    def namelist(cls, x):
        return x.json()[u'names'].split('|')

    @classmethod
    def tnrs_request(cls, names):
        return service.get_request('GET', {'names': u'|'.join(names)})

    # Insert here: edge case tests
    # Insert here: inputs out of range, leading to error or long delay
    # Insert here: error-generating conditions
    # (See ../README.md)

    def test_example_9(self):
        x = self.start_request_tests(example_9)
        # Insert: whether result is what it should be according to docs

    def test_example_10(self):
        x = self.start_request_tests(example_10)
        # Insert: whether result is what it should be according to docs

null=None; false=False; true=True

example_9 = service.get_request('GET', {u'names': u'Setophaga striata|Setophaga megnolia|Setophaga angilae|Setophaga plumbea|Setophaga virens'})
example_10 = service.get_request('GET', {u'names': u'Formica polyctena|Formica exsectoides|Formica pecefica'})

if __name__ == '__main__':
    webapp.main()
