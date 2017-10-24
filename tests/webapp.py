# This utility is specific to the phylotastic web API, not a
# completely general tool.

import sys, requests, time, unittest, json

# The content-type that we anticipate getting from the web services
# when the content is json.
# At one point this was text/html, but it has since been changed to
# application/json.
anticipated_content_type = 'application/json'

# Ensure unique instantiation of each service object

services_registry = {}    # url -> Service
requests_registry = {}    # label -> Request

def get_service(url):
    if url in services_registry:
        return services_registry[url]
    service = Service(url)
    services_registry[url] = service
    return service

def get_request(label):
    r = services_registry.get(label)
    if r == None:
        print >>sys.stderr, '** No such request: ', label
    return r

class Service():
    def __init__(self, url):
        self.url = url
        self.requests = {}  # maps (method, parameters) to Request

    def get_request(self, method='GET', parameters={},
                    label=None, source=None):
        key = (method, json.dumps(parameters, sort_keys=True))
        r = self.requests.get(key)
        if r == None:
            r = Request(self, method, parameters, label, source)
            self.requests[key] = r
            requests_registry[label] = r
        elif label != None:
            r.label = label
        return r

    # exchange blob
    def get_request_from_blob(self, blob):
        return self.get_request(blob[u'method'],
                                (blob[u'parameters']
                                 if u'parameters' in blob
                                 else blob[u'data']),
                                label=blob[u'label'],
                                source=blob[u'source'])

    def name(self):
        return self.url.split('phylotastic_ws/')[-1]

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
    def __init__(self, service, method, parameters, label, source, expect_status=None):
        self.service = service
        self.method = method
        self.parameters = parameters
        self.label = label
        self.source = source
        self.expect_status = expect_status
        self.exchanges = []   # ?
        
    # Perform a single exchange for this request (method, url, query)
    def exchange(self):
        time1 = time.time()      # in seconds, floating point
        if self.method == 'GET':
            # should we set an accept: header here?
            # in theory, yes.
            # but no, because the documentation never sets one.
            resp = requests.get(self.service.url, params=self.parameters)
        elif self.method == 'POST':
            resp = requests.post(self.service.url,
                                 headers={'Content-type': 'application/json',
                                          'Accept': 'application/json,*/*;q=0.1'},
                                 data=json.dumps(self.parameters))
        else:
            print >>sys.stderr, '** unrecognized method:', self.method
        time2 = time.time()
        x = Exchange(self, response=resp, time=(time2 - time1))
        self.exchanges.append(x) # for timing analysis
        return x

    def stringify(self):
        return('%s %s?%s' %
               (self.method,
                self.service.url,
                json.dumps(self.parameters)[0:60]))

    def to_dict(self):
        return {'label': self.label,
                'source': self.source,
                'service': self.service.url,
                'method': self.method,
                'parameters': self.parameters,
                'expect_status': self.expect_status}

def to_request(blob):
    if isinstance(blob, unicode):
        # blob is a label and is globally unique
        return get_request(blob)
    else:
        service = get_service(blob[u'service'])
        return Request(service,
                       blob[u'method'],
                       blob[u'parameters'],
                       blob[u'label'],
                       blob[u'source'],
                       blob.get(u'expect_status'))

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
            self.status_code = response.status_code
            self.text = response.text
            self.the_json = None
            ct = response.headers['content-type'].split(';')[0]
            self.content_type = ct
            if ct == 'application/json':
                self.the_json = response.json()
                # I expected the status code to be 4xx.
                # Instead, there's a 200 response, with a status_code
                # key in the JSON dict whose value is 400.
                if self.status_code == 200 and u'status_code' in self.the_json:
                    self.status_code = self.the_json[u'status_code']

        else:
            self.content_type = content_type
            self.status_code = status_code
            self.text = text
            self.the_json = json

    def json(self):
        return self.the_json

    def to_dict(self):
        if False:
            return {'request': self.request.to_dict(),
                    'time': self.time,
                    'status_code': self.status_code,
                    'content_type': self.content_type,
                    'response': self.json()}
        else:
            return {'request': self.request.label,
                    'time': self.time,
                    'status_code': self.status_code,
                    'content_type': self.content_type,
                    'response': self.json()}

