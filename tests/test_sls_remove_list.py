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

    # Insert here: edge case tests
    # Insert here: inputs out of range, leading to error or long delay
    # Insert here: error-generating conditions
    # (See ../README.md)

    def test_example_32(self):
        (user_id, access_token) = self.user_credentials()
        example_32 = service.get_request('GET', {u'user_id': user_id, u'access_token': access_token, u'list_id': u'2'})
        x = self.start_request_tests(example_32)
        # Insert: whether result is what it should be according to docs

    def tearDown(self):
        print 'cleaning up'
        lists.cleanup()
        webapp.WebappTestCase.tearDown(self)

if __name__ == '__main__':
    webapp.main()
