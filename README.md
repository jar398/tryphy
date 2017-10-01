# Phylotastic web service tests

[Phylotastic web API documentation](https://github.com/phylotastic/phylo_services_docs/blob/master/ServiceDescription/PhyloServicesDescription.md)

[Choice of Python test framework](doc/test-framework-choice.md)

## What these tests are supposed to do

Tests will probe (1) whether the API is correctly described in the
docs, (2) what happens with edge cases, input range limits, and
error-generating conditions such as syntax errors that may be expected
to arise deliberately or accidentally in normal use. Examples of edge
cases would be things like querying for a tree with a list of extinct
species, or querying with a taxon name that has unusual characters or
extra complexity. Testing for range limits is typically going to
involve finding (within a factor of 2) the minimum query complexity
(e.g., number of taxa) that results in an error or an unacceptable
delay (> 15 sec with no feedback or warning of delays).


## List of all services as of 17 Deptember 2017

| URL                   |Description
| ----------------------|--------
| fn/names_url          | Find Scientific Names on web pages
| fn/names_text         | Find Scientific Names on free-form text
| tnrs/ot/resolve       | Resolve Scientific Names with Open Tree TNRS
| tnrs/ot/names
| tnrs/gnr/resolve      | Resolve Scientific Names with GNR TNRS
| tnrs/gnr/names
| gt/ot/get_tree        | Get Phylogenetic Trees from Open Tree of Life
| gt/ot/tree
| ts/all_species        | Get all Species from a Taxon
| ts/country_species    | Get all Species from a Taxon filtered by country
| si/eol/get_images     | Get image urls of a list of species
| si/eol/images         | 
| ts/ncbi/genome_species| Get Species (of a Taxon) that have genome sequence in NCBI
| sl/eol/get_links      | Get information urls of a list of species
| sl/eol/links          
| sls/get_list          | Get lists of species
| sls/insert_list       | Post a new list of species
| sls/replace_species   | Replace species of an existing list
| sls/remove_list       | Remove an existing list
| sls/update_list       | Update metadata of an existing list
| compare_trees         | Compare Phylogenetic Trees
| md/get_studies        | Find supported studies of an induced tree
| md/studies
| gt/pm/get_tree        | Get Phylogenetic Trees from phylomatic
| gt/pm/tree
| gt/pt/get_tree        | Get Phylogenetic Trees from phyloT
| gt/pt/tree
| sc/scale              | Get Phylogenetic Trees with branch lengths
| sc/metadata_scale     | Get metadata for a output chronogram

The port is variously 5004, 5005, 5006, 5009
