
import sys, json, webapp

def report():
    for service in webapp.services_registry.values():
        nonjar = 0
        jar = 0
        for request in service.requests.values():
            if request.source.startswith('Phylo'):
                nonjar += 1
            else:
                jar += 1
        print >>sys.stderr, service.name(), nonjar, jar

def regression(xpath):
    i = 0
    with open(xpath, 'r') as infile:
        j = json.load(infile)
        for x in j[u'exchanges']:
            webapp.to_exchange(x)
            i += 1
    print >>sys.stderr, '%s exchanges' % i
    for service in webapp.services_registry.values():
        webapp.WebappTestCase(service).test_regression()

if __name__ == '__main__':
    webapp.read_requests('work/requests.json')
    #report()
    regression('work/exchanges.json')
