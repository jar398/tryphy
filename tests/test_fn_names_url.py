# STUB

import sys, unittest, json
sys.path.append("../")
import webapp

url = 'http://phylo.cs.nmsu.edu:5004/phylotastic_ws/fn/names_url'
service = webapp.get_service(url)

class TestFnNamesUrl(webapp.WebappTestCase):
    @classmethod
    def get_service(self):
        return service

    # Insert here: edge case tests
    # Insert here: inputs out of range, leading to error or long delay
    # Insert here: error-generating conditions
    # (See ../README.md)

    def test_example_1(self):
        x = self.start_request_tests(example_1)
        # Insert: whether result is what it should be according to docs

    def test_example_2(self):
        x = self.start_request_tests(example_2)
        # Insert: whether result is what it should be according to docs

    def test_example_3(self):
        x = self.start_request_tests(example_3)
        # Insert: whether result is what it should be according to docs

null=None; false=False; true=True

example_1 = service.get_request('GET', {u'url': u'http://en.wikipedia.org/wiki/Ant'})
example_2 = service.get_request('GET', {u'engine': u'1', u'url': u'https://en.wikipedia.org/wiki/Plain_pigeon'})
example_3 = service.get_request('GET', {u'url': u'http://www.fws.gov/westvirginiafieldoffice/PDF/beechridgehcp/Appendix_D_Table_D-1.pdf'})

if __name__ == '__main__':
    webapp.read_requests('work/requests.json')
    webapp.read_exchanges('work/exchanges.json')
    unittest.main()
