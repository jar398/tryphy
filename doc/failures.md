# Transcript of tests run 2017-11-05

    for t in `ls tests/test_*.py`; do PYTHONPATH=tests python $t; done
    Read 48 requests from work/requests.json
    Read 48 exchanges from work/exchanges.json
    F{
      "status_code": 200, 
      "message": "Success", 
      "meta_data": {
        "execution_time": 0.0, 
        "creation_time": "2017-11-05T19:44:48.710982", 
        "source_urls": [
          "http://dendropy.org/library/treecompare.html#module-dendropy.calculate.treecompare"
        ]
      }, 
      "are_same_tree": false
    ...F.
    Slowest exchange for http://phylo.cs.nmsu.edu:5006/phylotastic_ws/compare_trees: 0.238145112991

    ======================================================================
    FAIL: test_bogus_newick (__main__.TestCompareTrees)
    What if the Newick is bad?
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "tests/test_compare_trees.py", line 40, in test_bogus_newick
        self.assert_response_status(x, 400)
      File "./webapp.py", line 262, in assert_response_status
        self.assertEqual(x.status_code, code, message)
    AssertionError: 500 Error: global name 'Error' is not defined

Looks like the error is undetected, and there's an uninitialized
variable in the python code.

    ======================================================================
    FAIL: test_no_parameters (__main__.TestCompareTrees)
    What if no parameters are supplied?
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "tests/test_compare_trees.py", line 20, in test_no_parameters
        self.assert_response_status(x, 400)
      File "./webapp.py", line 262, in assert_response_status
        self.assertEqual(x.status_code, code, message)
    AssertionError: 500 Error: 'NoneType' object has no attribute '__getitem__'

The error is undetected, and there's a bug in the python code.

    ----------------------------------------------------------------------
    Ran 6 tests in 2.664s

    FAILED (failures=2)
    }Read 48 requests from work/requests.json
    Read 48 exchanges from work/exchanges.json
    No such resource: text-sample
    E..No such resource: text-sample
    E.
    Slowest exchange for http://phylo.cs.nmsu.edu:5004/phylotastic_ws/fn/names_text: 0.626534938812

    ======================================================================
    ERROR: test_engines (__main__.TestFnNamesText)
    It looks like engines 6, 7, and 8 are all the same.
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "tests/test_fn_names_text.py", line 55, in test_engines
        request = service.get_request('GET', {u'engine': engine, u'text': get_sample()[0:30000]})
      File "tests/test_fn_names_text.py", line 17, in get_sample
        with codecs.open(webapp.find_resource('text-sample'), 'r', 'latin-1') as infile:
      File "/System/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/codecs.py", line 884, in open
        file = __builtin__.open(filename, mode, buffering)
    TypeError: coercing to Unicode: need string or buffer, NoneType found

I need to look into this.  Doesn't make sense on a quick initial
scan.  Maybe a sys.path issue?

    ======================================================================
    ERROR: test_large_input (__main__.TestFnNamesText)
    Test large input.
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "tests/test_fn_names_text.py", line 42, in test_large_input
        request = service.get_request('GET', {u'text': get_sample()[0:30000]})
      File "tests/test_fn_names_text.py", line 17, in get_sample
        with codecs.open(webapp.find_resource('text-sample'), 'r', 'latin-1') as infile:
      File "/System/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/codecs.py", line 884, in open
        file = __builtin__.open(filename, mode, buffering)
    TypeError: coercing to Unicode: need string or buffer, NoneType found

Same as previous

    ----------------------------------------------------------------------
    Ran 5 tests in 1.365s

    FAILED (errors=2)
    Read 48 requests from work/requests.json
    Read 48 exchanges from work/exchanges.json
    ....
    Be patient, takes four minutes
    ....
    Slowest exchange for http://phylo.cs.nmsu.edu:5004/phylotastic_ws/fn/names_url: 248.884441853