def to_exchange(blob):
    rd = blob.get(u'request')
    if rd == None:
        # backward compatibility.  delete this code in a bit.
        service = get_service(blob[u'url'])
        request = service.get_request(method=blob[u'method'],
                                      parameters=blob[u'data'],
                                      source=blob.get(u'source'))
    else:
        request = to_request(rd)
        if request == None:
            return None
    return Exchange(request,
                    content_type=blob[u'content_type'],
                    status_code=blob[u'status_code'],
                    json=blob[u'response'])


# Subclass of unittest.TestCase with some additional methods that are
# useful for testing web services.

# There should be one of these for each service.

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
        if x.status_code < 300:
            self.assertEqual(x.content_type, u'application/json')

        self.assertEqual(x.status_code, code)

    # ? method for doing regression tests ?
    # ? instance variable 'service' is provided by the subclass ?

    def test_regression(self):
        service = self.get_service()
        print '\n# Regression testing:', service.url
        for request in service.requests.values():
            print '# checking adequacy', request.stringify()
            exchanges = [exchange for exchange in request.exchanges]
            for exchange in exchanges:
                print '# checking exchange adequacy'
                present = request.exchange()
                self.check_adequacy(present, exchange)
            return True

    # Is the 'now' result no worse than the 'then' result?
    def check_adequacy(self, now, then):
        self.assertEqual(now.status_code, then.status_code)
        self.check_result(now.json(), then.json())

    def check_result(self, now, then):
        if isinstance(then, dict):
            self.assertTrue(isinstance(now, dict))
            for key in then:
                self.assertTrue(key in now)
                if key == u'creation_time': continue
                if key == u'execution_time': continue
                self.check_result(now[key], then[key])
        elif isinstance(tuple, list):
            self.assertEqual(len(now), len(list))
            for (n, t) in zip(now, list):
                self.check_result(n, t)
        else:
            self.assertFalse(isinstance(now, dict))
            self.assertEqual(now, then)



    @classmethod
    def tearDownClass(self):
        maxtime = 0
        for r in self.get_service().requests.values():
            for x in r.exchanges:
                if x.time > maxtime:
                    maxtime = x.time
        print >>sys.stderr, '\nSlowest call:', maxtime


# Write list of requests (read from documentation) to a file

def write_requests(requests):
    json.dump({'requests': [r.to_dict() for r in requests]},
              sys.stdout, indent=2, sort_keys=True)

# Read them back in

def read_requests(inpath):
    with open(inpath, 'r') as infile:
        j = json.load(infile)
        return [to_request(blob) for blob in j[u'requests']]

# Having read (or parsed) some examples, execute them

def run_examples(requests):
    exchanges = []
    i = 0
    for request in requests:
        if i % 17 == 3:
            print >>sys.stderr, request.stringify()
            exchange = request.exchange()
            if request.expect_status != None:
                if exchange.status_code != request.expect_status:
                    print >>sys.stderr, ('** Status code %s not what was expected (%s)' %
                                         (exchange.status_code, request.expect_status))
                    print >>sys.stderr, '   for', request.stringify()
            exchanges.append(exchange)
            time.sleep(1)
        i += 1
    print >>sys.stderr, i
    return exchanges

# Load exchanges that were previously executed and dumped to a file
# N.b. creating Exchange also stashes the request,
# for regression testing or whatever

def read_exchanges(inpath):
    exchanges = []
    with open(inpath, 'r') as infile:
        j = json.load(infile)
        print 'reading exchanges from', inpath
        for blob in j[u'exchanges']:
            x = to_exchange(blob)
            if x != None:
                print 'exchange:', x.request.label, x.status_code
                exchanges.append(x)
    return exchanges

# Write exchanges to file (or stdout)

def write_exchanges(exchanges, outfile):
    json.dump({'exchanges': [x.to_dict() for x in exchanges]},
              outfile, indent=2, sort_keys=True)

if __name__ == '__main__':
    inpath = sys.argv[1]  #'work/requests.json'
    outpath = sys.argv[2] #'work/exchanges.json'
    the_requests = read_requests(inpath)
    # Get a baseline for future regression tests
    the_exchanges = run_examples(the_requests)
    with open(outpath, 'w') as outfile:
        write_exchanges(the_exchanges, outfile)
