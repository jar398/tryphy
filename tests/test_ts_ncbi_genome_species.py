# 9. ts/ncbi/genome_species

# Old documentation only lists GET as a possible method.
# New documentatino says "HTTP Method: GET or POST"
#  but maybe POST doesn't work.

# Get species (in a taxon) that have a genome sequence in NCBI.
# Parameter: taxon - a single taxon name.

import sys, unittest, json
sys.path.append('./')
sys.path.append('../')
import webapp

url = 'http://phylo.cs.nmsu.edu:5004/phylotastic_ws/ts/ncbi/genome_species'
service = webapp.get_service(url)

class TestTsNcbiGenomeSpecies(webapp.WebappTestCase):
    @classmethod
    def get_service(self):
        return service

    def test_no_parameter(self):
        request = service.get_request('GET', {})
        x = self.start_request_tests(request)
        mess = x.json().get(u'message')
        self.assertEqual(x.status_code, 400, mess)
        # Informative message?
        self.assertTrue(u'taxon' in mess,
                        'no "taxon" in "%s"' % mess)

    # What if we give it an unknown parameters name?
    # - should complain but doesn't.  TBD: issue.

    def test_bad_parameter_name(self):
        request = service.get_request('GET', {u'taxon': u'Panthera', u'rubbish': 25})
        x = self.start_request_tests(request)
        mess = x.json().get(u'message')
        self.assertEqual(x.status_code, 400, mess)
        # Informative message?
        self.assertTrue(u'parameter' in mess,
                        'no "parameter" in "%s"' % mess)

    # What if the taxon is unknown?
    # Should be a 400 I think.  200 is certainly incorrect.
    # TBD: issue

    def test_bad_taxon(self):
        request = service.get_request('GET', {u'taxon': u'Unknownia'})
        x = self.start_request_tests(request)
        mess = x.json().get(u'message')
        self.assertEqual(x.status_code, 400, mess)
        # Informative message?
        # 'No match found for term Unknownia'
        self.assertTrue(u'taxon' in mess,
                        'no "taxon" in "%s"' % mess)

    # Insert here: edge case tests
    # Insert here: inputs out of range, leading to error or long delay
    # Insert here: error-generating conditions
    # (See ../README.md)

    def test_example_21(self):
        x = self.start_request_tests(example_21)
        self.assert_success(x)
        n = len(x.json()[u'species'])
        self.assertTrue(n >= 4, str(n))
        # Insert: whether result is what it should be according to docs

    # TBD: Issue: many of the 'species' returned are actually subspecies

    def test_example_22(self):
        x = self.start_request_tests(example_22)
        self.assert_success(x)
        n = len(x.json()[u'species'])
        self.assertTrue(n >= 38, str(n))
        # Insert: whether result is what it should be according to docs

    # What about using POST instead of GET?
    # 400 Error: Missing parameter 'taxon'   - which doesn't make any sense.
    # TBD: issue.
    # Old documentation only lists GET as a possible.
    # New documentatino says "HTTP Method: GET or POST"

    def test_example_22_post(self):
        x = self.start_request_tests(example_22_post)
        self.assert_success(x)
        n = len(x.json()[u'species'])
        self.assertTrue(n >= 38, str(n))
        # Insert: whether result is what it should be according to docs

null=None; false=False; true=True

example_21 = service.get_request('GET', {u'taxon': u'Panthera'})
example_22 = service.get_request('GET', {u'taxon': u'Rodentia'})
example_22_post = service.get_request('POST', {u'taxon': u'Rodentia'})

if __name__ == '__main__':
    webapp.main()
