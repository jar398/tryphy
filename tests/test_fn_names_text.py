# STUB

import sys, unittest, json
sys.path.append("../")
import webapp

url = 'http://phylo.cs.nmsu.edu:5004/phylotastic_ws/fn/names_text'
service = webapp.get_service(url)

class TestFnNamesText(webapp.WebappTestCase):
    @classmethod
    def get_service(self):
        return service

    # Insert here: edge case tests
    # Insert here: inputs out of range, leading to error or long delay
    # Insert here: error-generating conditions
    # (See ../README.md)

    def test_example_5(self):
        x = self.start_request_tests(example_5)
        # Insert: whether result is what it should be according to docs

    def test_example_4(self):
        x = self.start_request_tests(example_4)
        # Insert: whether result is what it should be according to docs

null=None; false=False; true=True

example_5 = service.get_request('GET', {u'text': u'Formica polyctena is a species of European red wood ant in the genus Formica. The pavement ant, Tetramorium caespitum is an ant native to Europe. Pseudomyrmex is a genus of stinging, wasp-like ants. Adetomyrma venatrix is an endangered species of ants endemic to Madagascar. Carebara diversa is a species of ants in the subfamily Formicinae. It is found in many Asian countries.'})
example_4 = service.get_request('GET', {u'engine': u'2', u'text': u'The lemon dove (Columba larvata) is a species of bird in the pigeon family Columbidae found in montane forests of sub-Saharan Africa.'})

if __name__ == '__main__':
    webapp.read_requests('work/requests.json')
    webapp.read_exchanges('work/exchanges.json')
    unittest.main()
