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

service = webapp.get_service(5004, 'ts/ncbi/genome_species')

class TestTsNcbiGenomeSpecies(webapp.WebappTestCase):
    @classmethod
    def get_service(self):
        return service

    def test_no_parameter(self):
        """What is we give the service no parameters?  Hoping for 400."""

        request = service.get_request('GET', {})
        x = self.start_request_tests(request)
        mess = x.json().get(u'message')
        self.assertEqual(x.status_code, 400, mess)
        # Informative message?
        self.assertTrue(u'taxon' in mess,
                        'no "taxon" in "%s"' % mess)

    def test_bad_parameter_name(self):
        """What if we give it an unknown parameters name?
        It should complain (400).
        2017-11-05: It doesn't complain.  TBD: issue."""

        request = service.get_request('GET', {u'taxon': u'Panthera', u'rubbish': 25})
        x = self.start_request_tests(request)
        mess = x.json().get(u'message')
        self.assertEqual(x.status_code, 400, mess)
        # Informative message?
        self.assertTrue(u'parameter' in mess,
                        'no "parameter" in "%s"' % mess)

    def test_bad_taxon(self):
        """What if the taxon is unknown?
        Should be a 400 in my opinion.
        2017-11-05 behavior: 200, which is certainly incorrect.
        TBD: issue"""

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
