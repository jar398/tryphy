# 6. ts/all_species
# Get all species that belong to a particular Taxon.

import sys, unittest, json
sys.path.append('./')
sys.path.append('../')
import webapp

url = 'http://phylo.cs.nmsu.edu:5004/phylotastic_ws/ts/all_species'
service = webapp.get_service(url)

class TestTsAllSpecies(webapp.WebappTestCase):
    @classmethod
    def get_service(self):
        return service

    def test_no_parameter(self):
        request = service.get_request('GET', {})
        x = self.start_request_tests(request)
        self.assertTrue(x.status_code >= 400)
        self.assertTrue(u'taxon' in x.json()[u'message'],    #informative?
                        'no "taxon" in "%s"' % x.json()[u'message'])

    def test_bad_name(self):
        request = service.get_request('GET', {u'taxon': u'Nosuchtaxonia'})
        x = self.start_request_tests(request)
        m = x.json().get(u'message')
        self.assertTrue(x.status_code >= 400, '%s: %s' % (x.status_code, m))
        self.assertTrue(u'No ' in m,    #informative?
                        '%no "No" in "%s"' % x.status_code)

    # TBD: maybe try a very long name?

    def taxon_tester(self, name):
        request = service.get_request('GET', {u'taxon': name})
        x = self.start_request_tests(request)
        self.assert_success(x, name)
        print '%s: %s %s' % (name, len(x.json()[u'species']), x.time)

    # Found this sequence using the 'lineage' script in opentreeoflife/reference-taxonomy/bin

    def test_nested_sequence(self):
        self.taxon_tester('Apis mellifera')
        self.taxon_tester('Apis')
        self.taxon_tester('Apini')
        self.taxon_tester('Apinae')
        # Apidae at 5680 species is a struggle
        self.taxon_tester('Apidae')
        if False:
            # Apoidea: 19566 takes 223 seconds
            # Doc says "maximum taxonomic rank allowed: family" so why did it work at all?
            # Doc says "depending on rank" which isn't right, it depends on 
            # the number of species in the taxon. TBD: note it.
            self.taxon_tester('Apoidea')
            # Aculeata fails after 339 seconds
            self.taxon_tester('Aculeata')
            self.taxon_tester('Apocrita')
            self.taxon_tester('Hymenoptera')
            self.taxon_tester('Endopterygota')
            self.taxon_tester('Neoptera')
            self.taxon_tester('Pterygota')
            self.taxon_tester('Dicondylia')
            self.taxon_tester('Insecta')
            self.taxon_tester('Hexapoda')
            self.taxon_tester('Pancrustacea')
            self.taxon_tester('Mandibulata')
            self.taxon_tester('Arthropoda')
            self.taxon_tester('Panarthropoda')
            self.taxon_tester('Ecdysozoa')
            self.taxon_tester('Protostomia')
            self.taxon_tester('Bilateria')
            self.taxon_tester('Eumetazoa')
            self.taxon_tester('Metazoa')
            self.taxon_tester('Holozoa')
            self.taxon_tester('Opisthokonta')
            self.taxon_tester('Eukaryota')

    # Fails after 22 minutes - non-200 status code.
    @unittest.skip("takes too long")
    def test_big_family(self):
        self.taxon_tester('Staphylinidae')

    # Insert here: edge case tests
    # Insert here: inputs out of range, leading to error or long delay
    # Insert here: error-generating conditions
    # (See ../README.md)

    def test_example_15(self):
        x = self.start_request_tests(example_15)
        self.assert_success(x)
        # Insert: whether result is what it should be according to docs

    def test_example_16(self):
        x = self.start_request_tests(example_16)
        self.assert_success(x)
        # Insert: whether result is what it should be according to docs

null=None; false=False; true=True

example_15 = service.get_request('GET', {u'taxon': u'Vulpes'})
example_16 = service.get_request('GET', {u'taxon': u'Canidae'})

if __name__ == '__main__':
    webapp.read_requests('work/requests.json')
    webapp.read_exchanges('work/exchanges.json')
    unittest.main()
