# 14. sls/remove_list
# Method is GET (but ought to be POST or DELETE)

import sys, unittest, json
sys.path.append('./')
sys.path.append('../')
import webapp, lists

url = 'http://phylo.cs.nmsu.edu:5005/phylotastic_ws/sls/remove_list'
service = webapp.get_service(url)

class TestSlsRemoveList(webapp.WebappTestCase):
    @classmethod
    def get_service(self):
        return service

    list_id = None

    @classmethod
    def setUpClass(cls):
        # TBD: Create a list to operate on.
        list_id = u'2'

    # What is we give it a bad access token?

    def test_bad_token(self):
        user_id = webapp.config('user_id')
        list_id = self.__class__.list_id
        example_32 = service.get_request('GET', {u'user_id': user_id,
                                                 u'access_token': u'invalid token',
                                                 u'list_id': list_id})
        x = self.start_request_tests(example_32)
        # Insert: whether result is what it should be according to docs
        self.assert_response_status(x, 401)
        json.dump(x.to_dict(), sys.stdout, indent=2)

    # Insert here: edge case tests
    # Insert here: inputs out of range, leading to error or long delay
    # Insert here: error-generating conditions
    # (See ../README.md)

    def test_example_32(self):
        (user_id, access_token) = self.user_credentials()
        list_id = self.__class__.list_id
        example_32 = service.get_request('GET', {u'user_id': user_id,
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
