# STUB

import sys, unittest, json
sys.path.append("../")
import webapp

url = 'http://phylo.cs.nmsu.edu:5006/phylotastic_ws/md/get_studies'
service = webapp.get_service(url)

class TestMdGetStudies(webapp.WebappTestCase):
    @classmethod
    def get_service(self):
        return service

    # Insert here: edge case tests
    # Insert here: inputs out of range, leading to error or long delay
    # Insert here: error-generating conditions
    # (See ../README.md)

    def test_example_36(self):
        x = self.start_request_tests(example_36)
        # Insert: whether result is what it should be according to docs

    def test_example_37(self):
        x = self.start_request_tests(example_37)
        # Insert: whether result is what it should be according to docs

null=None; false=False; true=True

example_36 = service.get_request('GET', {u'list': u'3597191|3597209|3597205|60236|3597195', u'list_type': u'ottids'})
example_37 = service.get_request('GET', {u'list': u'Setophaga striata|Setophaga magnolia|Setophaga angelae|Setophaga plumbea|Setophaga virens', u'list_type': u'taxa'})

if __name__ == '__main__':
    webapp.read_requests('work/requests.json')
    webapp.read_exchanges('work/exchanges.json')
    unittest.main()
