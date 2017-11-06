# 18. gt/pm/get_tree

import sys, unittest, json
sys.path.append('./')
sys.path.append('../')
import webapp
from test_gt_ot_get_tree import GtTreeTester

service = webapp.get_service(5004, 'gt/pm/get_tree')

class TestGtPmGetTree(GtTreeTester):
    @classmethod
    def get_service(self):
        """Class method so that the superclass can tell which service we're testing."""

        return service

    @classmethod
    def http_method(cls):
        """Class method so that the superclass can tell which HTTP method should be used."""

        return 'GET'

    # Insert here: edge case tests
    # Insert here: inputs out of range, leading to error or long delay
    # Insert here: error-generating conditions
    # (See ../README.md)

    def test_example_41(self):
        x = self.start_request_tests(example_41)
        self.assert_success(x)
        # Insert: whether result is what it should be according to docs

    def test_example_40(self):
        x = self.start_request_tests(example_40)
        self.assert_success(x)
        # Insert: whether result is what it should be according to docs

null=None; false=False; true=True

example_41 = service.get_request('GET', {u'taxa': u'Helianthus annuus|Passiflora edulis|Rosa arkansana|Saccharomyces cerevisiae'})
example_40 = service.get_request('GET', {u'taxa': u'Panthera leo|Panthera onca|Panthera tigris|Panthera uncia'})

if __name__ == '__main__':
    webapp.main()
