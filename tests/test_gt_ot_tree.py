# STUB

import sys, unittest, json
sys.path.append("../")
import webapp

url = 'http://phylo.cs.nmsu.edu:5004/phylotastic_ws/gt/ot/tree'
service = webapp.get_service(url)

class TestGtOtTree(webapp.WebappTestCase):
    @classmethod
    def get_service(self):
        return service

    # Insert here: edge case tests
    # Insert here: inputs out of range, leading to error or long delay
    # Insert here: error-generating conditions
    # (See ../README.md)

    def test_example_14(self):
        x = self.start_request_tests(example_14)
        # Insert: whether result is what it should be according to docs

null=None; false=False; true=True

example_14 = service.get_request('POST', {u'resolvedNames': [{u'match_type': u'Exact', u'resolver_name': u'OT', u'matched_name': u'Setophaga striata', u'search_string': u'setophaga strieta', u'synonyms': [u'Dendroica striata', u'Setophaga striata'], u'taxon_id': 60236}, {u'match_type': u'Fuzzy', u'resolver_name': u'OT', u'matched_name': u'Setophaga magnolia', u'search_string': u'setophaga magnolia', u'synonyms': [u'Dendroica magnolia', u'Setophaga magnolia'], u'taxon_id': 3597209}, {u'match_type': u'Exact', u'resolver_name': u'OT', u'matched_name': u'Setophaga angelae', u'search_string': u'setophaga angilae', u'synonyms': [u'Dendroica angelae', u'Setophaga angelae'], u'taxon_id': 3597191}, {u'match_type': u'Exact', u'resolver_name': u'OT', u'matched_name': u'Setophaga plumbea', u'search_string': u'setophaga plambea', u'synonyms': [u'Dendroica plumbea', u'Setophaga plumbea'], u'taxon_id': 3597205}, {u'match_type': u'Fuzzy', u'resolver_name': u'OT', u'matched_name': u'Setophaga virens', u'search_string': u'setophaga virens', u'synonyms': [u'Dendroica virens', u'Setophaga virens'], u'taxon_id': 3597195}]})

if __name__ == '__main__':
    webapp.read_requests('work/requests.json')
    webapp.read_exchanges('work/exchanges.json')
    unittest.main()
