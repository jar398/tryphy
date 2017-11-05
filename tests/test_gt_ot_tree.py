# 5 (continued). gt/ot/tree
# Like gt/ot/get_tree, but using POST instead of GET

# The (old) example doesn't match the description.  At all.
# Look at new documentation.

import sys, unittest, json
sys.path.append('./')
sys.path.append('../')
import webapp
from test_gt_ot_get_tree import GtTreeTester

service = webapp.get_service(5004, 'gt/ot/tree')

class TestGtOtTree(GtTreeTester):
    @classmethod
    def http_method(cls):
        return 'POST'

    @classmethod
    def get_service(cls):
        return service

    # Insert here: edge case tests
    # Insert here: inputs out of range, leading to error or long delay
    # Insert here: error-generating conditions
    # (See ../README.md)

    def test_example_14a(self):
        x = self.start_request_tests(example_14a)
        if x.status_code != 200:
            json.dump(x.to_dict(), sys.stdout, indent=2)
        self.assert_success(x)
        # Insert: whether result is what it should be according to docs

null=None; false=False; true=True

# This example is from mid-October, and is better

example_14a = service.get_request('POST', {"taxa": ["Setophaga striata","Setophaga magnolia","Setophaga angelae","Setophaga plumbea","Setophaga virens"]})

# This example is from September, and is wrong

example_14 = service.get_request('POST', {u'resolvedNames': [{u'match_type': u'Exact', u'resolver_name': u'OT', u'matched_name': u'Setophaga striata', u'search_string': u'setophaga strieta', u'synonyms': [u'Dendroica striata', u'Setophaga striata'], u'taxon_id': 60236}, {u'match_type': u'Fuzzy', u'resolver_name': u'OT', u'matched_name': u'Setophaga magnolia', u'search_string': u'setophaga magnolia', u'synonyms': [u'Dendroica magnolia', u'Setophaga magnolia'], u'taxon_id': 3597209}, {u'match_type': u'Exact', u'resolver_name': u'OT', u'matched_name': u'Setophaga angelae', u'search_string': u'setophaga angilae', u'synonyms': [u'Dendroica angelae', u'Setophaga angelae'], u'taxon_id': 3597191}, {u'match_type': u'Exact', u'resolver_name': u'OT', u'matched_name': u'Setophaga plumbea', u'search_string': u'setophaga plambea', u'synonyms': [u'Dendroica plumbea', u'Setophaga plumbea'], u'taxon_id': 3597205}, {u'match_type': u'Fuzzy', u'resolver_name': u'OT', u'matched_name': u'Setophaga virens', u'search_string': u'setophaga virens', u'synonyms': [u'Dendroica virens', u'Setophaga virens'], u'taxon_id': 3597195}]})

if __name__ == '__main__':
    webapp.main()
