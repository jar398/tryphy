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

service = webapp.get_service(5004, 'gt/ot/get_tree')

the_names = None

discard_unicode = True

def get_names():
    """Get a long list of names, for testing purposes.
    The list is stored in a file.  All the names in this file happen to 
    come from the GBIF backbone taxonomy dump."""

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

    def test_no_parameter(self):
        """See what happens when there are no parameters.
        This returns a 500 (as of 2017-10-30).  More HTTP-like would be for it to give a 400.
        But the error message is not informative.  TBD: issue."""

        request = service.get_request(self.__class__.http_method(), {})
        x = self.start_request_tests(request)
        self.assertTrue(x.status_code >= 400)
        self.assertTrue(u'taxa' in x.json()[u'message'],    #informative?
                        'no "taxa" in "%s"' % x.json()[u'message'])

    def test_no_names(self):
        """See what happens if there are no names.  Expect a 400."""

        request = service.get_request(self.__class__.http_method(), {'taxa': ' '})
        x = self.start_request_tests(request)
        self.assertTrue(x.status_code >= 400)
        # Error: 'taxa' parameter must have a valid value
        self.assertTrue(u'taxa' in x.json()[u'message'],    #informative?
                        'no "taxa" in "%s"' % x.json()[u'message'])

    def test_bad_names(self):
        """Try a set of names none of which will be seen as a taxon name.  
        Expect error since we need at least three good names to make a tree."""

        params = {'taxa': '|'.join(['Unicornx', 'Dragonx', 'Pegasusx'])}
        request = service.get_request(self.__class__.http_method(), params)
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

    def test_some_bad(self):
        """Two good names, one bad.
        Call should succeed even if some names are unrecognized, yes?"""

        params = {'taxa': '|'.join(['Pseudacris crucifer', 'Plethodon cinereus', 'Nosuch taxon'])}
        request = service.get_request(self.__class__.http_method(), params)
        x = self.start_request_tests(request)
        mess = x.json().get(u'message')
        # json.dump(x.to_dict(), sys.stdout, indent=2)
        # Oddly we get a 400 saying Error: Missing parameter 'taxa'
        # for same two services (see above)
        # TBD: issue.
        self.assert_success(x, mess)

    # Names containing non-ASCII Unicode all fail with:
    # "message": "Error: 'ascii' codec can't encode character u'\\xe1' in position 5529: ordinal not in range(128)"
    # TBD: issue - all methods should deal in Unicode, not ASCII.

    # After filtering out unicode, we get, at 512 names:
    # "message": "Error: 'results'"
    # No 'informative message' in the response.  TBD: Issue.
    # (It's probably because an Open Tree name lookup failed.)

    # 256 names works (for gt/ot/get_tree).  512 doesn't.

    @unittest.skip("temporarily")
    def test_bigger_and_bigger(self):
        """Try the service with increasingly long name lists."""

        names = get_names()
        for i in range(6, 19):
            if i > len(names): break
            n = 2**i
            param = '|'.join(names[0:n]) # Asssume GET
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
        """Note: The example_12 tree includes both Formicinae and Aculeata, but the response
        does not list any supporting studies.  According to the OT tree browser,
        there are supporting trees that include both.  Need to investigate.
        Issue?"""

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


example_13 = service.get_request('GET', {u'taxa': u'Setophaga striata|Setophaga magnolia|Setophaga angelae|Setophaga plumbea|Setophaga virens'})

if __name__ == '__main__':
    webapp.main()
