# 13. sls/replace_species  - edit a list.

import sys, unittest, json
sys.path.append('./')
sys.path.append('../')
import webapp, lists

service = webapp.get_service(5005, 'sls/replace_species')

class TestSlsReplaceSpecies(webapp.WebappTestCase):
    @classmethod
    def get_service(cls):
        return service

    list_id = None

    @classmethod
    def setUpClass(cls):
        webapp.WebappTestCase.setUpClass()
        cls.list_id = lists.insert_sample_list()

    # Insert here: edge case tests
    # Insert here: inputs out of range, leading to error or long delay
    # Insert here: error-generating conditions
    # (See ../README.md)

    def test_example_31(self):
        (user_id, access_token) = self.user_credentials()
        list_id = self.__class__.list_id
        example_31 = service.get_request('POST',
                                         {u'access_token': access_token,
                                          u'user_id': user_id,
                                          u'species': [{u'family': u'', u'scientific_name': u'Aix sponsa', u'scientific_name_authorship': u'', u'vernacular_name': u'Wood Duck', u'phylum': u'', u'nomenclature_code': u'ICZN', u'order': u'Anseriformes'}, {u'family': u'', u'scientific_name': u'Anas strepera', u'scientific_name_authorship': u'', u'vernacular_name': u'Gadwall', u'phylum': u'', u'nomenclature_code': u'ICZN', u'order': u'Anseriformes'}],
                                          u'list_id': list_id})
        x = self.start_request_tests(example_31)
        self.assert_success(x)
        # Insert: whether result is what it should be according to docs

    @classmethod
    def tearDownClass(cls):
        print 'cleaning up'
        lists.cleanup()
        webapp.WebappTestCase.tearDownClass()    # ??

if __name__ == '__main__':
    webapp.main()