The message is wrong (fix test file)

    ----------------------------------------------------------------------
    Ran 8 tests in 260.461s

    OK
    Read 48 requests from work/requests.json
    Read 48 exchanges from work/exchanges.json
    ss..ssss.s.....
    Slowest exchange for http://phylo.cs.nmsu.edu:5004/phylotastic_ws/gt/ot/get_tree: 3.56758093834

    ----------------------------------------------------------------------
    Ran 14 tests in 16.957s

    OK (skipped=7)
    Read 48 requests from work/requests.json
    Read 48 exchanges from work/exchanges.json
    ss..ssssFs..{
      "status_code": 500, 
      "request": null, 
      "response": {
        "message": "Error: List of resolved names empty"
      }, 
      "content_type": "application/json", 
      "time": 0.5094292163848877
    F...F
    Slowest exchange for http://phylo.cs.nmsu.edu:5004/phylotastic_ws/gt/ot/tree: 2.03409099579

    ======================================================================
    FAIL: test_bad_names (__main__.TestGtOtTree)
    Try a set of names none of which will be seen as a taxon name.
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "/Users/jar/a/phy/tryphy/tests/test_gt_ot_get_tree.py", line 85, in test_bad_names
        'no "least" in message: "%s"' % mess)
    AssertionError: no "least" in message: "Error: Missing parameter 'taxa'"

The error message is wrong.

    ======================================================================
    FAIL: test_example_14 (__main__.TestGtOtTree)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "tests/test_gt_ot_tree.py", line 43, in test_example_14
        self.assert_success(x)
      File "./webapp.py", line 243, in assert_success
        self.assert_response_status(x, 200, message)
      File "./webapp.py", line 262, in assert_response_status
        self.assertEqual(x.status_code, code, message)
    AssertionError: 500 Error: List of resolved names empty

Should be a 400.

    ======================================================================
    FAIL: test_some_bad (__main__.TestGtOtTree)
    Two good names, one bad.
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "/Users/jar/a/phy/tryphy/tests/test_gt_ot_get_tree.py", line 99, in test_some_bad
        self.assert_success(x, mess)
      File "./webapp.py", line 243, in assert_success
        self.assert_response_status(x, 200, message)
      File "./webapp.py", line 262, in assert_response_status
        self.assertEqual(x.status_code, code, message)
    AssertionError: Error: Missing parameter 'taxa'

Error message is incorrect.

    ----------------------------------------------------------------------
    Ran 16 tests in 10.318s

    FAILED (failures=3, skipped=7)
    }Read 48 requests from work/requests.json
    Read 48 exchanges from work/exchanges.json
    ss..ssss.s.......
    Slowest exchange for http://phylo.cs.nmsu.edu:5004/phylotastic_ws/gt/pm/get_tree: 2.6761739254

    ----------------------------------------------------------------------
    Ran 16 tests in 20.557s

    OK (skipped=7)
    Read 48 requests from work/requests.json
    Read 48 exchanges from work/exchanges.json
    ss..ssssFs..F...F
    Slowest exchange for http://phylo.cs.nmsu.edu:5004/phylotastic_ws/gt/pm/tree: 2.70201301575

    ======================================================================
    FAIL: test_bad_names (__main__.TestGtPmTree)
    Try a set of names none of which will be seen as a taxon name.
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "/Users/jar/a/phy/tryphy/tests/test_gt_ot_get_tree.py", line 85, in test_bad_names
        'no "least" in message: "%s"' % mess)
    AssertionError: no "least" in message: "Error: Missing parameter 'taxa'"

See above

    ======================================================================
    FAIL: test_example_42 (__main__.TestGtPmTree)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "tests/test_gt_pm_tree.py", line 30, in test_example_42
        self.assert_success(x)
      File "./webapp.py", line 246, in assert_success
        self.assertEqual(j[u'message'], u'Success')
    AssertionError: u'No tree found using phylomatic web service' != u'Success'
    - No tree found using phylomatic web service
    + Success

