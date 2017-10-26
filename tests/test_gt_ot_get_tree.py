# STUB

import sys, unittest, json
sys.path.append("../")
import webapp

url = 'http://phylo.cs.nmsu.edu:5004/phylotastic_ws/gt/ot/get_tree'
service = webapp.get_service(url)

class TestGtOtGetTree(webapp.WebappTestCase):
    @classmethod
    def get_service(self):
        return service

    # Insert here: edge case tests
    # Insert here: inputs out of range, leading to error or long delay
    # Insert here: error-generating conditions
    # (See ../README.md)

    def test_example_12(self):
        x = self.start_request_tests(example_12)
        # Insert: whether result is what it should be according to docs

    def test_example_13(self):
        x = self.start_request_tests(example_13)
        # Insert: whether result is what it should be according to docs

null=None; false=False; true=True

example_12 = service.get_request('GET', {u'taxa': u'Crabronidae|Ophiocordyceps|Megalyridae|Formica polyctena|Tetramorium caespitum|Pseudomyrmex|Carebara diversa|Formicinae'})
example_13 = service.get_request('GET', {u'taxa': u'Setophaga striata|Setophaga magnolia|Setophaga angelae|Setophaga plumbea|Setophaga virens'})

if __name__ == '__main__':
    webapp.read_requests('work/requests.json')
    webapp.read_exchanges('work/exchanges.json')
    unittest.main()
