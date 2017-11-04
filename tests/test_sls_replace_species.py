# 13. sls/replace_species  - edit a list.

import sys, unittest, json
sys.path.append("../")
import webapp, lists

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
        (user_id, access_token) = self.user_credentials()
        example_31 = service.get_request('POST',
                                         {u'access_token': access_token,
                                          u'user_id': u'user_id',
                                          u'species': [{u'family': u'', u'scientific_name': u'Aix sponsa', u'scientific_name_authorship': u'', u'vernacular_name': u'Wood Duck', u'phylum': u'', u'nomenclature_code': u'ICZN', u'order': u'Anseriformes'}, {u'family': u'', u'scientific_name': u'Anas strepera', u'scientific_name_authorship': u'', u'vernacular_name': u'Gadwall', u'phylum': u'', u'nomenclature_code': u'ICZN', u'order': u'Anseriformes'}], u'list_id': 2})
        x = self.start_request_tests(example_31)
        # Insert: whether result is what it should be according to docs

    def tearDown(self):
        print 'cleaning up'
        lists.cleanup()
        webapp.WebappTestCase.tearDown(self)

if __name__ == '__main__':
    webapp.main()