200 status when 400 would have been better?  I think.

    ======================================================================
    FAIL: test_some_bad (__main__.TestGtPmTree)
    Two good names, one bad.
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "/Users/jar/a/phy/tryphy/tests/test_gt_ot_get_tree.py", line 99, in test_some_bad
        self.assert_success(x, mess)
      File "./webapp.py", line 243, in assert_success
        self.assert_response_status(x, 200, message)
      File "./webapp.py", line 262, in assert_response_status
        self.assertEqual(x.status_code, code, message)
    AssertionError: Error: Missing parameter 'taxa'

Incorrect message

    ----------------------------------------------------------------------
    Ran 16 tests in 11.662s

    FAILED (failures=3, skipped=7)
    Read 48 requests from work/requests.json
    Read 48 exchanges from work/exchanges.json
    ss..ssss.s......
    Slowest exchange for http://phylo.cs.nmsu.edu:5004/phylotastic_ws/gt/pt/get_tree: 5.16291499138

    ----------------------------------------------------------------------
    Ran 15 tests in 21.689s

    OK (skipped=7)
    Read 48 requests from work/requests.json
    Read 48 exchanges from work/exchanges.json
    ss..ssssFs.....F
    Slowest exchange for http://phylo.cs.nmsu.edu:5004/phylotastic_ws/gt/pt/tree: 3.58161687851

    ======================================================================
    FAIL: test_bad_names (__main__.TestGtPtTree)
    Try a set of names none of which will be seen as a taxon name.
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "/Users/jar/a/phy/tryphy/tests/test_gt_ot_get_tree.py", line 85, in test_bad_names
        'no "least" in message: "%s"' % mess)
    AssertionError: no "least" in message: "Error: Missing parameter 'taxa'"

Incorrect message

    ======================================================================
    FAIL: test_some_bad (__main__.TestGtPtTree)
    Two good names, one bad.
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "/Users/jar/a/phy/tryphy/tests/test_gt_ot_get_tree.py", line 99, in test_some_bad
        self.assert_success(x, mess)
      File "./webapp.py", line 243, in assert_success
        self.assert_response_status(x, 200, message)
      File "./webapp.py", line 262, in assert_response_status
        self.assertEqual(x.status_code, code, message)
    AssertionError: Error: Missing parameter 'taxa'

Incorrect message

    ----------------------------------------------------------------------
    Ran 15 tests in 11.393s

    FAILED (failures=2, skipped=7)
    Read 48 requests from work/requests.json
    Read 48 exchanges from work/exchanges.json
    F.
    Slowest exchange for http://phylo.cs.nmsu.edu:5006/phylotastic_ws/md/get_studies: 1.42290902138

    ======================================================================
    FAIL: test_example_36 (__main__.TestMdGetStudies)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "tests/test_md_get_studies.py", line 35, in test_example_36
        self.assert_success(x, mess)
      File "./webapp.py", line 243, in assert_success
        self.assert_response_status(x, 200, message)
      File "./webapp.py", line 262, in assert_response_status
        self.assertEqual(x.status_code, code, message)
    AssertionError: OpenTree Error: Not enough valid node ids provided to construct a subtree (there must be at least two).

? (investigate)

    ----------------------------------------------------------------------
    Ran 2 tests in 1.971s

    FAILED (failures=1)
    Read 48 requests from work/requests.json
    Read 48 exchanges from work/exchanges.json
    ..
    Slowest exchange for http://phylo.cs.nmsu.edu:5006/phylotastic_ws/md/studies: 1.43575906754

    ----------------------------------------------------------------------
    Ran 2 tests in 2.598s

    OK
    Read 48 requests from work/requests.json
    Read 48 exchanges from work/exchanges.json
    F.F.
    Slowest exchange for http://phylo.cs.nmsu.edu:5009/phylotastic_ws/sc/metadata_scale: 1.48180103302

    ======================================================================
    FAIL: test_bogus_newick (__main__.TestScMetadataScale)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "tests/test_sc_metadata_scale.py", line 38, in test_bogus_newick
        self.assert_response_status(x, 400)
      File "./webapp.py", line 262, in assert_response_status
        self.assertEqual(x.status_code, code, message)
    AssertionError: 500 Error: Failed to get metadata from datelife R package

