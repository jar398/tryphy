# STUB

import sys, unittest, json
sys.path.append("../")
import webapp

url = 'http://phylo.cs.nmsu.edu:5006/phylotastic_ws/md/studies'
service = webapp.get_service(url)

class TestMdStudies(webapp.WebappTestCase):
    @classmethod
    def get_service(self):
        return service

    # Insert here: edge case tests
    # Insert here: inputs out of range, leading to error or long delay
    # Insert here: error-generating conditions
    # (See ../README.md)

    def test_example_38(self):
        x = self.start_request_tests(example_38)
        # Insert: whether result is what it should be according to docs

    def test_example_39(self):
        x = self.start_request_tests(example_39)
        # Insert: whether result is what it should be according to docs

null=None; false=False; true=True

example_38 = service.get_request('POST', {u'list': [1094064, 860906, 257323, 698438, 698406, 187220, 336231, 124230], u'list_type': u'ottids'})
example_39 = service.get_request('POST', {u'list': [u'Delphinidae', u'Delphinus capensis', u'Delphinus delphis', u'Tursiops truncatus', u'Tursiops aduncus', u'Sotalia fluviatilis', u'Sousa chinensis'], u'list_type': u'taxa'})

if __name__ == '__main__':
    webapp.read_requests('work/requests.json')
    webapp.read_exchanges('work/exchanges.json')
    unittest.main()
