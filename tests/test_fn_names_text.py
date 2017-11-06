# 2. fn/names_text

# Parameters: text (required), engine (optional)

import sys, os, unittest, json, codecs
sys.path.append('./')
sys.path.append('../')
import webapp

service = webapp.get_service(5004, 'fn/names_text')

the_sample = None

def get_sample():
    global the_sample
    if the_sample == None:
        with codecs.open(webapp.find_resource('text-sample'), 'r', 'latin-1') as infile:
            the_sample = infile.read()
    return the_sample

class TestFnNamesText(webapp.WebappTestCase):
    @classmethod
    def get_service(self):
        return service

    def test_no_parameter(self):
        """No parameters.  Should yield some kind of error."""

        request = service.get_request('GET', {})
        x = self.start_request_tests(request)
        self.assertTrue(x.status_code >= 400)
        self.assertTrue(u'text' in x.json()[u'message'],
                        'error message from service is not informative: %s' % x.json()[u'message'])

    def test_large_input(self):
        """Test large input.
        40000 characters fails; 30000 succeeds.
        N.b. the input is copied to the output (u'input_text' result field).  
        That seems like a bad idea.
        TBD: design issue."""

        request = service.get_request('GET', {u'text': get_sample()[0:30000]})
        x = self.start_request_tests(request)
        self.assert_success(x)
        self.assertTrue(len(x.json()[u'scientificNames']) > 10)
        self.assertTrue(u'Papilio' in x.json()[u'scientificNames'])

    def test_engines(self):
        """It looks like engines 6, 7, and 8 are all the same.
        3 and 4 are the same as well.
        Maybe inadequate error checking?  In any case, there is *no* documentation
        of the engine parameter (in the old documentation).  TBD: issue."""

        for engine in range(0, 8):
            request = service.get_request('GET', {u'engine': engine, u'text': get_sample()[0:30000]})
            x = self.start_request_tests(request)
            # TBD: if range > ?? then x.status_code should be >= 400
            self.assert_success(x)
            self.assertTrue(len(x.json()[u'scientificNames']) > 10)
            self.assertTrue(u'Scolopendrella' in x.json()[u'scientificNames'])

    # Insert here: edge case tests
    # Insert here: inputs out of range, leading to error or long delay
    # Insert here: error-generating conditions
    # (See ../README.md)

    def test_example_4(self):
        x = self.start_request_tests(example_4)
        self.assert_success(x)
        # Insert: whether result is what it should be according to docs

    def test_example_5(self):
        x = self.start_request_tests(example_5)
        self.assert_success(x)
        # Insert: whether result is what it should be according to docs

null=None; false=False; true=True

example_5 = service.get_request('GET', {u'text': u'Formica polyctena is a species of European red wood ant in the genus Formica. The pavement ant, Tetramorium caespitum is an ant native to Europe. Pseudomyrmex is a genus of stinging, wasp-like ants. Adetomyrma venatrix is an endangered species of ants endemic to Madagascar. Carebara diversa is a species of ants in the subfamily Formicinae. It is found in many Asian countries.'})
example_4 = service.get_request('GET', {u'engine': u'2', u'text': u'The lemon dove (Columba larvata) is a species of bird in the pigeon family Columbidae found in montane forests of sub-Saharan Africa.'})

if __name__ == '__main__':
    webapp.main()
