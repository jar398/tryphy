# 20. sc/scale

# newick parameter is required
# method parameter is optional: median or sdm

import sys, unittest, json
sys.path.append('./')
sys.path.append('../')
import webapp

url = 'http://phylo.cs.nmsu.edu:5009/phylotastic_ws/sc/scale'
service = webapp.get_service(url)

class TestScScale(webapp.WebappTestCase):
    @classmethod
    def get_service(self):
        return service

    def test_no_parameters(self):
        x = self.start_request_tests(service.get_request('POST', None))
        # Yields 500.  TBD: issue
        self.assert_response_status(x, 400)
        self.assertTrue('tree' in x.json()[u'message'])

    def test_no_parameters_2(self):
        x = self.start_request_tests(service.get_request('POST', {}))
        self.assert_response_status(x, 400)
        mess = x.json()[u'message']
        self.assertTrue('newick' in mess, mess)

    def test_bogus_newick(self):
        x = self.start_request_tests(service.get_request('POST', {u'newick': '(a,b)c);'}))
        # Issue: 500 Error: Failed to scale from datelife R package
        self.assert_response_status(x, 400)
        # json.dump(x.json(), sys.stdout, indent=2)
        mess = x.json()[u'message']
        # Not clear what the message ought to say; be prepared to change the 
        # following check to match the message that eventually gets chosen.
        self.assertTrue('yntax' in mess, mess)

    # Insert here: edge case tests
    # Insert here: inputs out of range, leading to error or long delay
    # Insert here: error-generating conditions
    # (See ../README.md)

    def test_example_47(self):
        x = self.start_request_tests(example_47)
        mess = x.json().get(u'message')
        self.assert_success(x, mess)
        # Insert: whether result is what it should be according to docs

    def test_example_46(self):
        x = self.start_request_tests(example_46)
        mess = x.json().get(u'message')
        self.assert_success(x, mess)
        # Insert: whether result is what it should be according to docs

null=None; false=False; true=True

example_47 = service.get_request('POST', {u'newick': u'(((((Canis lupus pallipes,Melursus ursinus)Caniformia,((Panthera tigris,Panthera pardus)Panthera,Herpestes fuscus))Carnivora,(Macaca mulatta,Homo sapiens)Catarrhini)Boreoeutheria,Elephas maximus)Eutheria,Haliastur indus)Amniota;'})
example_46 = service.get_request('POST', {u'method': u'sdm', u'newick': u'((Zea mays,Oryza sativa),((Arabidopsis thaliana,(Glycine max,Medicago sativa)),Solanum lycopersicum)Pentapetalae);'})

if __name__ == '__main__':
    webapp.main()
