"""Common infrastructure for the list management services:
   sls/insert_list
   sls/get_list
   sls/remove_list
and
   sls/replace_species  (which modifies an existing list)

Use with:
    lists.sample_list = 23
    lists.temporary_lists.append(24)
    lists.cleanup()

but now I don't remember what the difference is, i.e. why the
sample_list is not just another temporary_list !

"""

import webapp

# These variables, which keep track of which lists have been created
# by tests (insert_list service), are global.  Ideally they should be
# specific to each test class, but it doesn't matter so long as tests
# aren't run in parallel.

temporary_lists = []   #68, 69, 70, 71, 72, 73, 74, 75, 76
sample_list = None

def cleanup():
    global temporary_lists, sample_list
    if sample_list != None:
        if remove_list(sample_list):
            sample_list = None
    losers = []
    for lst in temporary_lists:
        if not remove_list(lst):
            losers.append(lst)
    temporary_lists = losers

url = 'http://phylo.cs.nmsu.edu:5005/phylotastic_ws/sls/remove_list'
service = webapp.get_service(url)

def remove_list(lst):
    user_id = webapp.config('user_id')
    access_token = webapp.config('access_token')
    x = service.get_request('GET', {u'list_id': lst,
                                    u'user_id': user_id,
                                    u'access_token': access_token}
                             ).exchange()
    if x.status_code == 200:
        print 'removed', lst
        return True
    else:
        print 'Did not remove %s; message = %s' % (lst, x.json()[u'message'])
        return False
