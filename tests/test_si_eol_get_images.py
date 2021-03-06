# 8. si/eol/get_images
# TBD: reuse the eol/images tests for this method (similarly to other
# similar situations)

import sys, unittest, json
sys.path.append('./')
sys.path.append('../')
import webapp

service = webapp.get_service(5004, 'si/eol/get_images')

class SiEolImagesTester(webapp.WebappTestCase):

    def test_bad_method(self):
        request = service.get_request('POST', {})
        x = self.start_request_tests(request)
        # POST method not allowed
        self.assertEqual(x.status_code, 405)
        # TBD: check for informativeness

    def test_no_parameter(self):
        request = service.get_request('POST', {})
        x = self.start_request_tests(request)
        self.assertTrue(x.status_code == 400)
        m = x.json().get(u'message')
        self.assertTrue(u'species' in m,    #informative?
                        'no "species" in "%s"' % m)

    def test_bad_parameter(self):
        """What if the supplied parameter name is wrong?  Similar to previous"""

        request = service.get_request('POST', {u'bad_parameter': []})
        x = self.start_request_tests(request)
        self.assertTrue(x.status_code == 400)
        m = x.json().get(u'message')
        self.assertTrue(u'species' in m,    #informative?
                        'no "species" in "%s"' % m)

    def test_bad_value_type(self):
        """What if the value is a single species name instead of a list?
        18 seconds (!) - doc says expected response time 2s - 6s.
        76 metadata blobs are returned.  TBD: issue."""

        print 'Patience, this may take 20 seconds'
        request = service.get_request('POST', {u'species': u'Nosuchtaxonia mistakea'})
        x = self.start_request_tests(request)
        self.assertTrue(x.status_code % 100 == 4, x.status_code)
        json.dump(x.to_dict(), sys.stdout, indent=2)
        # TBD: Change this to a *correct* check for message informativeness.
        m = x.json().get(u'message')
        self.assertTrue(u'species' in m,    #informative?
                        'no "species" in "%s"' % m)

    def test_bad_name(self):
        request = service.get_request('POST', {u'species': [u'Nosuchtaxonia mistakea']})
        x = self.start_request_tests(request)
        m = x.json().get(u'message')
        self.assert_success(x, m)
        # gives a 200, which is acceptable
        self.assertTrue(u'species' in x.json())
        # json.dump(x.to_dict(), sys.stdout, indent=2)
        self.assertEqual(len(all_images(x)), 0, "number of images")

    # Too many species?

    # Insert here: edge case tests
    # Insert here: inputs out of range, leading to error or long delay
    # Insert here: error-generating conditions
    # (See ../README.md)

class TestSiEolGetImages(SiEolImagesTester):
    @classmethod
    def get_service(self):
        return service

    @classmethod
    def http_method(self):
        return 'GET'

    def test_bad_method(self):
        """What if you do a GET when the service is expecting a POST?
        (Hoping for 405.)"""

        request = service.get_request('GET', {})
        x = self.start_request_tests(request)
        # GET method not allowed
        self.assertEqual(x.status_code, 405)
        # TBD: check for informativeness
        json.dump(x.to_dict(), sys.stdout, indent=2)

    def test_example_19(self):
        x = self.start_request_tests(example_19)
        self.assert_success(x)
        # Insert: whether result is what it should be according to docs

def all_images(x):
    return [image for source in x.json()[u'species'] for image in source[u'images']]

example_19 = service.get_request('GET', {u'species': u'Panthera leo|Panthera onca|Panthera pardus'})

if __name__ == '__main__':
    webapp.main()