Status should have been 400

    ======================================================================
    FAIL: test_no_parameters (__main__.TestScMetadataScale)
    What if there are no parameters?  Hope for 400.
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "tests/test_sc_metadata_scale.py", line 26, in test_no_parameters
        self.assert_response_status(x, 400, mess)
      File "./webapp.py", line 262, in assert_response_status
        self.assertEqual(x.status_code, code, message)
    AssertionError: Error: 'NoneType' object has no attribute '__getitem__'

Error situation not detected by server.

    ----------------------------------------------------------------------
    Ran 4 tests in 2.145s

    FAILED (failures=2)
    Read 48 requests from work/requests.json
    Read 48 exchanges from work/exchanges.json
    F..F.
    Slowest exchange for http://phylo.cs.nmsu.edu:5009/phylotastic_ws/sc/scale: 4.71095299721

    ======================================================================
    FAIL: test_bogus_newick (__main__.TestScScale)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "tests/test_sc_scale.py", line 34, in test_bogus_newick
        self.assert_response_status(x, 400)
      File "./webapp.py", line 262, in assert_response_status
        self.assertEqual(x.status_code, code, message)
    AssertionError: 500 Error: Failed to scale from datelife R package

Should be 400 status

    ======================================================================
    FAIL: test_no_parameters (__main__.TestScScale)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "tests/test_sc_scale.py", line 22, in test_no_parameters
        self.assert_response_status(x, 400, mess)
      File "./webapp.py", line 262, in assert_response_status
        self.assertEqual(x.status_code, code, message)
    AssertionError: Error: 'NoneType' object has no attribute '__getitem__'

Error situation not detected by server.  Should be 400.

    ----------------------------------------------------------------------
    Ran 5 tests in 6.890s

    FAILED (failures=2)
    Read 48 requests from work/requests.json
    Read 48 exchanges from work/exchanges.json
    FF.Patience, this may take 20 seconds
    F.sFF.Patience, this may take 20 seconds
    F..
    Slowest exchange for http://phylo.cs.nmsu.edu:5004/phylotastic_ws/si/eol/get_images: 2.55190706253

    ======================================================================
    FAIL: test_bad_method (__main__.SiEolImagesTester)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "tests/test_si_eol_get_images.py", line 18, in test_bad_method
        self.assertEqual(x.status_code, 405)
    AssertionError: 400 != 405

GET where POST expected - not reported properly

    ======================================================================
    FAIL: test_bad_name (__main__.SiEolImagesTester)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "tests/test_si_eol_get_images.py", line 58, in test_bad_name
        self.assert_success(x, m)
      File "./webapp.py", line 243, in assert_success
        self.assert_response_status(x, 200, message)
      File "./webapp.py", line 262, in assert_response_status
        self.assertEqual(x.status_code, code, message)
    AssertionError: Error: Missing parameter 'species'

Incorrect message, I think (investigate)

    ======================================================================
    FAIL: test_bad_value_type (__main__.SiEolImagesTester)
    What if the value is a single species name instead of a list?
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "tests/test_si_eol_get_images.py", line 47, in test_bad_value_type
        self.assertTrue(x.status_code % 100 == 4, x.status_code)
    AssertionError: 400

That's a bug in the test.  Need to fix it.

    ======================================================================
    FAIL: test_bad_method (__main__.TestSiEolGetImages)
    What if you do a GET when the service is expecting a POST?
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "tests/test_si_eol_get_images.py", line 87, in test_bad_method
        self.assertEqual(x.status_code, 405)
    AssertionError: 400 != 405

GET where POST expected - not reported properly

    ======================================================================
    FAIL: test_bad_name (__main__.TestSiEolGetImages)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "tests/test_si_eol_get_images.py", line 58, in test_bad_name
        self.assert_success(x, m)
      File "./webapp.py", line 243, in assert_success
        self.assert_response_status(x, 200, message)
      File "./webapp.py", line 262, in assert_response_status
        self.assertEqual(x.status_code, code, message)
    AssertionError: Error: Missing parameter 'species'

