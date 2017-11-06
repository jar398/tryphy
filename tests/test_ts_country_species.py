# ts/country_species
# Species that belong to a particular taxon and established in a particular 
# country, using INaturalist services.
# GET or POST

import sys, unittest, json
sys.path.append('./')
sys.path.append('../')
import webapp

service = webapp.get_service(5004, 'ts/country_species')

class TestTsCountrySpecies(webapp.WebappTestCase):
    @classmethod
    def get_service(self):
        return service

    def test_no_parameter(self):
        request = service.get_request('GET', {})
        x = self.start_request_tests(request)
        self.assertTrue(x.status_code >= 400)
        self.assertTrue(u'taxon' in x.json()[u'message'],    #informative?
                        'no "taxon" in "%s"' % x.json()[u'message'])

    def test_bad_taxon(self):
        request = service.get_request('GET', {u'taxon': u'Nosuchtaxonia', u'country': u'Nepal'})
        x = self.start_request_tests(request)
        m = x.json().get(u'message')
        # Returns 200, should return 400.  TBD: issue
        self.assertTrue(x.status_code >= 400, m)
        self.assertTrue(u'axon' in m,    #informative?
                        'no "taxon" in "%s"' % m)

    @unittest.skip("hangs")
    def test_bad_country(self):
        """See what happens if the country is likely to be unknown.
        2017-11-05 This test just hangs, so skipping for now.
        TBD: issue"""

        request = service.get_request('GET', {u'taxon': u'Hylidae', u'country': u'Sovietunion'})
        x = self.start_request_tests(request)
        m = x.json().get(u'message')
        # Returns 200, should return 400.  TBD: issue
        self.assertTrue(x.status_code >= 400, m)
        self.assertTrue(u'axon' in m,    #informative?
                        'no "taxon" in "%s"' % m)

    # Insert here: edge case tests
    # Insert here: inputs out of range, leading to error or long delay
    # Insert here: error-generating conditions
    # (See ../README.md)

    def test_example_18(self):
        x = self.start_request_tests(example_18)
        self.assert_success(x)
        # Insert: whether result is what it should be according to docs

    def test_example_17(self):
        x = self.start_request_tests(example_17)
        self.assert_success(x)
        # Insert: whether result is what it should be according to docs

    def test_example_17p(self):
        """2017-11-05 This test complains about the 'taxon' parameter being 
        missing.  But it's not missing.
        Error: Missing parameter 'taxon'.  TBD: issue"""

        x = self.start_request_tests(example_17p)
        m = x.json()[u'message']
        self.assert_success(x, m)
        # Insert: whether result is what it should be according to docs

null=None; false=False; true=True

example_18 = service.get_request('GET', {u'country': u'Nepal', u'taxon': u'Felidae'})
example_17 = service.get_request('GET', {u'country': u'Bangladesh', u'taxon': u'Panthera'})
example_17p = service.get_request('POST', {u'country': u'Bangladesh', u'taxon': u'Panthera'})

if __name__ == '__main__':
    webapp.main()
