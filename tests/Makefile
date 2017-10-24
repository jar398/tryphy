
all:
	for t in test_*.py; do python $t; done

# markdown is here:
DESCRIPTION="https://raw.githubusercontent.com/phylotastic/phylo_services_docs/master/ServiceDescription/PhyloServicesDescription.md"

in/PhyloServicesDescription.md:
	@mkdir -p in
	wget -O $@ $(DESCRIPTION)

work/requests.json: in/PhyloServicesDescription.md doc_examples.py webapp.py
	@mkdir -p work
	python doc_examples.py in/PhyloServicesDescription.md >$@.new
	mv $@.new $@

# Run all the examples and store outcome
work/exchanges.json: work/requests.json webapp.py
	python webapp.py work/requests.json $@.new
	mv $@.new $@
