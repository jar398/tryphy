# 19 continued. gt/pm/tree

import sys, unittest, json
sys.path.append('./')
sys.path.append('../')
import webapp
from test_gt_ot_get_tree import GtTreeTester

url = 'http://phylo.cs.nmsu.edu:5004/phylotastic_ws/gt/pm/tree'
service = webapp.get_service(url)

class TestGtPmTree(GtTreeTester):
    @classmethod
    def get_service(self):
        return service

    @classmethod
    def http_method(cls):
        return 'POST'

    # Insert here: edge case tests
    # Insert here: inputs out of range, leading to error or long delay
    # Insert here: error-generating conditions
    # (See ../README.md)

    def test_example_42(self):
        x = self.start_request_tests(example_42)
        # Insert: whether result is what it should be according to docs

    def test_example_43(self):
        x = self.start_request_tests(example_43)
        # Insert: whether result is what it should be according to docs

null=None; false=False; true=True

example_42 = service.get_request('POST', {u'resolvedNames': [u'Setophaga striata', u'Setophaga magnolia', u'Setophaga angelae', u'Setophaga plumbea', u'Setophaga virens']})
example_43 = service.get_request('POST', {u'resolvedNames': [u'Helianthus annuus', u'Passiflora edulis', u'Rosa arkansana', u'Saccharomyces cerevisiae']})

if __name__ == '__main__':
    webapp.main()
