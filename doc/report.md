# Report on test system project

## Project description

"For each service, include tests of all examples in the documentation
(typically 1 to 3), along with 3 other tests. Any new methods or
functions in the test suite will be documented inline using an
existing standard. The test code will use an open-source license and
will be developed in a new or existing github repository associated
with the Phylotastic project."

"Tests will probe (1) whether the API is correctly described in the
docs, (2) what happens with edge cases, input range limits, and
error-generating conditions such as syntax errors that may be expected
to arise deliberately or accidentally in normal use. Examples of edge
cases would be things like querying for a tree with a list of extinct
species, or querying with a taxon name that has unusual characters or
extra complexity. Testing for range limits is typically going to
involve finding (within a factor of 2) the minimum query complexity
(e.g., number of taxa) that results in an error or an unacceptable
delay (> 15 sec with no feedback or warning of delays)."

The documentation was revised after the contract began.  For the most
part I referred to the old documentation (the documentation that was
available when work began), and only checked the new documentation
when necessary for clarification or for help in understanding
surprising behavior.

## Progress so far (2017-11-05)

You can run the tests as directed in [the README file](../README.md).  A number of
tests fail.  I believe that every failure reflects a bug in some
service.

The testing framework (`unittest`, see
[here](test-framework-choice.md) for rationale) is not designed to produce output
that explains failures.  You get a backtrace, giving the test function
name, source (python) file, and line number, and some kind of message,
which can be helpful in conjunction and the source file.  But to
really understand what happened, you usually have to read the source
file.

See [failures.md](failures.md) to see current output of test run.

The following sections attempt to compare what the test system does
now, against what was specified in the project description.

### All the examples in the documentation

Yes - the examples were extracted from the (old) documentation and
added to the test scripts automatically.  In some cases the result is
partially checked for correctness, but for many services there is only
a check for a 200 response.  Some examples required modification,
e.g. the `resolvedNames` parameter is now called `taxa`.

### Three additional tests

Yes, except for five of the services.  Most of the neglected services
are list services, which are more difficult to test since they involve
server state.

### Tests documented inline using an existing standard

When they are documented, which is often, functions including test
functions use the Python `"""..."""` documentation convention 
([PEP 257](https://www.python.org/dev/peps/pep-0257/)).

Work in progress: some functions don't have documentation strings.

### Use an open-source license?

BSD 2-clause.  It can easily be relicensed if necessary.

### Developed in a new or existing github repository associated with the Phylotastic project

No, currently at `http://github.com/jar398/tryphy/` - sorry, I forgot
about this requirement.  Easily moved.

What should the repo be called (`tryphy` is silly and uninformative;
maybe `service_tests` or similar)?  And how do we cause it to come into
being?

### (1) Is the API correctly described in the docs?

There are two aspects of this question.  One is *correctness* -
whether the documentation says anything about the services that's not
true.  The other is *completeness* - whether it adequately
describes how the services actually work.

Agreement between the two is not a high bar given how noncommittal the
documentation is, so the two rarely disagree, and I would say it's
largely correct in what it says.

The documentation doesn't answer the question "what does this service
do" in the kind of detail one would expect from a reference document,
and it does not explain the syntax or semantics of the result.  (The
newer documentation provides the output generated for the examples,
which is helpful but often mystifying.)

With some work, it would be possible to list all the information that
ought to be added to the documentation.

One particular situation that I wrote tests for was the claim in the
documentation that an error message will be informative.

It's hard for a program to judge the informativeness of a message, so
the tests use the presence of a particular keyword as a proxy for
informativeness.  These tests often fail because the message actually
is uninformative or wrong, not because I was unlucky and picked the
wrong keyword.

As these messages are corrected, it may turn out that the corrected
message does not contain the keyword, and that's OK.  In this
situation the test will have to be updated.

### (2) Edge cases

For some, but not all, the tests check what happens when there is one
unknown taxon, or if all taxa are unknown.

There are no checks involving taxonomic names with peculiar syntax as
suggested.  I did notice something odd, which is that some services
(`si/eol/images` maybe?) given a single letter as a name will yield
results, even though a single letter cannot plausibly be a taxon name.
This may be oversealous fuzzy matching.  If a downstream service is
doing peculiar things, it's not clear what the Phylotastic services
can do about it anyhow.

### Input range limits

I checked running time as a function of input or output size for four
of the services:

* `fn/names_url`: 10M input is processed in 4 minutes (time depends on input size, so should be about 600,000 bytes in 15 seconds)
* `fn/names_text`: accepts inputs up to 30 KByte (no way to get close to 15 seconds)
* `ts/all_species`: 20,000 species returned after 4 minutes (depends not on input, but on number of species below given taxon; so should be about 1250 species in 15 seconds - that seems slow to me)
* `si/eol/images`: 76 image metadata blobs returned after 18 seconds (number of images depends on taxon)

These tests require fussy code that is time consuming to prepare, so I
put off further work until later.

### Error-generating conditions

This part of the project consumed most of my attention.
There are checks for the following error situations:

* HTTP method not documented to work (`GET` where `POST` is required, etc.) - should be a 405 error
* No parameters
* Parameter with invalid name (not appropriate for this service)
* Invalid argument syntax (e.g. string instead of list, URN instead of URL)
* Degenerate argument (e.g. tree too small)
* Input too large
* Wrong HTTP status code (e.g. 500 or 200 instead of 400)

But not all such checks are present for every service.

## Neighboring concerns

Here are some things I worked on that were not strictly part of the
project description.

### Is HTTP being used properly?

One of the services (`sls/remove_list`) was described in the
documentation as accessed with `GET` which would be incorrect
according to the HTTP protocol.  (`GET` is reserved for
side-effect-free operations.)  The later documentation amended this to
"`GET` or `POST`".  I added a test that fails if `GET` works with this
service.  You may want to suppress this test if `GET` needs to be
supported for backward compatiblity purposes.

### Do services have peculiar side effects?

The `sls/insert_list` service fails to add the list when there is no access
token, but returns success (200) even so.  I can't tell whether it
*should* fail but I suspect it should (you need to be authenticated in
order to add a list).  But strangely, even when it fails, the server's
list id counter increments.  This is benign but I'm sure it's
unintended.

### Regression tests

I implemented a rudimentary regression test feature, but it is not
required by the project description and has some issues (e.g. does not
understand lists where the order is immaterial, and does not deal with
access tokens).

## To be done

All failing tests need to be diagnosed, and the bug in each case
should be brought to the attention of someone who can do something
about it.  Details of many of these diagnoses are scattered in the
test system source code.

Also in the source code are questions about service design and about
odd behavior from some of the downstream services.

Document the functions in `webapp.py`.  Maybe split that file up into
several smaller files.