Incorrect message? (check)

    ======================================================================
    FAIL: test_bad_value_type (__main__.TestSiEolGetImages)
    What if the value is a single species name instead of a list?
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "tests/test_si_eol_get_images.py", line 47, in test_bad_value_type
        self.assertTrue(x.status_code % 100 == 4, x.status_code)
    AssertionError: 400

Bug in test, should be `/` not `%`

    ----------------------------------------------------------------------
    Ran 11 tests in 4.674s

    FAILED (failures=6, skipped=1)
    Traceback (most recent call last):
      File "tests/test_si_eol_images.py", line 14, in <module>
        import si_eol_get_images.SiEolImagesTester
    ImportError: No module named si_eol_get_images.SiEolImagesTester
    Read 48 requests from work/requests.json
    Read 48 exchanges from work/exchanges.json
    ssss....
    Slowest exchange for http://phylo.cs.nmsu.edu:5004/phylotastic_ws/sl/eol/get_links: 0.73219704628

    ----------------------------------------------------------------------
    Ran 7 tests in 1.511s

    OK (skipped=4)
    Read 48 requests from work/requests.json
    Read 48 exchanges from work/exchanges.json
    ssss.F.F
    Slowest exchange for http://phylo.cs.nmsu.edu:5004/phylotastic_ws/sl/eol/links: 5.85573601723

    ======================================================================
    FAIL: test_bad_species (__main__.TestSlEolLinks)
    What if the species name is unknown?
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "/Users/jar/a/phy/tryphy/tests/test_sl_eol_get_links.py", line 50, in test_bad_species
        self.assertEqual(x.json()[u'species'][0][u'matched_name'], '')
    AssertionError: u'Macronectes halli Mathews 1912' != ''

The taxon name is 'Nosuchtaxonia notatall'.  EOL really shouldn't
match that to any species.

    ======================================================================
    FAIL: test_no_parameter (__main__.TestSlEolLinks)
    What if no parameters are supplied?  (Hoping for 400.)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "/Users/jar/a/phy/tryphy/tests/test_sl_eol_get_links.py", line 27, in test_no_parameter
        self.assert_response_status(x, 400)
      File "./webapp.py", line 262, in assert_response_status
        self.assertEqual(x.status_code, code, message)
    AssertionError: 500 Error: 'NoneType' object has no attribute '__getitem__'

No parameters needs to be detected & turned into 400

    ----------------------------------------------------------------------
    Ran 7 tests in 6.858s

    FAILED (failures=2, skipped=4)
      File "tests/test_sls_get_list.py", line 119

        ^
    SyntaxError: EOF while scanning triple-quoted string literal

Oops.  Bug in test file.

    Read 48 requests from work/requests.json
    Read 48 exchanges from work/exchanges.json
    setting up insert_list
    list id: 114
    {
      "status_code": 200, 
      "request": null, 
      "response": {
        "status_code": 200, 
        "message": "Success", 
        "list": {
          "list_title": "Bird Species List for Everglades National Park", 
          "list_id": 114, 
          "list_species": [
            "Aix sponsa", 
            "Anas strepera", 
            "Caprimulgus vociferus", 
            "Columba livia", 
            "Ceryle alcyon", 
            "Aramus guarauna"
          ]
        }
      }, 
      "content_type": "application/json", 
      "time": 0.21498489379882812
    }.unwanted list id: 115
    Ftearing down insert_list
    removed 114
    removed 115
    s
    ======================================================================
    FAIL: test_example_no_access (__main__.TestSlsInsertList)
    Very strange - this test appears to succeed, even if the access

Need to fix my doc strings so that first line alone is always intelligible.

    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "tests/test_sls_insert_list.py", line 43, in test_example_no_access
        self.assert_response_status(x, 400, mess)
      File "./webapp.py", line 262, in assert_response_status
        self.assertEqual(x.status_code, code, message)
    AssertionError: Success

