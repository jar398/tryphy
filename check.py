# Common type checking logic and types to be used by all tests
# Copied from treemachine/ws-tests/  - eventually remove that

import sys, json
import traceback

def check_integer(x, where):
    if isinstance(x, int) or isinstance(x, long):
        return True
    else:
        print '** expected integer but got', x, where
        return False

def check_float(x, where):
    if isinstance(x, float):
        return True
    else:
        print '** expected float but got', x, where
        return False

def check_string(x, where):
    if isinstance(x, unicode):
        return True
    else:
        print '** expected string but got', x, where
        return False

def check_boolean(x, where):
    if x == True or x == False:
        return True
    else:
        print '** expected boolean but got', x, where
        return False

def field(name, check):
    if not isinstance(check, type(check_integer)):
        print '** bad check function', check, 'for', name
        return (name, (lambda x, where: False), True)
    return (name, check, True)

def opt_field(name, check):
    return (name, check, False)

def check_blob(fields):
    required = [name for (name, check, req) in fields if req]
    checks = {}
    for (name, check, req) in fields:
        checks[name] = check
    def do_check_blob(x, where):
        if not isinstance(x, dict):
            print '** expected dict but got', x, where
            return False
        win = True
        for name in x:
            if name in checks:
                check = checks[name]
                if not check(x[name], more_where(name, where)):
                    win = False
            else:
                print "** unexpected field '%s' found among %s %s" % (name, x.keys(), where)
                win = False
        for name in required:
            if not (name in x):
                print "** missing required field '%s' not found among %s %s" % (name, x.keys(), where)
                win = False
        return win
    return do_check_blob

def check_list(check):
    def do_check_list(x, where):
        if not isinstance(x, list):
            print '** expected list but got', x, where
            return False
        where = more_where('list', where)
        for y in x:
            if not check(y, where):
                return False
        return True
    return do_check_list

def check_nonempty_list(check):
    ch = check_list(check)
    def do_check_nonempty_list(x, where):
        if x == []:
            print '** expected nonempty list but got', x, where
            return False
        else:
            return ch(x, where)
    return do_check_nonempty_list

def more_where(w, where):
    if where == '':
        return where
    else:
        return w + ' in ' + where

# Check types of all keys and values in a dictionary

def check_dict(check_key, check_val):
    def do_check_dict(x, where):
        if not isinstance(x, dict):
            print '** expected dict but got', x, where
            return False
        ok = True
        for key in x:
            if not check_key(key, where):
                ok = False
            val = x[key]
            if not check_val(val, ' in ' + key + where):
                ok = False
        return ok
    return do_check_dict
