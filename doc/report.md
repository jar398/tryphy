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

You can run the tests as directed in [the README file](..README.md).  A number of
tests fail.  I believe that every failure reflects a bug in some
service.

The testing framework (`unittest`, see
[here](test-framework-choice.md)) is not designed to produce output
that explains failures.  You get some kind of message, and the
source file and line number in a backtrace.  To understand what
happened you have to read the test script code.

The following sections attempt to compare what the test system does
against what was specified in the project description.

### All examples in the documentation

Yes - the examples were extracted from the (old) documentation and
added to the test scripts automatically.  In some cases the result is
partially checked for correctness, but for many services there is only
a check for a 200 response.

### 3 other tests

Yes, with five exceptions (most of which are list methods).

### Tests documented inline using an existing standard?

Not yet.

### Use an open-source license?

BSD 2-clause, but there it can be relicensed if necessary.

### Developed in a new or existing github repository associated with the Phylotastic project

No, currently at `http://github.com/jar398/tryphy/` - sorry, I forgot
about this provision.  Easily moved.  What should the repo be called
(`tryphy` is silly and uninformative; maybe `service_tests` or
similar) and how do we cause it to come into being?

### (1) Is the API correctly described in the docs?

There are two aspects of this question.  One is *correctness* -
whether the documentation says anything about the services that's not
true.  The other is *completeness* - whether it adequately
describes how the services actually work.

Where the API disagrees with the documentation, this could be due
either to the API being 'wrong' (not working as intended) or to the
documentation being 'wrong'.  Agreement between the two is not a high
bar given how noncommittal the documentation is, so the two rarely
disagree.

The documentation is certainly incomplete; it says almost nothing
about what the services do (or are intended to do).  There a brief
descriptions, one line at best, that give the general idea, and there
are parameter descriptions saying what the inputs should look like.
But there is no explanation of the returned result, e.g. what the
syntax of the response to a `sls/get_list` request is.  (The newer
documentation provides examples, but examples are often not a good
substitute for explanatory prose or schematic information about
syntax.)

### (2) Edge cases

For some, but not all, the tests check what happens when there is one
unknown taxon, or if all taxa are unknown.

There are no checks involving names with peculiar syntax.  I did
notice something odd, which is that some services (`si/eol/images`
maybe?) given a single letter as a name will yield results, even
though a single letter cannot plausibly be a taxon name.  This may be
oversealous fuzzy matching.  If a downstream service is doing peculiar
things, it's not clear what phylotastic can do about it.

### Input range limits

I checked running time as a function of input or output size for four
of the services:

* `fn/names_url`: 10M input is processed in 4 minutes (time depends on input size, so should be about 600,000 bytes in 15 seconds)
* `fn/names_text`: accepts inputs up to 30 kbyte (no way to get close to 15 seconds)
* `ts/all_species`: 20,000 species returned after 4 minutes (depends not on input, but on number of species below given taxon; so should be about 1250 species in 15 seconds - that seems slow to me)
* `si/eol/images`: 76 image metadata blobs returned after 18 seconds (number of images depends on taxon)

These tests require fussy code that is time consuming to prepare, so I
put off further work until later.

### Error-generating conditions

This part of the project consumed most of my attention.
There are checks for the following error situations:

* HTTP method not documented to work (GET instead of POST, etc.) - should be a 405 error
* No parameters
* Parameter with invalid name (not appropriate for this service)
* Invalid argument syntax (e.g. string instead of list, URN instead of URL)
* Degenerate argument (e.g. tree too small)
* Input too large
* Wrong HTTP status code (e.g. 500 or 200 instead of 400)

But not all such checks are there for every service.

## Neighboring concerns

### Are the error messages informative?

This kind of check was not demanded but I think it is valuable.

I included a number of checks for this, with the presence of a
particular keyword as a proxy for informativeness.  These tests often
fail because the message actually is inappropriate, not because I
picked the wrong keyword.

As these messages are corrected, it may turn out that the corrected
message does not contain the keyword, and that's OK.  In this
situation the test will have to be updated.

### Is HTTP being used properly?

One of the services (`sls/remove_list`) was described in the
documentation as accessed with `GET` which would be incorrect
according to the HTTP protocol.  (`GET` is reserved for
side-effect-free operations.)  The later documentation amended this to
`GET` or `POST`.  I added a test that fails if `GET` works with this
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

