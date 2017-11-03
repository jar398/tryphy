# 21. sc/metadata_scale

import sys, unittest, json
sys.path.append('./')
sys.path.append('../')
import webapp

url = 'http://phylo.cs.nmsu.edu:5009/phylotastic_ws/sc/metadata_scale'
service = webapp.get_service(url)

class TestScMetadataScale(webapp.WebappTestCase):
    @classmethod
    def get_service(self):
        return service

    # Insert here: edge case tests
    # Insert here: inputs out of range, leading to error or long delay
    # Insert here: error-generating conditions
    # (See ../README.md)

    def test_example_48(self):
        x = self.start_request_tests(example_48)
        mess = x.json().get(u'message')
        self.assert_success(x, mess)
        # Insert: whether result is what it should be according to docs

null=None; false=False; true=True

example_48 = service.get_request('POST', {u'newick': u'((Zea mays,Oryza sativa),((Arabidopsis thaliana,(Glycine max,Medicago sativa)),Solanum lycopersicum)Pentapetalae);'})

if __name__ == '__main__':
    webapp.main()
