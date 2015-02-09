#!/usr/bin/env python2

import adblock

def bench(l, desc=None):
    from time import time

    start   = time()
    result  = l()
    elapsed = time() - start

    if not desc:
        desc = result

    print "[%s] %0.5f seconds" % (desc, elapsed)

    return result


rules = adblock.load_rules()

# Types of elements that can be blocked:
#   https://adblockplus.org/en/filter-cheatsheet#options
# options = {'script': False, 'domain': 'www.mystartpage.com'}
with open("urls.txt") as urls:
    for url in urls:
        url = url.strip()
        if bench(lambda: rules.should_block(url)):
            print "Blocked:", url
