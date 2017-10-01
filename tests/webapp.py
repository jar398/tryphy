# This utility is specific to the phylotastic web API, not a
# completely general tool.


import sys, requests, time, unittest, json

# Changed this to application/json now that the service is fixed
# expected_content_type = 'text/html'
expected_content_type = 'application/json'

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

    def get(self, params=None):
        time1 = time.clock()      # in seconds, floating point
        response = requests.get(self.url, params=params)
        time2 = time.clock()
        return Exchange(response, time2 - time1)

    def post(self, data=None):
        time1 = time.clock()      # in seconds, floating point
        response = requests.post(self.url, data=data)
        time2 = time.clock()
        return Exchange(response, time2 - time1)

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
        
    def exchange(self):
        time1 = time.clock()      # in seconds, floating point
        if self.method == 'GET':
            response = requests.get(self.service.url, params=self.data)
        else:                   # 'POST'
            response = requests.post(self.service.url,
                                     headers={'Content-type': 'application/json'},
                                     data=self.data)
        time2 = time.clock()
        return Exchange(response, time2 - time1)


# An Exchange is an activation of a Request yielding either an error
# or a response (in the 'requests' library sense) and taking up time.

class Exchange():
    def __init__(self, response, time):
        self.response = response
        self.time = time
        self.the_json = False
        self.headers = self.response.headers
        self.status_code = self.response.status_code
        self.text = self.response.text

    def json(self):
        if self.the_json == False:
            ct = self.response.headers['content-type']
            if ct == 'application/json':
                self.the_json = self.response.json()
            else:
                print >>sys.stderr, '** Content of response is not json:', ct
                print >>sys.stderr, self.response.text
                self.the_json = None
        return self.the_json

class TestCase(unittest.TestCase):
    # Ensure that the JSON has the form of a successful response

    def assert_success(self, r):
        self.assert_response_status(r, 200)
        j = r.json()
        self.assertTrue(u'message' in j)
        self.assertEqual(j[u'message'], u'Success')
        self.assertTrue(u'execution_time' in j)
        self.assertTrue(u'creation_time' in j)

    # Somehow check:
    # Informative message:
    #   when service is down --
    #   when malformed input is provided --

    # Expected response time: 3s~10s

    def assert_response_status(self, r, code):
        # I expected the status code to be 4xx.
        # Instead, you get a 200 response, and there is a status_code
        # key in the JSON dict whose value is 400.
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.headers[u'content-type'].split(';')[0],
                         expected_content_type)
        j = r.json()
        self.assertTrue(u'status_code' in j)    # what Open Tree returns?
        self.assertEqual(j[u'status_code'], code)    # what Open Tree returns?

def read_exchanges(inpath):
    with open(inpath, 'r') as infile:
        j = json.load(infile)
        for x in j[u'exchanges']:
            service = get_service(x[u'url'])
            request = service.get_request(x[u'method'], x[u'data'])