Appears to succeed, but actually doesn't.

    ----------------------------------------------------------------------
    Ran 2 tests in 1.600s

    FAILED (failures=1, skipped=1)
    Read 48 requests from work/requests.json
    Read 48 exchanges from work/exchanges.json
    FFF.cleaning up
    removed 116
    s
    ======================================================================
    FAIL: test_bad_token (__main__.TestSlsRemoveList)
    What is we give it a bad access token?
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "tests/test_sls_remove_list.py", line 71, in test_bad_token
        self.assertTrue(u'oken' in mess)
    AssertionError: False is not true

Error message is wrong.

    ======================================================================
    FAIL: test_example_32 (__main__.TestSlsRemoveList)
    I'm getting "Error: Missing parameter 'user_id'"
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "tests/test_sls_remove_list.py", line 92, in test_example_32
        self.assert_success(x, mess)
      File "./webapp.py", line 243, in assert_success
        self.assert_response_status(x, 200, message)
      File "./webapp.py", line 262, in assert_response_status
        self.assertEqual(x.status_code, code, message)
    AssertionError: Error: Missing parameter 'user_id'

Error message is wrong.

    ======================================================================
    FAIL: test_get_should_fail (__main__.TestSlsRemoveList)
    As of 2017-11-05, we get either 400
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "tests/test_sls_remove_list.py", line 42, in test_get_should_fail
        self.assert_response_status(x, 405, mess)
      File "./webapp.py", line 262, in assert_response_status
        self.assertEqual(x.status_code, code, message)
    AssertionError: Error: Missing parameter 'access_token'

Error message is wrong.

    ----------------------------------------------------------------------
    Ran 4 tests in 1.423s

    FAILED (failures=3, skipped=1)
    Read 48 requests from work/requests.json
    Read 48 exchanges from work/exchanges.json
    .cleaning up
    removed 117
    s
    ----------------------------------------------------------------------
    Ran 1 test in 1.458s

