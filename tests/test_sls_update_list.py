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

    # Insert here: edge case tests
    # Insert here: inputs out of range, leading to error or long delay
    # Insert here: error-generating conditions
    # (See ../README.md)

    def test_example_33(self):
        x = self.start_request_tests(example_33)
        # Insert: whether result is what it should be according to docs

    def test_example_34(self):
        x = self.start_request_tests(example_34)
        # Insert: whether result is what it should be according to docs

null=None; false=False; true=True

example_33 = service.get_request('POST', {u'access_token': u'ya29..zQLmLjbyujJjwV6RVSM2sy-mkeaKu-9_n7y7iB6uKuL-rHDGp3W2_hPWUSO5uX_OcA', u'user_id': u'hdail.laughinghouse@gmail.com', u'list': {u'list_title': u'Virginia Invasive Plant Species List', u'list_description': u'The list contains information on the invasive plants of Virginia, with data on the Invasiveness Rank and region in which they occur'}, u'list_id': 5})
example_34 = service.get_request('POST', {u'access_token': u'ya29..zQLmLjbyujJjwV6RVSM2sy-mkeaKu-9_n7y7iB6uKuL-rHDGp3W2_hPWUSO5uX_OcA', u'user_id': u'hdail.laughinghouse@gmail.com', u'list': {u'is_list_public': True}, u'list_id': 5})

if __name__ == '__main__':
    webapp.read_requests('work/requests.json')
    webapp.read_exchanges('work/exchanges.json')
    unittest.main()
