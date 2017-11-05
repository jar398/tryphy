# 17. ms/get_studies
# Get supported studies of an induced tree from OpenTreeOfLife.
# Parameters:
#   list
#   list_type

import sys, unittest, json
sys.path.append('./')
sys.path.append('../')
import webapp

service = webapp.get_service(5006, 'md/get_studies')

class MdStudiesTester(webapp.WebappTestCase):
    def foo(self):
        return 3

class TestMdGetStudies(MdStudiesTester):
    @classmethod
    def get_service(self):
        return service

    @classmethod
    def http_method(self):
        return 'GET'

    # Insert here: edge case tests
    # Insert here: inputs out of range, leading to error or long delay
    # Insert here: error-generating conditions
    # (See ../README.md)

    def test_example_36(self):
        x = self.start_request_tests(example_36)
        mess = x.json().get(u'message')
        self.assert_success(x, mess)
        # Insert: whether result is what it should be according to docs

    def test_example_37(self):
        x = self.start_request_tests(example_37)
        mess = x.json().get(u'message')
        self.assert_success(x, mess)
        # Insert: whether result is what it should be according to docs

null=None; false=False; true=True

example_36 = service.get_request('GET', {u'list': u'3597191|3597209|3597205|60236|3597195', u'list_type': u'ottids'})
example_37 = service.get_request('GET', {u'list': u'Setophaga striata|Setophaga magnolia|Setophaga angelae|Setophaga plumbea|Setophaga virens', u'list_type': u'taxa'})

if __name__ == '__main__':
    webapp.main()
