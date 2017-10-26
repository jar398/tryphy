# STUB

import sys, unittest, json
sys.path.append("../")
import webapp

url = 'http://phylo.cs.nmsu.edu:5004/phylotastic_ws/ts/country_species'
service = webapp.get_service(url)

class TestTsCountrySpecies(webapp.WebappTestCase):
    @classmethod
    def get_service(self):
        return service

    # Insert here: edge case tests
    # Insert here: inputs out of range, leading to error or long delay
    # Insert here: error-generating conditions
    # (See ../README.md)

    def test_example_18(self):
        x = self.start_request_tests(example_18)
        # Insert: whether result is what it should be according to docs

    def test_example_17(self):
        x = self.start_request_tests(example_17)
        # Insert: whether result is what it should be according to docs

null=None; false=False; true=True

example_18 = service.get_request('GET', {u'country': u'Nepal', u'taxon': u'Felidae'})
example_17 = service.get_request('GET', {u'country': u'Bangladesh', u'taxon': u'Panthera'})

if __name__ == '__main__':
    webapp.read_requests('work/requests.json')
    webapp.read_exchanges('work/exchanges.json')
    unittest.main()
