# 10 continued. sl/eol/links - POST
# STUB

import sys, unittest, json
sys.path.append("../")
import webapp
from test_sl_eol_get_links import SlEolGetLinksTester

url = 'http://phylo.cs.nmsu.edu:5004/phylotastic_ws/sl/eol/links'
service = webapp.get_service(url)

class TestSlEolLinks(SlEolGetLinksTester):
    @classmethod
    def get_service(self):
        return service

    @classmethod
    def http_method(self):
        return 'POST'

    # Insert here: edge case tests
    # Insert here: inputs out of range, leading to error or long delay
    # Insert here: error-generating conditions
    # (See ../README.md)

    def test_example_24(self):
        x = self.start_request_tests(example_24)
        self.assert_success(x, name)
        # Insert: whether result is what it should be according to docs

null=None; false=False; true=True

example_24 = service.get_request('POST', {u'species': [u'Catopuma badia', u'Catopuma temminckii']})

if __name__ == '__main__':
    webapp.main()
