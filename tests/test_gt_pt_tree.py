# 19 continued. gt/pt/tree

import sys, unittest, json
sys.path.append('./')
sys.path.append('../')
import webapp
from test_gt_ot_get_tree import GtTreeTester

service = webapp.get_service(5004, 'gt/pt/tree')

class TestGtPtTree(GtTreeTester):
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

    def test_example_45(self):
        x = self.start_request_tests(example_45)
        self.assert_success(x)
        # Insert: whether result is what it should be according to docs

null=None; false=False; true=True

# Example in doc has 'resolvedNames', but service doesn't work unless
# you give it 'taxa'

example_45 = service.get_request('POST', {u'taxa': [u'Setophaga striata', u'Setophaga magnolia', u'Setophaga angelae', u'Setophaga plumbea', u'Setophaga virens']})

if __name__ == '__main__':
    webapp.main()
