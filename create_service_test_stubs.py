
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

    # Insert here: edge case tests
    # Insert here: inputs out of range, leading to error or long delay
    # Insert here: error-generating conditions
    # (See ../README.md)
"""

template2 = """
if __name__ == '__main__':
    webapp.read_requests('../work/requests.json')
    webapp.read_exchanges('../work/exchanges.json')
    unittest.main()
"""

# TBD: should be configurable whether we do strict regression tests or not
# or whether strict regression tests cause test failure, or just warnings

# As of start of project, the docs say nothing about the result, so
# technically there is nothing to check...

template3="""
    def test_%s(self):
        x = self.start_request_tests(%s)
        # Insert: whether result is what it should be according to docs
"""

# Generate the python file based on the templates.

if not os.path.isdir('templates'):
    os.mkdir('templates')

for service in sorted(webapp.services_registry.values(), key=(lambda s: s.url)):
    service_url = service.url
    path = service_url.split('/phylotastic_ws/')[1]
    outpath = 'test_' + path.replace('/', '_')
    class_name = ''.join(map(lambda s:s.capitalize(), outpath.split('_')))
    outpathy = os.path.join('templates', outpath + '.py')
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
