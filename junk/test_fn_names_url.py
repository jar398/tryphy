"""
Service Name: Find Scientific Names on web pages
Service Description: A service to find scientific names on web pages, PDFs, 
 Microsoft Office documents, images.
Resource URI: http://phylo.cs.nmsu.edu:5004/phylotastic_ws/fn/names_url
HTTP Method: GET
Input Format: application/x-www-form-urlencoded
Output Format: application/json

Parameters:

    Name: url
    Category: mandatory
    Data Type: string
    Description: an encoded URL for a web page, PDF, Microsoft Office 
      document, or image file 
    Name: engine
    Category: optional
    Data Type: integer

    Description: a integer value to specify which search engine (TaxonFinder or
    NetiNeti) to use. By default it is 0 which means it will use both
    engines. Value 1 means TaxonFinder and 2 means NetiNeti

Examples:

curl -D - "http://phylo.cs.nmsu.edu:5004/phylotastic_ws/fn/names_url?url=http://en.wikipedia.org/wiki/Ant"

curl -D - "http://phylo.cs.nmsu.edu:5004/phylotastic_ws/fn/names_url?url=https://en.wikipedia.org/wiki/Plain_pigeon&engine=1"

curl -D - "http://phylo.cs.nmsu.edu:5004/phylotastic_ws/fn/names_url?url=http://www.fws.gov/westvirginiafieldoffice/PDF/beechridgehcp/Appendix_D_Table_D-1.pdf"

Citation: http://gnrd.globalnames.org/

Service Quality:

    Restrictions on capacity:
    Restrictions on scope:
    Expected response time: 5s~12s
    Informative message:
        when service is down --
        when malformed input is provided --
    Uptime:
"""

import unittest, webapp, json, sys

url = 'http://phylo.cs.nmsu.edu:5004/phylotastic_ws/fn/names_url'
service = webapp.Service(url)

class TestFnNamesUrl(webapp.TestCase):

    def test_1(self):
        r = service.get()
        self.assert_response_status(r, 400)

if __name__ == '__main__':
    unittest.main()
