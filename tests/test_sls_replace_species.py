# STUB

import sys, unittest, json
sys.path.append("../")
import webapp

url = 'http://phylo.cs.nmsu.edu:5005/phylotastic_ws/sls/replace_species'
service = webapp.get_service(url)

class TestSlsReplaceSpecies(webapp.WebappTestCase):
    @classmethod
    def get_service(self):
        return service

    # Insert here: edge case tests
    # Insert here: inputs out of range, leading to error or long delay
    # Insert here: error-generating conditions
    # (See ../README.md)

    def test_example_31(self):
        x = self.start_request_tests(example_31)
        # Insert: whether result is what it should be according to docs

null=None; false=False; true=True

example_31 = service.get_request('POST', {u'access_token': u'ya29..zQLmLjbyujJjwV6RVSM2sy-mkeaKu-9_n7y7iB6uKuL-rHDGp3W2_hPWUSO5uX_OcA', u'user_id': u'hdail.laughinghouse@gmail.com', u'species': [{u'family': u'', u'scientific_name': u'Aix sponsa', u'scientific_name_authorship': u'', u'vernacular_name': u'Wood Duck', u'phylum': u'', u'nomenclature_code': u'ICZN', u'order': u'Anseriformes'}, {u'family': u'', u'scientific_name': u'Anas strepera', u'scientific_name_authorship': u'', u'vernacular_name': u'Gadwall', u'phylum': u'', u'nomenclature_code': u'ICZN', u'order': u'Anseriformes'}], u'list_id': 2})

if __name__ == '__main__':
    webapp.read_requests('work/requests.json')
    webapp.read_exchanges('work/exchanges.json')
    unittest.main()