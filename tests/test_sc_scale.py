# STUB

import sys, unittest, json
sys.path.append("../")
import webapp

url = 'http://phylo.cs.nmsu.edu:5009/phylotastic_ws/sc/scale'
service = webapp.get_service(url)

class TestScScale(webapp.WebappTestCase):
    @classmethod
    def get_service(self):
        return service

    # Insert here: edge case tests
    # Insert here: inputs out of range, leading to error or long delay
    # Insert here: error-generating conditions
    # (See ../README.md)

    def test_example_47(self):
        x = self.start_request_tests(example_47)
        # Insert: whether result is what it should be according to docs

    def test_example_46(self):
        x = self.start_request_tests(example_46)
        # Insert: whether result is what it should be according to docs

null=None; false=False; true=True

example_47 = service.get_request('POST', {u'newick': u'(((((Canis lupus pallipes,Melursus ursinus)Caniformia,((Panthera tigris,Panthera pardus)Panthera,Herpestes fuscus))Carnivora,(Macaca mulatta,Homo sapiens)Catarrhini)Boreoeutheria,Elephas maximus)Eutheria,Haliastur indus)Amniota;'})
example_46 = service.get_request('POST', {u'method': u'sdm', u'newick': u'((Zea mays,Oryza sativa),((Arabidopsis thaliana,(Glycine max,Medicago sativa)),Solanum lycopersicum)Pentapetalae);'})

if __name__ == '__main__':
    webapp.main()
