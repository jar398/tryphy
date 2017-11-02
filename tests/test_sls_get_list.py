# STUB

import sys, unittest, json
sys.path.append("../")
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

    def test_example_25(self):
        x = self.start_request_tests(example_25)
        # Insert: whether result is what it should be according to docs

    def test_example_26(self):
        x = self.start_request_tests(example_26)
        # Insert: whether result is what it should be according to docs

    def test_example_28(self):
        x = self.start_request_tests(example_28)
        # Insert: whether result is what it should be according to docs

    def test_example_27(self):
        x = self.start_request_tests(example_27)
        # Insert: whether result is what it should be according to docs

null=None; false=False; true=True

example_29 = service.get_request('GET', {u'access_token': u'ya29..zQLmLjbyujJjwV6RVSM2sy-mkeaKu-9_n7y7iB6uKuL-rHDGp3W2_hPWUSO5uX_OcA', u'user_id': u'hdail.laughinghouse@gmail.com', u'verbose': u'true', u'list_id': u'20'})
example_25 = service.get_request('GET', None)
example_26 = service.get_request('GET', {u'list_id': u'22'})
example_28 = service.get_request('GET', {u'access_token': u'ya29..zQLmLjbyujJjwV6RVSM2sy-mkeaKu-9_n7y7iB6uKuL-rHDGp3W2_hPWUSO5uX_OcA', u'user_id': u'hdail.laughinghouse@gmail.com', u'list_id': u'20'})
example_27 = service.get_request('GET', {u'access_token': u'ya29..zQLmLjbyujJjwV6RVSM2sy-mkeaKu-9_n7y7iB6uKuL-rHDGp3W2_hPWUSO5uX_OcA', u'user_id': u'hdail.laughinghouse@gmail.com'})

if __name__ == '__main__':
    webapp.main()
