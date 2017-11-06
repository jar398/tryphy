# 3. tnrs/ot/resolve
# GET

# To skip a test, do this: @unittest.skip("skipping")

"""
https://github.com/phylotastic/phylo_services_docs/blob/master/ServiceDescription/PhyloServicesDescription.md

Web Service 3.
Service Name: Resolve Scientific Names with Open Tree TNRS
Service Description: A service which resolves lists of scientific names 
  against known sources. 
Resource URI: http://phylo.cs.nmsu.edu:5004/phylotastic_ws/tnrs/ot/resolve
HTTP Method: GET
Input Format: application/x-www-form-urlencoded
Output Format: application/json
Parameters:
    Name: names
    Category: mandatory
    Data Type: string
    Description: list of scientific names delimited by pipe "|"

e.g.
curl -D - "http://phylo.cs.nmsu.edu:5004/phylotastic_ws/tnrs/ot/resolve?names=Psuedacris%20crucifer"
"""

import sys, os, unittest, json
sys.path.append('./')
sys.path.append('../')
import webapp

service = webapp.get_service(5004, 'tnrs/ot/resolve')

class TnrsTester(webapp.WebappTestCase):
    # Insert here: edge case tests
    # Insert here: inputs out of range, leading to error or long delay
    # Insert here: error-generating conditions
    # (See ../README.md)

    def test_no_parameter(self):
        """Edge case:
        Ensure that we get failure if names parameter is unsupplied.
        The documentation says that the names parameter is 'mandatory'."""

        m = self.__class__.http_method()
        service = self.__class__.get_service()
        x = service.get_request(m, None).exchange()
        self.assert_response_status(x, 400)

        # The documentation says we should get an 'informative message'
        # In this case we have: "Error: Missing parameter 'names'"
        # which is indeed informative.
        # How to test for informativeness?  How about just check to see
        # if the name of the missing parameter is present in the error
        # message.
        self.assertTrue('ame' in x.json()[u'message'])

    def test_3(self):
        """Ensure that the result we get is 'correct' per documentation.
        The Phylotastic documentation doesn't say anything about what is
        returned; it simply links to the Open Tree documentation.
        Maybe you're supposed to reverse engineer based on what the service
        does?"""

        name = u'Pseudacris crucifer'
        m = self.http_method()
        request = self.__class__.tnrs_request(['Pseudacris crucifer'])
        x = request.exchange()
        self.assert_success(x)
        # Check that Pseudacris crucifer is among the matched names
        matched_names = self.all_matched_names(x)
        self.assertTrue(name in matched_names)

    def test_4(self):
        """What if one of the names is misspelled?
        There's no such thing as 'Setophaga megnolia'."""

        namesx = [(u'Setophaga striata', True),
                  (u'Setophaga megnolia', False),
                  (u'Setophaga angilae', False),
                  (u'Setophaga plumbea', True),
                  (u'Setophaga virens', True)]
        self.try_names(namesx)

    def try_names(self, namesx):
        m = self.http_method()
        request = self.__class__.tnrs_request([name for (name, tf) in namesx])
        x = request.exchange()
        self.assert_success(x)
        matched_names = self.all_matched_names(x)
        for (name, tf) in namesx:
            outcome = ((name in matched_names) == tf)
            if not outcome:
                print name, 'not in matched_names'
                print 'json:'
                json.dump(x.json(), sys.stdout, indent=2)
            self.assertTrue(outcome)

    def all_matched_names(self, x):
        """Utility for some of the tests; weak test of correct returned value"""

        j = x.json()
        self.assertTrue(u'resolvedNames' in j)
        matches = j[u'resolvedNames']
        names = []
        for m in matches:
            # Oh right.  The form of the result changed between September 2017 and
            # some time in October.
            self.assertTrue(u'matched_results' in m,
                            'no matched_results key in %s' % list(m.keys()))
            for r in m[u'matched_results']:
                self.assertTrue(u'matched_name' in r,
                                'no matched_name key in %s' % list(r.keys()))
                names.append(r[u'matched_name'])
                self.assertTrue(u'synonyms' in r,
                                'no synonyms key in %s' % list(r.keys()))
                names.extend(r[u'synonyms'])
        return names

    def test_5(self):
        namesx = [(u'Formica polyctena', True),
                  (u'Formica exsectoides', True),
                  (u'Formica pecefica', False)]
        self.try_names(namesx)

    @unittest.skip("temporarily to save time")
    def test_big_request(self):
        """Try a request with many copies of the same name.
        128 copies succeeds, 256 fails (assuming GET - POST might be 
        more capacious)."""
        n = 1
        names = [u'Formica polyctena']
        m = self.http_method()
        while True:
            print >>sys.stderr, 'Testing big request %s' % n
            request = self.__class__.tnrs_request(names)
            x = request.exchange()
            if x.status_code != 200:
                print >>sys.stderr, 'Big request status %s at %s names' % (x.status_code, n)
                print >>sys.stderr, x.text
                break
            n = n * 2
            if n > 10000000: break
            names = names + names

    """
    {"total_names": 1, 
     "resolvedNames": [{"match_type": "Exact",
                        "resolver_name": "OT",
                        "matched_name": "Pseudacris",
                        "search_string": "pseudacris",
                        "synonyms": ["Limnaoedus", "Pseudachris", "Pseudacris"], 
                        "taxon_id": 173133}],
     "input_query": ["Pseudacris"],
     "service_url_doc": "https://github.com/phylotastic/phylo_services_docs/blob/master/ServiceDescription/PhyloServicesDescription.md#web-service-3",
     "execution_time": "0.38",
     "status_code": 200, 
     "message": "Success", 
     "creation_time": "2017-09-15T14:22:42.613526"}
    """


class TestTnrsOtResolve(TnrsTester):
    @classmethod
    def get_service(cls):
        return service

    @classmethod
    def http_method(cls):
        return 'GET'

    @classmethod
    def namelist(cls, x):
        return x.json()[u'names'].split('|')

    @classmethod
    def tnrs_request(cls, names):
        return service.get_request('GET', {'names': u'|'.join(names)})

    def test_2(self):
        """Edge case: names= is supplied, but there are no names.
        In this case, the deployed web service says that there is no names
        parameter.  (The difference between missing and supplied 
        but null is academic?  Depends on taste.)"""

        m = self.http_method()
        request = self.__class__.tnrs_request([])
        x = request.exchange()
        # 204 = no content (from open tree)
        # message = "Could not resolve any name"
        # Changed: now returns 400, not 204.  Better.
        self.assert_response_status(x, 400)

    def test_example_6(self):
        x = self.start_request_tests(example_6)
        self.assert_success(x)
        # Insert: whether result is what it should be according to docs

    def test_example_7(self):
        x = self.start_request_tests(example_7)
        self.assert_success(x)
        # Insert: whether result is what it should be according to docs

null=None; false=False; true=True

example_6 = service.get_request('GET', {u'names': u'Setophaga striata|Setophaga megnolia|Setophaga angilae|Setophaga plumbea|Setophaga virens'})
example_7 = service.get_request('GET', {u'names': u'Formica polyctena|Formica exsectoides|Formica pecefica'})

if __name__ == '__main__':
    webapp.main()
