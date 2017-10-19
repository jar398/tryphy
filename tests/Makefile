
all:
	for t in test_*.py; do python $t; done

# markdown is here:
DESCRIPTION="https://raw.githubusercontent.com/phylotastic/phylo_services_docs/master/ServiceDescription/PhyloServicesDescription.md"

in/PhyloServicesDescription.md:
	@mkdir -p in
	wget -O $@ $(DESCRIPTION)

work/requests.json: in/PhyloServicesDescription.md
	@mkdir -p work
	python doc_examples.py $< >$@.new
	mv $@.new $@
