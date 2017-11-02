# 8 (continued). si/eol/images

# images is for POST, get_images is for GET

# The output is weird.
# "species": [{"images": [{"mediaURL": ...}, {"mediaURL": ...}, ...]}]

# How do we know which image goes with which species?

import sys, unittest, json
sys.path.append('./')
sys.path.append('../')
import webapp

url = 'http://phylo.cs.nmsu.edu:5004/phylotastic_ws/si/eol/images'
service = webapp.get_service(url)

class TestSiEolImages(webapp.WebappTestCase):
    @classmethod
    def get_service(self):
        return service

    def test_bad_method(self):
        request = service.get_request('GET', {})
        x = self.start_request_tests(request)
        # GET method not allowed
        self.assertEqual(x.status_code, 405)
        # TBD: check for informativeness
        json.dump(x.to_dict(), sys.stdout, indent=2)

    def test_no_parameter(self):
        request = service.get_request('POST', {})
        x = self.start_request_tests(request)
        self.assertTrue(x.status_code == 400)
        m = x.json().get(u'message')
        self.assertTrue(u'species' in m,    #informative?
                        'no "species" in "%s"' % m)

    # What if the supplied parameter name is wrong?  Similar to previous

    def test_bad_parameter(self):
        request = service.get_request('POST', {u'bad_parameter': []})
        x = self.start_request_tests(request)
        self.assertTrue(x.status_code == 400)
        m = x.json().get(u'message')
        self.assertTrue(u'species' in m,    #informative?
                        'no "species" in "%s"' % m)

    # What if the value is a single species name instead of a list?
    # 18 seconds (!) - doc says expected response time 2s - 6s.
    # 76 metadata blobs are returned.  TBD: issue.

    def test_bad_value_type(self):
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

    def test_example_20(self):
        x = self.start_request_tests(example_20)
        self.assert_success(x)
        # Insert: whether result is what it should be according to docs
        # There should be at least one image per species
        self.assertTrue(len(all_images(x)) >= len(example_20.parameters[u'species']))

def all_images(x):
    return [image for source in x.json()[u'species'] for image in source[u'images']]

null=None; false=False; true=True

example_20 = service.get_request('POST', {u'species': [u'Catopuma badia', u'Catopuma temminckii']})

if __name__ == '__main__':
    webapp.main()
