# STUB

import sys, unittest, json
sys.path.append('./')
sys.path.append('../')
import webapp, lists

url = 'http://phylo.cs.nmsu.edu:5005/phylotastic_ws/sls/update_list'
service = webapp.get_service(url)

class TestSlsUpdateList(webapp.WebappTestCase):
    @classmethod
    def get_service(self):
        return service

    list_id = None

    @classmethod
    def setUpClass(self):
        webapp.WebappTestCase.setUpClass()
        # TBD: Create a list to operate on.
        list_id = u'2'
        lists.temporary_lists.append(list_id)

    # Insert here: edge case tests
    # Insert here: inputs out of range, leading to error or long delay
    # Insert here: error-generating conditions
    # (See ../README.md)

    def test_example_33(self):
        (user_id, access_token) = self.user_credentials()
        list_id = self.__class__.list_id
        example_33 = service.get_request('POST',
                                         {u'access_token': access_token,
                                          u'user_id': user_id,
                                          u'list': {u'list_title': u'Virginia Invasive Plant Species List', u'list_description': u'The list contains information on the invasive plants of Virginia, with data on the Invasiveness Rank and region in which they occur'},
                                          u'list_id': list_id})
        x = self.start_request_tests(example_33)
        mess = x.json().get(u'message')
        self.assert_success(x, mess)
        # Insert: whether result is what it should be according to docs

    def test_example_34(self):
        (user_id, access_token) = self.user_credentials()
        list_id = self.__class__.list_id
        example_34 = service.get_request('POST',
                                         {u'access_token': access_token,
                                          u'user_id': user_id,
                                          u'list': {u'is_list_public': True},
                                          u'list_id': list_id})
        mess = x.json().get(u'message')
        self.assert_success(x, mess)

    @classmethod
    def tearDownClass(cls):
        print 'cleaning up'
        lists.cleanup()
        webapp.WebappTestCase.tearDownClass()


if __name__ == '__main__':
    webapp.main()
