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
    Name: name
    Category: mandatory
    Data Type: string
    Description: list of scientific names delimited by pipe "|"

e.g.
curl -D - "http://phylo.cs.nmsu.edu:5004/phylotastic_ws/tnrs/ot/resolve?names=Psuedacris%20crucifer"
"""

import unittest, webapp, json, sys

smoke = True

class TestTnrsOtResolve(webapp.WebappTestCase):

    url = 'http://phylo.cs.nmsu.edu:5004/phylotastic_ws/tnrs/ot/resolve'
    service = webapp.get_service(url)

    def get_service(self):
        return TestTnrsOtResolve.service

    # Ensure that we get failure if names parameter is unsupplied.
    # The documentation says that the names parameter is 'mandatory'.
    def test_1(self):
        if smoke: return
        x = self.get_service().get_request('GET', None).exchange()
        self.assert_response_status(x, 400)

        # The documentation says we should get an 'informative message'
        # In this case we have: "Error: Missing parameter 'names'"
        # which is indeed informative.
        # How to test for informativeness?  How about just check to see
        # if the name of the missing parameter is present in the error
        # message.
        self.assertTrue(u'names' in x.text)

    # Edge case: names= is supplied, but there are no names.
    # In this case, the deployed web service says that there is no names
    # parameter.  (The difference between missing and supplied 
    # but null is academic?  Depends on taste.)
    def test_2(self):
        if smoke: return
        request = self.get_service().get_request('GET', {'names': ''})
        x = request.exchange()
        # 204 = no content (from open tree)
        # message = "Could not resolve any name"
        self.assert_response_status(x, 204)

    # Ensure that the result we get is 'correct' per documentation.
    # The Phylotastic documentation doesn't say anything about what is
    # returned; it simply links to the Open Tree documentation.
    # Maybe you're supposed to reverse engineer based on what the service
    # does?
    def test_3(self):
        if smoke: return
        name = u'Pseudacris crucifer'
        request = self.get_service().get_request('GET', {'names': name})
        x = request.exchange()
        self.assert_success(x)
        # Check that Pseudacris crucifer is among the matched names
        matched_names = all_matched_names(x)
        self.assertTrue(name in matched_names)

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

    # Examples from documentation:
    # http://phylo.cs.nmsu.edu:5004/phylotastic_ws/tnrs/ot/resolve?names=Setophaga striata|Setophaga megnolia|Setophaga angilae|Setophaga plumbea|Setophaga virens
    # http://phylo.cs.nmsu.edu:5004/phylotastic_ws/tnrs/ot/resolve?names=Formica polyctena|Formica exsectoides|Formica pecefica

    # There's no such thing as 'Setophaga megnolia'

    def test_4(self):
        if smoke: return
        names = [(u'Setophaga striata', True),
                 (u'Setophaga megnolia', False),
                 (u'Setophaga angilae', False),
                 (u'Setophaga plumbea', True),
                 (u'Setophaga virens', True)]
        self.try_names(names)

    def try_names(self, names):
        request = self.get_service().get_request('GET', {'names': u'|'.join([name for (name, tf) in names])})
        x = request.exchange()
        self.assert_success(x)
        matched_names = all_matched_names(x)
        for (name, tf) in names:
            outcome = ((name in matched_names) == tf)
            if not outcome:
                print name, 'not in matched_names'
                print 'json:'
                json.dump(x.json(), sys.stdout, indent=2)
            self.assertTrue(outcome)

    def test_5(self):
        names = [(u'Formica polyctena', True),
                 (u'Formica exsectoides', True),
                 (u'Formica pecefica', False)]
        self.try_names(names)

def all_matched_names(x):
    j = x.json()
    matches = j[u'resolvedNames']
    return ([m[u'matched_name'] for m in matches] +
            [synonym for synonym in m[u'synonyms'] for m in matches])


if __name__ == '__main__':
    webapp.read_exchanges('work/exchanges.json')
    unittest.main()
