"""Common infrastructure for the list management services:
   sls/insert_list
   sls/get_list
   sls/remove_list
and
   sls/replace_species  (which modifies an existing list)

Use with:
    lists.temporary_lists.append(24)
    lists.cleanup()

"""

import copy
import webapp

# These variables, which keep track of which lists have been created
# by tests (insert_list service), are global.  Ideally they should be
# specific to each test class, but it doesn't matter so long as tests
# aren't run in parallel.

# A better design might be to make this code into a superclass of all
# the list manipulation services.

temporary_lists = []   #68, 69, 70, 71, 72, 73, 74, 75, 76

def cleanup():
    global temporary_lists
    losers = []
    for lst in temporary_lists:
        if not remove_list(lst):
            losers.append(lst)
    temporary_lists = losers

service = webapp.get_service(5005, 'sls/remove_list')

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

# Store this list temporarily so we can test get, update, and remove

sample_list =\
  {u'list_extra_info': u'',
   u'list_description': u'A list of the bird species and their endangered, threatened or invasive status',
   u'list_keywords': [u'bird', u'endangered species', u'Everglades'],
   u'list_curator': u'HD Laughinghouse',
   u'list_origin': u'webapp',
   u'list_curation_date': u'02-24-2016',
   u'list_source': u'Des',
   u'list_date_published': u'01-01-2006',
   u'list_focal_clade': u'Aves',
   u'list_title': u'Bird Species List for Everglades National Park',
   u'list_author': [u'Bass, O.', 'Cunningham, R.'],
   u'list_species': [{u'family': u'', u'scientific_name': u'Aix sponsa', u'scientific_name_authorship': u'', u'order': u'Anseriformes', u'vernacular_name': u'Wood Duck', u'phylum': u'', u'nomenclature_code': u'ICZN', u'class': u''},
                     {u'family': u'', u'scientific_name': u'Anas strepera', u'scientific_name_authorship': u'', u'order': u'Anseriformes', u'vernacular_name': u'Gadwall', u'phylum': u'', u'nomenclature_code': u'ICZN', u'class': u''},
                     {u'family': u'', u'scientific_name': u'Caprimulgus vociferus', u'scientific_name_authorship': u'', u'order': u'Caprimulgiformes', u'vernacular_name': u'Whip-poor-will', u'phylum': u'', u'nomenclature_code': u'ICZN', u'class': u''},
                     {u'family': u'', u'scientific_name': u'Columba livia', u'scientific_name_authorship': u'', u'order': u'Columbiformes', u'vernacular_name': u'Rock Dove', u'phylum': u'', u'nomenclature_code': u'ICZN', u'class': u''},
                     {u'family': u'', u'scientific_name': u'Ceryle alcyon', u'scientific_name_authorship': u'', u'order': u'Coraciiformes', u'vernacular_name': u'Belted Kingfisher', u'phylum': u'', u'nomenclature_code': u'ICZN', u'class': u''},
                     {u'family': u'', u'scientific_name': u'Aramus guarauna', u'scientific_name_authorship': u'', u'order': u'Gruiformes', u'vernacular_name': u'Limpkin', u'phylum': u'', u'nomenclature_code': u'ICZN', u'class': u''}]}

def insert_sample_list(public=True):
    service = webapp.get_service(5005, 'sls/insert_list')
    user_id = webapp.config('user_id')
    access_token = webapp.config('access_token')

    lst = copy.copy(sample_list)
    lst[u'is_list_public'] = public
    params = {u'user_id': user_id,
              u'access_token': access_token,
              u'list': lst}
    x = service.get_request('POST', params).exchange()
    if x.status_code != 200:
        return None
    list_id = x.json().get(u'list_id')
    if list_id != None:
        temporary_lists.append(list_id)
    return list_id