Need to write some tests for this service

    OK (skipped=1)
    Read 48 requests from work/requests.json
    Read 48 exchanges from work/exchanges.json
    ..cleaning up
    removed 118
    s
    ----------------------------------------------------------------------
    Ran 2 tests in 1.538s

    OK (skipped=1)
      File "tests/test_tnrs_gnr_names.py", line 4
        sys.path.append('./)
                           ^
    SyntaxError: EOL while scanning string literal
    Read 48 requests from work/requests.json
    Read 48 exchanges from work/exchanges.json
    ...s...
    Slowest exchange for http://phylo.cs.nmsu.edu:5004/phylotastic_ws/tnrs/gnr/resolve: 0.673294067383
    ssssss
    ----------------------------------------------------------------------
    Ran 12 tests in 3.126s

    OK (skipped=7)
    Read 48 requests from work/requests.json
    Read 48 exchanges from work/exchanges.json
    ....s.F
    Slowest exchange for http://phylo.cs.nmsu.edu:5004/phylotastic_ws/tnrs/ot/names: 0.516929864883
    ssssss
    ======================================================================
    FAIL: test_no_parameter (__main__.TestTnrsOtNames)
    Edge case:
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "/Users/jar/a/phy/tryphy/tests/test_tnrs_ot_resolve.py", line 48, in test_no_parameter
        self.assert_response_status(x, 400)
      File "./webapp.py", line 262, in assert_response_status
        self.assertEqual(x.status_code, code, message)
    AssertionError: 500 Error: 'NoneType' object has no attribute '__getitem__'

Should check for no parameters and yield 400

    ----------------------------------------------------------------------
    Ran 12 tests in 2.479s

    FAILED (failures=1, skipped=7)
    Read 48 requests from work/requests.json
    Read 48 exchanges from work/exchanges.json
    ....s...
    Slowest exchange for http://phylo.cs.nmsu.edu:5004/phylotastic_ws/tnrs/ot/resolve: 0.510138034821
    ssssss
    ----------------------------------------------------------------------
    Ran 13 tests in 2.989s

    OK (skipped=7)
    Read 48 requests from work/requests.json
    Read 48 exchanges from work/exchanges.json
    Fs..Apis mellifera: 1 0.531002044678
    Apis: 24 0.552427053452
    Apini: 24 0.51824593544
    Apinae: 1269 0.631856918335
    Apidae: 5680 0.825549125671
    ..
    Slowest exchange for http://phylo.cs.nmsu.edu:5004/phylotastic_ws/ts/all_species: 0.825549125671

    ======================================================================
    FAIL: test_bad_name (__main__.TestTsAllSpecies)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "tests/test_ts_all_species.py", line 27, in test_bad_name
        self.assertTrue(x.status_code >= 400, '%s: %s' % (x.status_code, m))
    AssertionError: 200: No Taxon matched with Nosuchtaxonia

Error shouldn't have a 200 status.

    ----------------------------------------------------------------------
    Ran 6 tests in 4.889s

    FAILED (failures=1, skipped=1)
    Read 48 requests from work/requests.json
    Read 48 exchanges from work/exchanges.json
    sF.F..
    Slowest exchange for http://phylo.cs.nmsu.edu:5004/phylotastic_ws/ts/country_species: 0.550210952759

    ======================================================================
    FAIL: test_bad_taxon (__main__.TestTsCountrySpecies)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "tests/test_ts_country_species.py", line 30, in test_bad_taxon
        self.assertTrue(x.status_code >= 400, m)
    AssertionError: No Taxon matched with Nosuchtaxonia

Error shouldn't have a 200 status.

    ======================================================================
    FAIL: test_example_17p (__main__.TestTsCountrySpecies)
    2017-11-05 This test complains about the 'taxon' parameter being
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "tests/test_ts_country_species.py", line 70, in test_example_17p
        self.assert_success(x, m)
      File "./webapp.py", line 243, in assert_success
        self.assert_response_status(x, 200, message)
      File "./webapp.py", line 262, in assert_response_status
        self.assertEqual(x.status_code, code, message)
    AssertionError: Error: Missing parameter 'taxon'

Incorrect error message

    ----------------------------------------------------------------------
    Ran 6 tests in 1.996s

    FAILED (failures=2, skipped=1)
    Read 48 requests from work/requests.json
    Read 48 exchanges from work/exchanges.json
    FF..F.
    Slowest exchange for http://phylo.cs.nmsu.edu:5004/phylotastic_ws/ts/ncbi/genome_species: 1.72170305252

    ======================================================================
    FAIL: test_bad_parameter_name (__main__.TestTsNcbiGenomeSpecies)
    What if we give it an unknown parameter name?
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "tests/test_ts_ncbi_genome_species.py", line 41, in test_bad_parameter_name
        self.assertEqual(x.status_code, 400, mess)
    AssertionError: Success

Should be error, but response is 200

    ======================================================================
    FAIL: test_bad_taxon (__main__.TestTsNcbiGenomeSpecies)
    What if the taxon is unknown?
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "tests/test_ts_ncbi_genome_species.py", line 55, in test_bad_taxon
        self.assertEqual(x.status_code, 400, mess)
    AssertionError: No match found for term Unknownia

Should be error, but response is 200 (I think)

    ======================================================================
    FAIL: test_example_22_post (__main__.TestTsNcbiGenomeSpecies)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "tests/test_ts_ncbi_genome_species.py", line 90, in test_example_22_post
        self.assert_success(x)
      File "./webapp.py", line 243, in assert_success
        self.assert_response_status(x, 200, message)
      File "./webapp.py", line 262, in assert_response_status
        self.assertEqual(x.status_code, code, message)
    AssertionError: 400 Error: Missing parameter 'taxon'

Incorrect error message

    ----------------------------------------------------------------------
    Ran 6 tests in 5.679s

    FAILED (failures=3)
