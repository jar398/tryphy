# This utility is specific to the phylotastic web API, not a
# completely general tool.

import sys, requests, time, unittest, json

# The content-type that we anticipate getting from the web services
# when the content is json.
# At one point this was text/html, but it has since been changed to
# application/json.
anticipated_content_type = 'application/json'

# Ensure unique instantiation of each service object

services_registry = {}

def get_service(url):
    if url in services_registry:
        return services_registry[url]
    service = Service(url)
    services_registry[url] = service
    return service

class Service():
    def __init__(self, url):
        self.url = url
        self.requests = {}  # maps (method, data) to Request

    def get_request(self, method, data):
        key = (method, json.dumps(data))
        r = self.requests.get(key)
        if r != None:
            return r
        else:
            r = Request(self, method, data)
            self.requests[key] = r
            return r

# Every Service has a set of requests that can be (or have been) made.
# Typically these are tests or examples.

class Request():
    def __init__(self, service, method, data):
        self.service = service
        self.method = method
        self.data = data
        self.exchanges = []   # ?
        
    # Perform a single exchange for this request (method, url, query)
    def exchange(self):
        time1 = time.clock()      # in seconds, floating point
        if self.method == 'GET':
            resp = requests.get(self.service.url, params=self.data)
        else:                   # 'POST'
            resp = requests.post(self.service.url,
                                     headers={'Content-type': 'application/json'},
                                     data=self.data)
        time2 = time.clock()
        return Exchange(response=resp, time=(time2 - time1))


# An Exchange is an activation of a Request yielding either an error
# or a response (in the 'requests' library sense) and taking up time.

class Exchange():
    def __init__(self, time=None, response=None,
                 content_type='application/json',     # type *requested*
                 status_code=200, headers={}, text=None, json=None):
        self.time = time
        self.the_json = False
        if response != None:
            self.content_type = response.headers['content-type']
            self.status_code = response.status_code
            self.text = response.text
            if self.content_type == anticipated_content_type:
                self.the_json = response.json()
            else:
                print >>sys.stderr, '** Content of response is not json:', ct
                print >>sys.stderr, response.text
                self.the_json = None
        else:
            self.content_type = content_type
            self.status_code = status_code
            self.text = text
            self.the_json = json

    def json(self):
        return self.the_json

# Subclass of unittest.TestCase with some additional methods that are
# useful for testing web services.

class WebappTestCase(unittest.TestCase):
    # Ensure that the JSON has the form of a successful response.

    # x is an Exchange
    def assert_success(self, x):
        self.assert_response_status(x, 200)
        j = x.json()
        self.assertTrue(u'message' in j)
        self.assertEqual(j[u'message'], u'Success')
        self.assertTrue(u'execution_time' in j)
        self.assertTrue(u'creation_time' in j)

    # Somehow check:
    #  Informative message:
    #   when service is down --
    #   when malformed input is provided --
    #  Expected response time: 3s~10s

    def assert_response_status(self, x, code):
        # I expected the status code to be 4xx.
        # Instead, you get a 200 response, and there is a status_code
        # key in the JSON dict whose value is 400.
        self.assertEqual(x.status_code, 200)
        self.assertEqual(x.content_type.split(';')[0],
                         anticipated_content_type)
        j = x.json()
        self.assertTrue(u'status_code' in j)    # what Open Tree returns?
        self.assertEqual(j[u'status_code'], code)    # what Open Tree returns?

# Read a set of exchanges that were originally written after
# performing them (see run_examples.py).

def read_exchanges(inpath):
    with open(inpath, 'r') as infile:
        j = json.load(infile)
        for blob in j[u'exchanges']:
            service = get_service(blob[u'url'])
            request = service.get_request(blob[u'method'], blob[u'data'])
