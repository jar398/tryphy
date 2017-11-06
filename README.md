# Phylotastic web service tests

## TL;DR How to Run

To run all tests:

    make

To run tests for an individual web service:

    export PYTHONPATH=.
    python tests/test_tnrs_ot_resolve.py

substituting in the desired service name (slash becomes underscore).

## Background documents

* [Phylotastic web API documentation](https://github.com/phylotastic/phylo_services_docs/blob/master/ServiceDescription/PhyloServicesDescription.md)
* [Choice of Python test framework](doc/test-framework-choice.md)

## How it works

There is a `tests/` directory containing one `test_...py` python file
for each service.  There is one test for each example in the
documentation, plus others for edge cases, range limits, capacity
tests, and error conditions.  For the examples, there is a regression
test, comparing the latest result from a previously saved result.
When a result is checked for correctness, the test is usually partial,
just looking at particular aspects of the result, not checking every
part of it.

Sitting beneath this is a bit of infrastructure with classes for
services, requests (i.e. service + parameters), and exchanges (request
plus response).  There are a few additional scripts to scrape the
examples, obtain the baseline responses for regression testing, and
create stub test_ files for the services.

## Example

    bash-3.2$ PYTHONPATH=. python tests/test_tnrs_ot_resolve.py 
    Read 48 requests from work/requests.json
    Read 48 exchanges from work/exchanges.json
    ....FTesting big request 1
    Testing big request 2
    Testing big request 4
    Testing big request 8
    Testing big request 16
    Testing big request 32
    Testing big request 64
    Testing big request 128
    Testing big request 256
    Big request status 500 at 256 names
    {"message": "Error: 'results'"}
    ...
    Slowest exchange for http://phylo.cs.nmsu.edu:5004/phylotastic_ws/tnrs/ot/resolve: 0.610131978989

    ======================================================================
    FAIL: test_5 (__main__.TestTnrsOtResolve)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "tests/test_tnrs_ot_resolve.py", line 141, in test_5
        self.try_names(names)
      File "tests/test_tnrs_ot_resolve.py", line 115, in try_names
        matched_names = self.all_matched_names(x)
      File "tests/test_tnrs_ot_resolve.py", line 131, in all_matched_names
        self.assertTrue(u'matched_name' in m)
    AssertionError: False is not true

    ----------------------------------------------------------------------
    Ran 8 tests in 6.238s

    FAILED (failures=1)
    bash-3.2$ 

## How to run the tests

To run all tests:

    python -m unittest discover -s tests

or equivalently (assuming bash)

    for f in tests/test*.py; do python $f; done

To run tests for just a single service (for example, the `gt/ot/tree` service):

    python tests/test_gt_ot_tree.py

or equivalently

    PYTHONPATH=tests python -m unittest test_gt_ot_tree.TestGtOtTree

(that's bash syntax: `VAR=value command` means run `command` with environment variable `VAR` set to `value`)

To run a single test:

    PYTHONPATH=tests python -m unittest test_gt_ot_tree.TestGtOtTree.test_some_bad

Note that tests are not necessarily run in order, i.e. sometimes a
test occurring earlier in the python file will be run after one that
occurs later.

## Running the list service tests

To run the list services tests, you will need a configuration file
(`config.json`) and a current access token.
A google (gmail) account is required to get a token.
If you do not get a token, the tests will be skipped.

Set up the test system configuration as follows:

* `cp config-template.json config.json`
* `chmod go-rwx config.json`
* Edit `config.json` so that your google account's email address is in the 
  obvious place.

Documentation on obtaining an access token is
[here](https://github.com/phylotastic/phylo_services_docs/blob/master/SpeciesListServer/AccessToken.md).

Once you have the token, install it in configuration file as follows:

    python tokenconfig.py "... the token ..."

This makes a note of the expiration time for the token, which is
checked each time the token is used.

## List of all services as of 17 September 2017

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

