# 16. compare_trees

import sys, unittest, json
sys.path.append('./')
sys.path.append('../')
import webapp

service = webapp.get_service(5006, 'compare_trees')

class TestCompareTrees(webapp.WebappTestCase):
    @classmethod
    def get_service(self):
        return service

    def test_no_parameters(self):
        """What if no parameters are supplied?
        Fails, because 500 response 'no parameters' instead of 400.  Issue."""

        x = self.start_request_tests(service.get_request('POST', None))
        self.assert_response_status(x, 400)
        self.assertTrue('tree' in x.json()[u'message'])

    def test_no_parameters_2(self):
        x = self.start_request_tests(service.get_request('POST', {}))
        self.assert_response_status(x, 400)
        self.assertTrue('tree' in x.json()[u'message'])

    def test_missing_parameter(self):
        # What if only one parameter is supplied?
        x = self.start_request_tests(service.get_request('POST', {u'tree2_nwk': '((a,b)c)'}))
        self.assert_response_status(x, 400)
        self.assertTrue('tree1' in x.json()[u'message'])

    def test_bogus_newick(self):
        """What if the Newick is bad?
        Issue: uninformative 500 error message "global name 'Error' is not defined" """

        x = self.start_request_tests(service.get_request('POST', {u'tree1_nwk': '(a,b)c);',
                                                                  u'tree2_nwk': '((a,b)c'}))
        self.assert_response_status(x, 400)
        # json.dump(x.json(), sys.stdout, indent=2)
        mess = x.json()[u'message']
        # Not clear what the message ought to say; be prepared to change the 
        # following check to match the message that eventually gets chosen.
        self.assertTrue('yntax' in mess, mess)

    def test_different(self):
        """Does it always say the trees are the same? (It shouldn't.) """

        x = self.start_request_tests(service.get_request('POST', {u'tree1_nwk': '((a,b)c);',
                                                                  u'tree2_nwk': '(a,(b,c));'}))
        # Insert: whether result is what it should be according to docs
        self.assert_success(x)
        json.dump(x.json(), sys.stdout, indent=2)
        mess = x.json().get(u'message')
        self.assertFalse(x.json()[u'are_same_tree'], mess)

    # Insert here: edge case tests
    # Insert here: inputs out of range, leading to error or long delay
    # Insert here: error-generating conditions
    # (See ../README.md)

    def test_example_35(self):
        """Example service call from the documentation."""

        x = self.start_request_tests(example_35)
        # Insert: whether result is what it should be according to docs
        self.assert_success(x)
        # json.dump(x.json(), sys.stdout, indent=2)
        self.assertTrue(x.json()[u'are_same_tree'])

null=None; false=False; true=True

tree1 = u'(((((((EU368025_Uncult_marine_euk_FS14JA72_30Mar05_5m:0.00329,EU368020_Uncult_marine_euk_FS04GA95_01Aug05_5m:-0.00002):0.00002,EU368013_Uncult_marine_euk_FS01D014_01Aug05_65m:-0.00002):0.00010,(EU368034_Uncult_marine_euk_OC413NSS_Q007_15m:-0.00000,(EU368007_Uncult_marine_euk_FS01B026_30Mar05_5m:-0.00001,EU368004_Uncult_marine_euk_FS01AA94_01Aug05_5m:0.00328):0.00000):0.00317):0.00725,(EU368005_Uncult_marine_euk_FS01B033_30Mar05_5m:-0.00002,(EF172850_Uncult_euk_SSRPB47:-0.00003,EU368022_Uncult_marine_euk_FS04H169_01Aug05_89m:0.00166):0.00002):0.00597):0.00202,((DQ060523_Uncult_marine_euk_NOR46.29:0.01559,(HQ868826_Uncult_euk_SHAX1073:0.00155,EU368038_Uncult_marine_euk_EN351CTD040_4mN11:0.00172):0.00429):0.00017,(EU368023_Uncult_marine_euk_FS04H153_01Aug05_89m:0.00504,(DQ222879_Uncult_photo_euk_RA000907.18:0.00166,HM858468_Uncult_marine_euk_MO.011.5m.00036:-0.00003):0.00152):0.00566):0.00662):0.00941,(HQ868882_Uncult_euk_SHAX1135:0.00170,HQ868810_Uncult_euk_SHAX1056:-0.00007):0.02449):0.00648,(EU368021_Uncult_marine_euk_FS04GA46_01Aug05_5m:0.02285,(HQ869075_Uncult_euk_SHAX587:0.00000,HQ869035_Uncult_euk_SHAX540:0.00000):0.04720):0.01029,HQ156863_Uncult_marine_ciliate_170609_08:0.17059);'

tree2 = u'((HQ869075_Uncult_euk_SHAX587:0.00000,HQ869035_Uncult_euk_SHAX540:0.00000):0.04484,(EU368021_Uncult_marine_euk_FS04GA46_01Aug05_5m:0.02285,(((((EU368005_Uncult_marine_euk_FS01B033_30Mar05_5m:-0.00002,(EF172850_Uncult_euk_SSRPB47:-0.00003,EU368022_Uncult_marine_euk_FS04H169_01Aug05_89m:0.00166):0.00002):0.00597,(((EU368025_Uncult_marine_euk_FS14JA72_30Mar05_5m:0.00329,EU368020_Uncult_marine_euk_FS04GA95_01Aug05_5m:-0.00002):0.00002,EU368013_Uncult_marine_euk_FS01D014_01Aug05_65m:-0.00002):0.00010,(EU368034_Uncult_marine_euk_OC413NSS_Q007_15m:-0.00000,(EU368007_Uncult_marine_euk_FS01B026_30Mar05_5m:-0.00001,EU368004_Uncult_marine_euk_FS01AA94_01Aug05_5m:0.00328):0.00000):0.00317):0.00725):0.00202,((DQ060523_Uncult_marine_euk_NOR46.29:0.01559,(HQ868826_Uncult_euk_SHAX1073:0.00155,EU368038_Uncult_marine_euk_EN351CTD040_4mN11:0.00172):0.00429):0.00017,(EU368023_Uncult_marine_euk_FS04H153_01Aug05_89m:0.00504,(DQ222879_Uncult_photo_euk_RA000907.18:0.00166,HM858468_Uncult_marine_euk_MO.011.5m.00036:-0.00003):0.00152):0.00566):0.00662):0.00941,(HQ868882_Uncult_euk_SHAX1135:0.00170,HQ868810_Uncult_euk_SHAX1056:-0.00007):0.02449):0.00648,HQ156863_Uncult_marine_ciliate_170609_08:0.17059):0.01029):0.00236);'

example_35 = service.get_request('POST', {u'tree1_nwk': tree1, u'tree2_nwk': tree2})

if __name__ == '__main__':
    webapp.main()
