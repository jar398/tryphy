# Utilities for reading and writing the examples that are in the
# documentation.

import sys, requests, subprocess, json, time, re, webapp

# 1. Parse examples (requests) from documentation

def parse_requests(inpath):
    requests = []
    i = 1
    with open(inpath, 'r') as infile:
        for line in infile:
            line = line.strip()
            z = None
            if line.startswith('curl'):
                z = parse_post_example(line, 'example_' + str(i))
            elif line.startswith('http'):
                z = parse_get_example(line, 'example_' + str(i))
            if z != None:
                requests.append(z)
                i += 1
    return requests

# Assumption: \ is not used in any of the examples

# We have curl -X POST both with and without double quotes; that
# is a source of complexity here.

post_example_pattern = \
  re.compile('curl -X POST "?(https?://[^ "]*).* -d \'([^\']*)\'')

def parse_get_example(line, label):
    parts = line.split('?', 1)
    if len(parts) > 2:
        print >>sys.stderr, '** Doc file not understood: too many parts', line
        return None
    service = webapp.get_service(parts[0])
    if len(parts) > 1:
        query = parts[1].replace('%20', ' ')
        params = {param[0] : param[1] for param in [x.split('=') for x in query.split('&')]}
    else:
        params = None
    return service.get_request('GET', params, examplep=True, label=label)

def parse_post_example(line, label):
    m = post_example_pattern.match(line)
    if m == None:
        print >>sys.stderr, "** Doc file not understood: don't know how to process this line", line
        return None
    service = webapp.get_service(m.group(1))
    params = json.loads(m.group(2))
    return service.get_request('POST', params, examplep=True, label=label)

# 1a. Write list of requests (read from documentation) to a file

def write_requests(requests):
    json.dump({'requests': [r.to_dict() for r in requests]},
              sys.stdout, indent=2, sort_keys=True)

# Read them back in

def read_requests(inpath):
    with open(inpath, 'r') as infile:
        j = json.load(infile)
        return [webapp.to_request(blob) for blob in j[u'requests']]

# 2. Having read (or parsed) the examples, now execute them

def run_examples(requests):
    exchanges = []
    i = 0
    for request in requests:
        if True:
            print >>sys.stderr, request.method, request.service.url, \
                  request.parameterss
            exchange = request.exchange()
            exchanges.append(exchange.to_dict())
            time.sleep(1)
        i += 1
    print >>sys.stderr, i
    return exchanges

# 3. Load exchanges that were previously executed and dumped to a file

def read_exchanges(inpath):
    def get_exchange(blob):
        request = webapp.to_request(blob[u'request'])
        # creating Exchange also stashes the request,
        # for regression testing or whatever
        return Exchange(request,
                        content_type=blob[u'content_type'],
                        status_code=blob[u'status_code'],
                        # text=???,
                        json=blob.json)
    exchanges = []
    with open(inpath, 'r') as infile:
        j = json.load(infile)
        for blob in j[u'exchanges']:
            exchanges.append(get_exchange(blob))
    return exchanges

# Write exchanges to file (or stdout)

def write_exchanges(exchanges, outfile):
    json.dump({'exchanges': [x.to_dict() for x in exchanges]},
              sys.stdout, indent=2, sort_keys=True)

# Parse the example web service calls from the documentation file (stdin),
# run them for regression testing, and write all exchanges(request + response)
# to standard output.

if __name__ == '__main__':
    inpath = sys.argv[1]
    requests = parse_requests(inpath)
    if False:
        exchanges = run_examples(requests)
        write_exchanges(exchanges, sys.stdout)
    else:
        write_requests(requests)
