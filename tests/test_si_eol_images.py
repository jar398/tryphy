# 8 (continued). si/eol/images

# images is for POST, get_images is for GET

# The output is weird.
# "species": [{"images": [{"mediaURL": ...}, {"mediaURL": ...}, ...]}]

# How do we know which image goes with which species?

import sys, unittest, json
sys.path.append('./')
sys.path.append('../')
import webapp
import si_eol_get_images.SiEolImagesTester

url = 'http://phylo.cs.nmsu.edu:5004/phylotastic_ws/si/eol/images'
service = webapp.get_service(url)

class TestSiEolImages(SiEolImagesTester):
    @classmethod
    def get_service(self):
        return service

    @classmethod
    def http_method(self):
        return 'GET'

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

example_20 = service.get_request('POST', {u'species': [u'Catopuma badia', u'Catopuma temminckii']})

if __name__ == '__main__':
    webapp.main()
