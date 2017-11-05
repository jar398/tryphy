# 11. sls/get_list

# Access token is required in two cases:
#   - want to look at list of all lists
#   - want to look at private lists

import sys, unittest, json
sys.path.append('./')
sys.path.append('../')
import webapp, lists

service = webapp.get_service(5005, 'sls/get_list')

class TestSlsGetList(webapp.WebappTestCase):
    @classmethod
    def get_service(self):
        return service

    # TBD: setup should create lists to probe for.

    list_id = None
    private_list_id = None

    @classmethod
    def setUpClass(cls):
        webapp.WebappTestCase.setUpClass()
        # Put a list into the repository (it will be removed afterwards)
        cls.list_id = lists.insert_sample_list()
        cls.private_list_id = lists.insert_sample_list(public=False)

    # What if we give it an unknown parameter name?  Should complain.
    # TBD: Issue: we get a 200.

    def test_invalid_parameter(self):
        # To get all the public lists available:
        req = service.get_request('GET', {u'last_id': u'2'})
        x = self.start_request_tests(req)
        self.assert_response_status(x, 400)
        # TBD: check for informativeness.

    # What if we ask for a list that doesn't exist?

    def test_no_such_list(self):
        # To get a specific public list:
        example_26 = service.get_request('GET', {u'list_id': u'9999999'})
        x = self.start_request_tests(example_26)
        # Fails with 409 Conflict 'No list found with ID 9999999'.
        # That seems an odd status code for this situation. (tbd: issue)
        # 404 might be better (if you can consider a list a 'resource').
        if x.status_code != 404:
            self.assert_response_status(x, 400)

    # Insert here: edge case tests
    # Insert here: inputs out of range, leading to error or long delay
    # Insert here: error-generating conditions
    # (See ../README.md)

    def test_example_25(self):
        # To get all the public lists available:
        example_25 = service.get_request('GET', None)
        x = self.start_request_tests(example_25)
        self.assert_success(x)
        # Insert: whether result is what it should be according to docs

    # What if we ask for a list that DOES exist?  Should work.
    # (List should be created in the unittest setup method.)

    def test_example_26(self):
        # To get a specific public list:
        list_id = self.__class__.list_id
        example_26 = service.get_request('GET', {u'list_id': list_id})
        x = self.start_request_tests(example_26)
        self.assert_success(x)
        # Insert: whether result is what it should be according to docs

    def test_example_27(self):
        (user_id, access_token) = self.user_credentials()
        example_27 = service.get_request('GET', {u'access_token': access_token, u'user_id': user_id})
        x = self.start_request_tests(example_27)
        # Insert: whether result is what it should be according to docs
        self.assert_success(x)

    def test_example_28(self):
        (user_id, access_token) = self.user_credentials()
        private_list_id = self.__class__.private_list_id
        example_28 = service.get_request('GET', {u'access_token': access_token, u'user_id': user_id,
                                                 u'list_id': private_list_id})
        x = self.start_request_tests(example_28)
        # Insert: whether result is what it should be according to docs
        self.assert_success(x)

    def test_example_29(self):
        (user_id, access_token) = self.user_credentials()
        private_list_id = self.__class__.private_list_id
        example_29 = service.get_request('GET', {u'access_token': access_token, u'user_id': user_id,
                                                 u'verbose': u'true', u'list_id': private_list_id})
        x = self.start_request_tests(example_29)
        self.assert_success(x)
        # Insert: whether result is what it should be according to docs

    @classmethod
    def tearDownClass(cls):
        print 'cleaning up'
        lists.cleanup()
        webapp.WebappTestCase.tearDownClass()

if __name__ == '__main__':
    webapp.main()
