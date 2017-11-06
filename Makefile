
all:
	for t in `ls tests/test_*.py`; do PYTHONPATH=tests python $$t; done

# "Old" documentation markdown is here:
DESCRIPTION_URL="https://raw.githubusercontent.com/phylotastic/phylo_services_docs/master/ServiceDescription/PhyloServicesDescription.md"

in/PhyloServicesDescription.md:
	@mkdir -p in
	wget -O $@ $(DESCRIPTION_URL)

work/requests.json: in/PhyloServicesDescription.md doc_examples.py webapp.py
	@mkdir -p work
	python doc_examples.py in/PhyloServicesDescription.md >$@.new
	mv $@.new $@

baseline: work/exchanges.json

# Run all the examples and store outcomes, for regression testing
work/exchanges.json: work/requests.json webapp.py
	python webapp.py work/requests.json $@.new
	mv $@.new $@

tags:
	etags *.py tests/*.py
