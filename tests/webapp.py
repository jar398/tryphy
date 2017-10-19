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
        self.requests = {}  # maps (method, parameters) to Request
        self.requests_by_label = {}
        self.examplep = False

    def get_request(self, method='GET', parameters={}, examplep=False, label=None):
        key = (method, json.dumps(parameters, sort_keys=True))
        r = self.requests.get(key)
        if r == None:
            r = Request(self, method, parameters, label)
            self.requests[key] = r
            self.requests_by_label[label] = r
        elif label != None:
            r.label = label
        r.examplep = examplep
        return r

    def get_request_from_blob(self, blob):
        return self.get_request(blob[u'method'],
                                blob[u'parameters'],
                                blob[u'label'])

    def get_examples(self):
        return [r for r in self.requests if r.examplep]

    def get_times():
        times = []
        for r in requests:
            for x in request.exchanges:
                times.append(x.time)
        return times

# Every Service has a set of requests that can be (or have been) made.
# Typically a Request is a test or example.

class Request():
    def __init__(self, service, method, parameters, label):
        self.service = service
        self.method = method
        self.parameters = parameters
        self.label = label
        self.exchanges = []   # ?
        
    # Perform a single exchange for this request (method, url, query)
    def exchange(self):
        time1 = time.clock()      # in seconds, floating point
        if self.method == 'GET':
            # should we set an accept: header here?
            # in theory, yes.
            # but no, because the documentation never sets one.
            resp = requests.get(self.service.url, params=self.parameters)
        elif self.method == 'POST':
            resp = requests.post(self.service.url,
                                 headers={'Content-type': 'application/json'},
                                 data=self.parameters)
        else:
            print >>sys.stderr, '** unrecognized method:', self.method
        time2 = time.clock()
        x = Exchange(self, response=resp, time=(time2 - time1))
        self.exchanges.append(x) # for timing analysis
        return x

    def to_dict(self):
        return {'label': self.label,
                'service': self.service.url,
                'method': self.method,
                'parameters': self.parameters}

def to_request(blob):
    service = get_service(blob[u'service'])
    return service.get_request_from_blob(blob)

# An Exchange is an activation of a Request yielding either an error
# or a response (in the 'requests' library sense) and taking up time.

class Exchange():
    def __init__(self, request, time=None, response=None,
                 content_type='application/json',     # type *requested*
                 status_code=200, text=None, json=None):
        self.request = request
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

    def to_dict(self):
        return {'request': self.request.to_dict(),
                'time': self.time,
                'status_code': self.status_code,
                'content_type': self.content_type,
                'response': self.json()}

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
            service = get_service(blob[u'service'])
            request = service.get_request(method=blob[u'method'],
                                          parameters=blob[u'parameters'],
                                          label=blob[u'label'])
