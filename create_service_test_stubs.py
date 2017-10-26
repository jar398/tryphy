
import webapp, os

webapp.read_requests('work/requests.json')

template1 = """# STUB

import sys, unittest, json
sys.path.append("../")
import webapp

url = '%s'
service = webapp.get_service(url)

class %s(webapp.WebappTestCase):
    @classmethod
    def get_service(self):
        return service
"""

template2 = """
if __name__ == '__main__':
    webapp.read_requests('work/requests.json')
    webapp.read_exchanges('work/exchanges.json')
    unittest.main()
"""

# TBD: should be configurable whether we do strict regression tests or not
# or whether strict regression tests cause test failure, or just warnings

template3="""
    def test_%s(self):
        x = self.start_request_tests(%s)
        # Insert here: additional checks on x.response
"""

# Generate the python file based on the templates.

for service in sorted(webapp.services_registry.values(), key=(lambda s: s.url)):
    service_url = service.url
    path = service_url.split('/phylotastic_ws/')[1]
    outpath = 'test_' + path.replace('/', '_')
    class_name = ''.join(map(lambda s:s.capitalize(), outpath.split('_')))
    outpathy = 'templates/' + outpath + '.py'
    requests = service.requests.values()
    with open(outpathy, 'w') as outfile:
        print 'Writing', outpathy
        outfile.write(template1 % (service_url, class_name))
        # One method definition for each request (parameter set)
        for request in requests:
            outfile.write(template3 %
                          (request.label, request.label))
        # Define each request (from examples in documentation)
        outfile.write('\nnull=None; false=False; true=True\n\n')
        for request in requests:
            outfile.write("%s = service.get_request('%s', %s)\n" %
                          (request.label, request.method, request.parameters))
        outfile.write(template2)
