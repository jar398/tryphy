# STUB

import sys, unittest, json
sys.path.append("../")
import webapp

url = 'http://phylo.cs.nmsu.edu:5004/phylotastic_ws/gt/pt/tree'
service = webapp.get_service(url)

class TestGtPtTree(webapp.WebappTestCase):
    @classmethod
    def get_service(self):
        return service

    # Insert here: edge case tests
    # Insert here: inputs out of range, leading to error or long delay
    # Insert here: error-generating conditions
    # (See ../README.md)

    def test_example_45(self):
        x = self.start_request_tests(example_45)
        # Insert: whether result is what it should be according to docs

null=None; false=False; true=True

example_45 = service.get_request('POST', {u'resolvedNames': [u'Setophaga striata', u'Setophaga magnolia', u'Setophaga angelae', u'Setophaga plumbea', u'Setophaga virens']})

if __name__ == '__main__':
    webapp.read_requests('work/requests.json')
    webapp.read_exchanges('work/exchanges.json')
    unittest.main()
