
all: work/examples.txt

# markdown is here:
DESCRIPTION="https://raw.githubusercontent.com/phylotastic/phylo_services_docs/master/ServiceDescription/PhyloServicesDescription.md"

in/PhyloServicesDescription.md:
	@mkdir -p in
	wget -O $@ $(DESCRIPTION)

work/examples.txt: in/PhyloServicesDescription.md
	@mkdir -p work
	egrep "^http|^curl" $< >$@

