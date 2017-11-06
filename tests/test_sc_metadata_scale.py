# 21. sc/metadata_scale
# Parameter: newick
# Result: metadata_tree_scaling
#   
# Issue: "service_documentation" points to old documentation, not new.

import sys, unittest, json
sys.path.append('./')
sys.path.append('../')
import webapp

service = webapp.get_service(5009, 'sc/metadata_scale')

class TestScMetadataScale(webapp.WebappTestCase):
    @classmethod
    def get_service(self):
        return service

    def test_no_parameters(self):
        """What if there are no parameters?  Hope for 400."""

        x = self.start_request_tests(service.get_request('POST', None))
        # Yields 500.  TBD: issue
        # Error: 'NoneType' object has no attribute '__getitem__'
        mess = x.json().get(u'message')
        self.assert_response_status(x, 400, mess)
        self.assertTrue('newick' in mess, mess)

    def test_no_parameters_2(self):
        x = self.start_request_tests(service.get_request('POST', {}))
        self.assert_response_status(x, 400)
        mess = x.json().get(u'message')
        self.assertTrue('newick' in mess, mess)

    def test_bogus_newick(self):
        x = self.start_request_tests(service.get_request('POST', {u'newick': '(a,b)c);'}))
        # Issue: 500 Error: Failed to scale from datelife R package
        self.assert_response_status(x, 400)
        # json.dump(x.json(), sys.stdout, indent=2)
        mess = x.json().get(u'message')
        # Not clear what the message ought to say; be prepared to change the 
        # following check to match the message that eventually gets chosen.
        self.assertTrue('yntax' in mess, mess)

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
