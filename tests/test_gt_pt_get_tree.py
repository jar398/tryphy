# 19. gt/pt/get_tree

import sys, unittest, json
sys.path.append('./')
sys.path.append('../')
import webapp
from test_gt_ot_get_tree import GtTreeTester

service = webapp.get_service(5004, 'gt/pt/get_tree')

class TestGtPtGetTree(GtTreeTester):
    @classmethod
    def get_service(self):
        return service

    @classmethod
    def http_method(cls):
        return 'GET'

    # Insert here: edge case tests
    # Insert here: inputs out of range, leading to error or long delay
    # Insert here: error-generating conditions
    # (See ../README.md)

    def test_example_44(self):
        x = self.start_request_tests(example_44)
        self.assert_success(x)
        # Insert: whether result is what it should be according to docs

null=None; false=False; true=True

example_44 = service.get_request('GET', {u'taxa': u'Setophaga striata|Setophaga magnolia|Setophaga angelae|Setophaga plumbea|Setophaga virens'})

if __name__ == '__main__':
    webapp.main()
