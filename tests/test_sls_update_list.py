# STUB

import sys, unittest, json
sys.path.append("../")
import webapp

url = 'http://phylo.cs.nmsu.edu:5005/phylotastic_ws/sls/update_list'
service = webapp.get_service(url)

class TestSlsUpdateList(webapp.WebappTestCase):
    @classmethod
    def get_service(self):
        return service

    list_id = None

    @classmethod
    def setUpClass(self):
        # TBD: Create a list to operate on.
        list_id = u'2'

    # Insert here: edge case tests
    # Insert here: inputs out of range, leading to error or long delay
    # Insert here: error-generating conditions
    # (See ../README.md)

    def test_example_33(self):
        (user_id, access_token) = self.user_credentials()
        example_33 = service.get_request('POST',
                                         {u'access_token': access_token,
                                          u'user_id': user_id,
                                          u'list': {u'list_title': u'Virginia Invasive Plant Species List', u'list_description': u'The list contains information on the invasive plants of Virginia, with data on the Invasiveness Rank and region in which they occur'},
                                          u'list_id': list_id})
        x = self.start_request_tests(example_33)
        # Insert: whether result is what it should be according to docs

    def test_example_34(self):
        (user_id, access_token) = self.user_credentials()
        example_34 = service.get_request('POST',
                                         {u'access_token': access_token,

    @classmethod
    def tearDownClass(cls):
        print 'cleaning up'
        lists.cleanup()
        webapp.WebappTestCase.tearDownClass(TestSlsUpdateList)    # ??


if __name__ == '__main__':
    webapp.main()
