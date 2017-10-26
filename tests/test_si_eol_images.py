# STUB

import sys, unittest, json
sys.path.append("../")
import webapp

url = 'http://phylo.cs.nmsu.edu:5004/phylotastic_ws/si/eol/images'
service = webapp.get_service(url)

class TestSiEolImages(webapp.WebappTestCase):
    @classmethod
    def get_service(self):
        return service

    # Insert here: edge case tests
    # Insert here: inputs out of range, leading to error or long delay
    # Insert here: error-generating conditions
    # (See ../README.md)

    def test_example_20(self):
        x = self.start_request_tests(example_20)
        # Insert: whether result is what it should be according to docs

null=None; false=False; true=True

example_20 = service.get_request('POST', {u'species': [u'Catopuma badia', u'Catopuma temminckii']})

if __name__ == '__main__':
    webapp.read_requests('work/requests.json')
    webapp.read_exchanges('work/exchanges.json')
    unittest.main()