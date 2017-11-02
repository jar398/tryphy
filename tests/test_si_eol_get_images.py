# 8. si/eol/get_images
# TBD: reuse the eol/images tests for this method (similarly to other
# similar situations)

import sys, unittest, json
sys.path.append('./')
sys.path.append('../')
import webapp

url = 'http://phylo.cs.nmsu.edu:5004/phylotastic_ws/si/eol/get_images'
service = webapp.get_service(url)

class TestSiEolGetImages(webapp.WebappTestCase):
    @classmethod
    def get_service(self):
        return service

    def test_bad_method(self):
        request = service.get_request('POST', {})
        x = self.start_request_tests(request)
        # POST method not allowed
        self.assertEqual(x.status_code, 405)
        # TBD: check for informativeness

    # Insert here: edge case tests
    # Insert here: inputs out of range, leading to error or long delay
    # Insert here: error-generating conditions
    # (See ../README.md)

    def test_example_19(self):
        x = self.start_request_tests(example_19)
        self.assert_success(x)
        # Insert: whether result is what it should be according to docs

null=None; false=False; true=True

example_19 = service.get_request('GET', {u'species': u'Panthera leo|Panthera onca|Panthera pardus'})

if __name__ == '__main__':
    webapp.main()
