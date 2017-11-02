# 9. ts/ncbi/genome_species
# GET (POST also allowed in more recent version??)
# Get species (in a taxon) that have a genome sequence in NCBI

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
        self.assertTrue(x.status_code == 400)
        m = x.json().get(u'message')
        # Informative message?
        self.assertTrue(u'taxon' in m, 'no "taxon" in "%s"' % m)

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

    def test_example_22p(self):
        x = self.start_request_tests(example_22p)
        self.assert_success(x)
        n = len(x.json()[u'species'])
        self.assertTrue(n >= 38, str(n))
        # Insert: whether result is what it should be according to docs

null=None; false=False; true=True

example_21 = service.get_request('GET', {u'taxon': u'Panthera'})
example_22 = service.get_request('GET', {u'taxon': u'Rodentia'})
example_22p = service.get_request('GET', {u'taxon': u'Rodentia'})

if __name__ == '__main__':
    webapp.main()
