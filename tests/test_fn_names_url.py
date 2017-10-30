# 1. fn/names_url

import sys, unittest, json
sys.path.append('./')
sys.path.append('../')
import webapp

url = 'http://phylo.cs.nmsu.edu:5004/phylotastic_ws/fn/names_url'
service = webapp.get_service(url)

class TestFnNamesUrl(webapp.WebappTestCase):
    @classmethod
    def get_service(self):
        return service

    # No parameters.
    # This returns a 500 (as of 2017-10-30).  More http-like would be for it to give a 400.
    # But the error message is not informative.  TBD: issue.
    def test_no_parameter(self):
        request = service.get_request('GET', {})
        x = self.start_request_tests(request)
        self.assertTrue(x.status_code >= 400)
        self.assertTrue(u'url' in x.json()[u'message'])    #informative?

    # Non-HTTP URI.
    # This returns a 500 (as of 2017-10-30).  More http-like would be for it 
    # to give a 400. But the error message is not informative.  TBD: issue.
    def test_non_http_uri(self):
        request = service.get_request('GET', {u'url': u'urn:nbn:de:bvb:19-146642'})
        x = self.start_request_tests(request)
        self.assertTrue(x.status_code >= 400)

    # Nonexistent target.
    # This returns a 500 (as of 2017-10-30).  More http-like would be for it 
    # to give a 400. In any case, the error message is not informative.  TBD: issue.
    def test_nonexistent(self):
        request = service.get_request('GET', {u'url': u'https://example.com/nonexistent.txt'})
        x = self.start_request_tests(request)
        self.assertTrue(x.status_code >= 400)
        self.assertTrue(x.status_code < 500)
        # TBD: test for informative message

    # See what happens when you give it a file of an unrecognized type.
    # It succeeds with no results.  I would think that GNRD should have told
    # us that the file couldn't be processed, but it doesn't.
    # There is no way to distinguish in the GNRD response the absence of names
    # from an invalid file, so not sure what we should expect here.
    # TBD: GNRD issue.
    # NOTE: If this URL stops working, simply replace it by any other
    # similar URL on the web - a zip or tarball, or even an image.
    def test_bad_type(self):
        request = service.get_request('GET', {u'url': u'http://files.opentreeoflife.org/silva/silva-115/silva-115.tgz'})
        x = self.start_request_tests(request)
        self.assertEqual(x.json()[u'scientificNames'], [])

    # Test large input.
    # This takes 240 seconds on a 10 Mb input file - but it works.
    # Trimming the file back to 10 Mb.
    def test_large_input(self):
        request = service.get_request('GET', {u'url': u'http://mumble.net/~jar/tmp/tenth-psyche.txt'})
        print >>sys.stderr, '\nBe patient, takes about 25 seconds'
        x = self.start_request_tests(request)
        self.assert_success(x)
        self.assertTrue(len(x.json()[u'scientificNames']) > 1000)

    # TBD: test what happens if extraneous parameter supplied

    # Insert here: edge case tests
    # Insert here: inputs out of range, leading to error or long delay
    # Insert here: error-generating conditions
    # (See ../README.md)

    def test_example_1(self):
        x = self.start_request_tests(example_1)
        self.assert_success(x)
        # Insert: whether result is what it should be according to docs
        self.assertTrue(len(x.json()[u'scientificNames']) > 20)
        self.assertTrue(u'Odontomachus bauri' in x.json()[u'scientificNames'])

    def test_example_2(self):
        x = self.start_request_tests(example_2)
        self.assert_success(x)
        # Insert: whether result is what it should be according to docs
        self.assertTrue(len(x.json()[u'scientificNames']) > 5)
        self.assertTrue(u'Patagioenas inornata' in x.json()[u'scientificNames'])

    def test_example_3(self):
        x = self.start_request_tests(example_3)
        self.assert_success(x)
        # Insert: whether result is what it should be according to docs
        self.assertTrue(len(x.json()[u'scientificNames']) > 20)
        self.assertTrue(u'Lolium perenne' in x.json()[u'scientificNames'])

null=None; false=False; true=True

example_1 = service.get_request('GET', {u'url': u'http://en.wikipedia.org/wiki/Ant'})
example_2 = service.get_request('GET', {u'engine': u'1', u'url': u'https://en.wikipedia.org/wiki/Plain_pigeon'})
example_3 = service.get_request('GET', {u'url': u'http://www.fws.gov/westvirginiafieldoffice/PDF/beechridgehcp/Appendix_D_Table_D-1.pdf'})

if __name__ == '__main__':
    webapp.read_requests('work/requests.json')
    webapp.read_exchanges('work/exchanges.json')
    unittest.main()
