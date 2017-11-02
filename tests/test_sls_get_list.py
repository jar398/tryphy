# 11. sls/get_list
# Important: run the list creation tests first (sls/insert_list)

import sys, unittest, json
sys.path.append('./')
sys.path.append('../')
import webapp

url = 'http://phylo.cs.nmsu.edu:5005/phylotastic_ws/sls/get_list'
service = webapp.get_service(url)

class TestSlsGetList(webapp.WebappTestCase):
    @classmethod
    def get_service(self):
        return service

    # Insert here: edge case tests
    # Insert here: inputs out of range, leading to error or long delay
    # Insert here: error-generating conditions
    # (See ../README.md)

    def test_example_29(self):
        x = self.start_request_tests(example_29)
        # Insert: whether result is what it should be according to docs
        self.assert_success(x)

    def test_example_25(self):
        x = self.start_request_tests(example_25)
        # Insert: whether result is what it should be according to docs
        self.assert_success(x)

    def test_example_26(self):
        x = self.start_request_tests(example_26)
        # Insert: whether result is what it should be according to docs
        # Fails; I'm not sure what it's supposed to do.
        # List ids are 'unique' and 'public'.
        # Assume that list 22 does not exist (it doesn't exist now, 2017-11-02).
        self.assert_response_status(x, 400)

    def test_example_28(self):
        x = self.start_request_tests(example_28)
        # Insert: whether result is what it should be according to docs
        self.assert_success(x)

    def test_example_27(self):
        x = self.start_request_tests(example_27)
        # Insert: whether result is what it should be according to docs
        self.assert_success(x)

user_id = webapp.config(u'user_id')
access_token = webapp.config(u'access_token')    # Expires in 1 hour.

null=None; false=False; true=True
example_29 = service.get_request('GET', {u'access_token': access_token, u'user_id': user_id, u'verbose': u'true', u'list_id': u'20'})
example_25 = service.get_request('GET', None)
example_26 = service.get_request('GET', {u'list_id': u'22'})
example_28 = service.get_request('GET', {u'access_token': access_token, u'user_id': user_id, u'list_id': u'20'})
example_27 = service.get_request('GET', {u'access_token': access_token, u'user_id': user_id})

if __name__ == '__main__':
    webapp.main()
