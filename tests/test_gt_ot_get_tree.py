# 5. gt/ot/get_tree

"""
Here's how I made the some-names.txt file (list of sample names):

    egrep "genus|species" ~/a/ot/repo/reference-taxonomy/r/gbif-20160729/resource/taxonomy.tsv \
    | gcut -f 5 \
    | tail -50000 \
    > some-names.txt

I chose the number 50000 (names) in order to end up with a file of about a million bytes.

The file is in the git repository, so there should be no call to regenerate it.
"""

import sys, unittest, json, codecs
sys.path.append('./')
sys.path.append('../')
import webapp

url = 'http://phylo.cs.nmsu.edu:5004/phylotastic_ws/gt/ot/get_tree'
service = webapp.get_service(url)

the_names = None

discard_unicode = True

def get_names():
    global the_names
    if the_names == None:
        names_path = webapp.find_resource('some-names.txt')
        with codecs.open(names_path, 'r', 'utf-8') as infile:
            the_names = []
            for line in infile:
                if discard_unicode:
                    try:
                        line.encode('ascii')
                    except:
                        continue
                the_names.append(line.strip())
            print len(the_names), 'names'
    return the_names

class GtTreeTester(webapp.WebappTestCase):
    # No parameters.
    # This returns a 500 (as of 2017-10-30).  More http-like would be for it to give a 400.
    # But the error message is not informative.  TBD: issue.
    def test_no_parameter(self):
        request = service.get_request(self.__class__.http_method(), {})
        x = self.start_request_tests(request)
        self.assertTrue(x.status_code >= 400)
        self.assertTrue(u'taxa' in x.json()[u'message'],    #informative?
                        'no "taxa" in "%s"' % x.json()[u'message'])

    def test_no_names(self):
        request = service.get_request(self.__class__.http_method(), {'taxa': ' '})
        x = self.start_request_tests(request)
        self.assertTrue(x.status_code >= 400)
        # Error: 'taxa' parameter must have a valid value
        self.assertTrue(u'taxa' in x.json()[u'message'],    #informative?
                        'no "taxa" in "%s"' % x.json()[u'message'])

    def test_bad_names(self):
        request = service.get_request(self.__class__.http_method(), {'taxa': '|'.join(['Unicornx', 'Dragonx', 'Pegasusx'])})
        x = self.start_request_tests(request)
        self.assertTrue(x.status_code >= 400)
        # Expecting "Not enough valid nodes provided to construct a subtree 
        #   (there must be at least two)"
        # For tests/test_gt_pm_tree, we get tests/test_gt_pt_tree
        # "message": "Error: Missing parameter 'taxa'"
        # which doesn't make sense since we did supply 'taxa'.  TBD: issue
        mess = x.json().get(u'message')
        self.assertTrue(u'least' in mess,    #informative?
                        'no "least" in message: "%s"' % mess)

    # Call should succeed even if some names are unrecognized
    def test_some_bad(self):
        request = service.get_request(self.__class__.http_method(), {'taxa': '|'.join(['Pseudacris crucifer', 'Plethodon cinereus', 'Nosuch taxon'])})
        x = self.start_request_tests(request)
        mess = x.json().get(u'message')
        # json.dump(x.to_dict(), sys.stdout, indent=2)
        # Oddly we get a 400 saying Error: Missing parameter 'taxa'
        # for same two services (see above)
        # TBD: issue.
        self.assert_success(x, mess)

    # These all file with:
    # "message": "Error: 'ascii' codec can't encode character u'\\xe1' in position 5529: ordinal not in range(128)"
    # TBD: issue - all methods should deal in Unicode, not ASCII.

    # After filtering out unicode, we get, at 512 names:
    # "message": "Error: 'results'"
    # No 'informative message' in the response.  TBD: Issue.
    # (It's probably because an Open Tree name lookup failed.)

    # 256 names works.

    @unittest.skip("temporarily")
    def test_bigger_and_bigger(self):
        names = get_names()
        for i in range(6, 19):
            if i > len(names): break
            n = 2**i
            param = '|'.join(names[0:n])
            print 'Trying %s names' % n
            request = service.get_request(self.__class__.http_method(), {'taxa': param})
            x = self.start_request_tests(request)
            print x.time
            if x.status_code != 200:
                  with open('tmp.tmp', 'w') as outfile:
                    json.dump(x.to_dict(), outfile, indent=2)
                    outfile.write('\n')
            self.assert_success(x)
            self.assertTrue(u'newick' in x.json())
            newick = x.json()[u'newick']
            self.assertTrue(len(newick) > len(param),
                            '%s %s' % (len(newick), len(param)))

    # Insert here: edge case tests
    # Insert here: inputs out of range, leading to error or long delay
    # Insert here: error-generating conditions
    # (See ../README.md)

    def test_example_12(self):
        x = self.start_request_tests(example_12)
        self.assert_success(x)
        # Insert: whether result is what it should be according to docs
        self.assertTrue(u'Aculeata' in x.json()[u'newick'])

    def test_example_13(self):
        x = self.start_request_tests(example_13)
        self.assert_success(x)
        # Insert: whether result is what it should be according to docs
        # MRCA = Setophaga = OTT 285198
        self.assertTrue(u'newick' in x.json())
        self.assertTrue(u'ott285198' in x.json()[u'newick'])
        self.assertTrue(u'tree_metadata' in x.json())
        m = x.json()[u'tree_metadata']
        self.assertTrue(u'supporting_studies' in m)
        self.assertTrue(len(m[u'supporting_studies']) > 1)

class TestGtOtGetTree(GtTreeTester):
    @classmethod
    def http_method(cls):
        return 'GET'

    @classmethod
    def get_service(cls):
        return service

null=None; false=False; true=True

example_12 = service.get_request('GET', {u'taxa': u'Crabronidae|Ophiocordyceps|Megalyridae|Formica polyctena|Tetramorium caespitum|Pseudomyrmex|Carebara diversa|Formicinae'})
# example_12 tree includes both Formicinae and Aculeata, but the response
# does not list any supporting studies.  According to OT tree browser
# there is are supporting trees... need to investigate.


example_13 = service.get_request('GET', {u'taxa': u'Setophaga striata|Setophaga magnolia|Setophaga angelae|Setophaga plumbea|Setophaga virens'})

if __name__ == '__main__':
    webapp.main()
