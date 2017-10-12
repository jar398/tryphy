# Parse the example web service calls from the documentation file (stdin),
# run them for regression testing, and write all requests and responses
# to standard output


import sys, requests, subprocess, json, time, re, webapp

# Assumption: \ is not used in any of the examples

# We have curl -X POST both with and without double quotes.

doit = False

service_pattern = re.compile('curl -X POST "?(https?://[^ "]*).* -d \'([^\']*)\'')

def parse_get_example(line):
    parts = line.split('?', 1)
    if len(parts) > 2:
        print >>sys.stderr, '** Doc file not understood: too many parts', line
        return None
    service = webapp.get_service(parts[0])
    if len(parts) > 1:
        query = parts[1].replace('%20', ' ')
        data = {param[0] : param[1] for param in [x.split('=') for x in query.split('&')]}
    else:
        data = None
    return service.get_request('GET', data)

def parse_post_example(line):
    m = service_pattern.match(line)
    if m == None:
        print >>sys.stderr, "** Doc file not understood: don't know how to process this line", line
        return None
    service = webapp.get_service(m.group(1))
    data = m.group(2)
    return service.get_request('POST', data)

def parse_examples(inpath):
    examples = []
    with open(inpath, 'r') as infile:
        for line in infile:
            line = line.strip()
            z = None
            if line.startswith('curl'):
                z = parse_post_example(line)
            elif line.startswith('http'):
                z = parse_get_example(line)
            if z != None:
                examples.append(z)
    return examples

def run_examples(inpath):
    examples = parse_examples(inpath)
    exchanges = []
    i = 0
    for request in examples:
        if True:
            print >>sys.stderr, request.method, request.service.url, request.data
            exchange = request.exchange()
            exchanges.append({'url': request.service.url,
                              'method': request.method,
                              'data': request.data,
                              'time': exchange.time,
                              'status_code': exchange.status_code,
                              'content_type': exchange.headers['content-type'],
                              'response': exchange.json()})
            time.sleep(1)
        i += 1
    print >>sys.stderr, i
    json.dump({'exchanges': exchanges}, sys.stdout, indent=2)

run_examples(sys.argv[1])
