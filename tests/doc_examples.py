# Utilities for reading and writing the examples that are in the
# documentation.

import sys, requests, subprocess, json, time, re, webapp

# 1. Parse examples (requests) from documentation

def parse_requests(inpath):
    requests = []
    i = 1
    source = inpath.split('/')[-1]
    with open(inpath, 'r') as infile:
        for line in infile:
            line = line.strip()
            z = None
            if line.startswith('curl'):
                z = parse_post_example(line, 'example_' + str(i), source)
            elif line.startswith('http'):
                z = parse_get_example(line, 'example_' + str(i), source)
            if z != None:
                requests.append(z)
                i += 1
    print >>sys.stderr, '%s services' % len(webapp.services_registry)
    print >>sys.stderr, '%s examples' % i
    return requests

# Assumption: \ is not used in any of the examples

# We have curl -X POST both with and without double quotes; that
# is a source of complexity here.

post_example_pattern = \
  re.compile('curl -X POST "?(https?://[^ "]*).* -d \'([^\']*)\'')

def parse_get_example(line, label, source):
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
    return service.get_request('GET', params, examplep=True, label=label,
                               source=source)

def parse_post_example(line, label, source):
    m = post_example_pattern.match(line)
    if m == None:
        print >>sys.stderr, "** Doc file not understood: don't know how to process this line", line
        return None
    service = webapp.get_service(m.group(1))
    params = json.loads(m.group(2))
    return service.get_request('POST', params, examplep=True, label=label,
                               source=source)

# Parse the example web service calls from the documentation file (stdin),
# run them for regression testing, and write all exchanges(request + response)
# to standard output.

if __name__ == '__main__':
    inpath = sys.argv[1]
    requests = parse_requests(inpath)
    if False:
        exchanges = run_examples(requests)
        webapp.write_exchanges(exchanges, sys.stdout)
    else:
        webapp.write_requests(requests)
