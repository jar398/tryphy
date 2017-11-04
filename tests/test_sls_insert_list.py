# 12. sls/insert_list
# Oddly, no access_token is required.  Issue?

import sys, unittest, json
sys.path.append('./')
sys.path.append('../')
import webapp, lists

url = 'http://phylo.cs.nmsu.edu:5005/phylotastic_ws/sls/insert_list'
service = webapp.get_service(url)

class TestSlsInsertList(webapp.WebappTestCase):
    @classmethod
    def get_service(self):
        return service

    # Insert here: edge case tests
    # Insert here: inputs out of range, leading to error or long delay
    # Insert here: error-generating conditions
    # (See ../README.md)

    # Very strange - this test appears to succeed, even if the access
    # token is expired.  I don't know what behavior is intended.  The
    # new documentation says nothing about what happens in this situation.

    # Hypothesis: you get a fresh list id, but the list is not
    # actually stored on the server.  (Evidence: I don't see the list
    # in the web UI.)

    def test_example_no_access(self):
        user_id = webapp.config('user_id')
        access_token = None
        example_30 = make_example_30(user_id, None)
        x = self.start_request_tests(example_30)
        mess = x.json().get(u'message')
        if x.status_code == 200:
            id = x.json()[u'list_id']
            lists.temporary_lists.append(id)
            print 'list id:', id
        # What's the right status code?  Is a list a 'resource'?
        self.assert_response_status(x, 404, mess)
        json.dump(x.to_dict(), sys.stderr, indent=2)

    def test_example_30(self):
        (user_id, access_token) = self.user_credentials()    # Expires in 1 hour.
        example_30 = make_example_30(user_id, access_token)
        x = self.start_request_tests(example_30)
        # Insert: whether result is what it should be according to docs
        self.assert_success(x)
        json.dump(x.to_dict(), sys.stderr, indent=2)
        id = x.json()[u'list_id']
        lists.temporary_lists.append(id)
        print 'list id:', id

    def tearDown(self):
        print 'cleaning up'
        lists.cleanup()
        webapp.WebappTestCase.tearDown(self)

def make_example_30(user_id, access_token):
    j = {u'user_id': user_id,
         u'list': {u'list_extra_info': u'', u'list_description': u'A list on the bird species add their endangered, threatened or invasive status', u'list_keywords': [u'bird', u'endangered species', u'Everglades'], u'list_curator': u'HD Laughinghouse', u'list_origin': u'webapp', u'list_curation_date': u'02-24-2016', u'list_source': u'Des', u'list_date_published': u'01-01-2006', u'list_focal_clade': u'Aves', u'list_title': u'Bird Species List for Everglades National Park', u'list_author': [u'Bass', u'O. & Cunningham', u'R.'], u'list_species': [{u'family': u'', u'scientific_name': u'Aix sponsa', u'scientific_name_authorship': u'', u'order': u'Anseriformes', u'vernacular_name': u'Wood Duck', u'phylum': u'', u'nomenclature_code': u'ICZN', u'class': u''}, {u'family': u'', u'scientific_name': u'Anas strepera', u'scientific_name_authorship': u'', u'order': u'Anseriformes', u'vernacular_name': u'Gadwall', u'phylum': u'', u'nomenclature_code': u'ICZN', u'class': u''}, {u'family': u'', u'scientific_name': u'Caprimulgus vociferus', u'scientific_name_authorship': u'', u'order': u'Caprimulgiformes', u'vernacular_name': u'Whip-poor-will', u'phylum': u'', u'nomenclature_code': u'ICZN', u'class': u''}, {u'family': u'', u'scientific_name': u'Columba livia', u'scientific_name_authorship': u'', u'order': u'Columbiformes', u'vernacular_name': u'Rock Dove', u'phylum': u'', u'nomenclature_code': u'ICZN', u'class': u''}, {u'family': u'', u'scientific_name': u'Ceryle alcyon', u'scientific_name_authorship': u'', u'order': u'Coraciiformes', u'vernacular_name': u'Belted Kingfisher', u'phylum': u'', u'nomenclature_code': u'ICZN', u'class': u''}, {u'family': u'', u'scientific_name': u'Aramus guarauna', u'scientific_name_authorship': u'', u'order': u'Gruiformes', u'vernacular_name': u'Limpkin', u'phylum': u'', u'nomenclature_code': u'ICZN', u'class': u''}], u'is_list_public': True}}
    if access_token != None:
        j[u'access_token'] = access_token
    return service.get_request('POST', j)

if __name__ == '__main__':
    webapp.main()
