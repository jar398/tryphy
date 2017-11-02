# STUB

import sys, unittest, json
sys.path.append("../")
import webapp

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
        x = self.start_request_tests(example_32)
        # Insert: whether result is what it should be according to docs

null=None; false=False; true=True

example_32 = service.get_request('GET', {u'access_token': u'ya29..zQLmLjbyujJjwV6RVSM2sy-mkeaKu-9_n7y7iB6uKuL-rHDGp3W2_hPWUSO5uX_OcA', u'user_id': u'hdail.laughinghouse@gmail.com', u'list_id': u'2'})

if __name__ == '__main__':
    webapp.main()
