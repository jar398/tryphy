# 14. sls/remove_list
# Method is GET (but ought to be POST or DELETE)

import sys, unittest, json
sys.path.append('./')
sys.path.append('../')
import webapp, lists

url = 'http://phylo.cs.nmsu.edu:5005/phylotastic_ws/sls/remove_list'
service = webapp.get_service(url)
http_method = 'GET'

class TestSlsRemoveList(webapp.WebappTestCase):
    @classmethod
    def get_service(self):
        return service

    list_id = None

    @classmethod
    def setUpClass(cls):
        webapp.WebappTestCase.setUpClass()
        # TBD: Create a list to operate on.
        list_id = u'2'
        lists.temporary_lists.append(list_id)

    # What is we give it a bad access token?
    # It says "400 Error: Missing parameter 'list_id'" - which is
    # wrong in two ways.
    # tbd: issue

    def test_bad_token(self):
        user_id = webapp.config('user_id')
        list_id = self.__class__.list_id
        example_32 = service.get_request(http_method,
                                         {u'user_id': user_id,
                                          u'access_token': u'invalid token',
                                          u'list_id': list_id})
        x = self.start_request_tests(example_32)
        # Insert: whether result is what it should be according to docs
        self.assert_response_status(x, 401)
        # Informative error message?  Hard to say what is should be.  
        # Something about a token maybe.
        mess = x.json().get(u'message')
        self.assertTrue(u'oken' in mess)
        json.dump(x.to_dict(), sys.stdout, indent=2)

    # Insert here: edge case tests
    # Insert here: inputs out of range, leading to error or long delay
    # Insert here: error-generating conditions
    # (See ../README.md)

    def test_example_32(self):
        (user_id, access_token) = self.user_credentials()
        list_id = self.__class__.list_id
        example_32 = service.get_request(http_method,
                                         {u'user_id': user_id,
                                          u'access_token': access_token,
                                          u'list_id': list_id})
        x = self.start_request_tests(example_32)
        mess = x.json().get(u'message')
        self.assert_success(x, mess)
        # Insert: whether result is what it should be according to docs

    @classmethod
    def tearDownClass(cls):
        print 'cleaning up'
        lists.cleanup()
        webapp.WebappTestCase.tearDownClass()

if __name__ == '__main__':
    webapp.main()
