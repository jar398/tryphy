# 10. sl/eol/get_links

# Parameter: list of species
# Result:
#   input_species - repeats input (issue: flush this)
#   message, status_code  as usual
#   meta_data - not very useful
#   species - list of blobs about species
#      eol_id
#      matched_name  - contains authority
#      searched_name  - presumably what was provided

import sys, unittest, json
sys.path.append('./')
sys.path.append('../')
import webapp

service = webapp.get_service(5004, 'sl/eol/get_links')

class SlEolGetLinksTester(webapp.WebappTestCase):
    def test_no_parameter(self):
        """What if no parameters are supplied?  (Hoping for 400.)"""

        m = self.__class__.http_method()
        service = self.__class__.get_service()
        x = service.get_request(m, None).exchange()
        self.assert_response_status(x, 400)
        # tbd: check for informativeness

    def test_bad_parameter(self):
        """What if the supplied parameter has the wrong name?  (Hoping for 400.)"""

        m = self.__class__.http_method()
        service = self.__class__.get_service()
        x = service.get_request(m, {u'bad_parameter': u'Nosuchtaxonia notatall'}).exchange()
        self.assert_response_status(x, 400)
        # Check for informativeness
        mess = x.json()[u'message']
        self.assertTrue(u'species' in mess, mess)

    def test_bad_species(self):
        """What if the species name is unknown?"""

        m = self.__class__.http_method()
        service = self.__class__.get_service()
        x = service.get_request(m, {u'species': u'Nosuchtaxonia notatall'}).exchange()
        # json.dump(x.to_dict(), sys.stdout, indent=2)
        # TBD: Issue: Not documented what happens in this case.
        self.assert_success(x)
        self.assertEqual(x.json()[u'species'][0][u'matched_name'], '')

    # Insert here: edge case tests
    # Insert here: inputs out of range, leading to error or long delay
    # Insert here: error-generating conditions
    # (See ../README.md)


class TestSlEolGetLinks(SlEolGetLinksTester):
    @classmethod
    def get_service(self):
        return service

    @classmethod
    def http_method(self):
        return 'GET'

    def test_example_23(self):
        x = self.start_request_tests(example_23)
        self.assert_success(x)
        # Insert: whether result is what it should be according to docs

null=None; false=False; true=True

example_23 = service.get_request('GET', {u'species': u'Panthera leo|Panthera onca|Panthera pardus'})

if __name__ == '__main__':
    webapp.main()
