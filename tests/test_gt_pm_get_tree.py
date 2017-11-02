# STUB

import sys, unittest, json
sys.path.append("../")
import webapp

url = 'http://phylo.cs.nmsu.edu:5004/phylotastic_ws/gt/pm/get_tree'
service = webapp.get_service(url)

class TestGtPmGetTree(webapp.WebappTestCase):
    @classmethod
    def get_service(self):
        return service

    # Insert here: edge case tests
    # Insert here: inputs out of range, leading to error or long delay
    # Insert here: error-generating conditions
    # (See ../README.md)

    def test_example_41(self):
        x = self.start_request_tests(example_41)
        # Insert: whether result is what it should be according to docs

    def test_example_40(self):
        x = self.start_request_tests(example_40)
        # Insert: whether result is what it should be according to docs

null=None; false=False; true=True

example_41 = service.get_request('GET', {u'taxa': u'Helianthus annuus|Passiflora edulis|Rosa arkansana|Saccharomyces cerevisiae'})
example_40 = service.get_request('GET', {u'taxa': u'Panthera leo|Panthera onca|Panthera tigris|Panthera uncia'})

if __name__ == '__main__':
    webapp.main()
