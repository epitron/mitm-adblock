#!/usr/bin/env python2

from adblockparser import AdblockRules

def bench(l, desc=None):
    from time import time

    start   = time()
    result  = l()
    elapsed = time() - start

    if not desc:
        desc = result

    print "[%s] %0.5f seconds" % (desc, elapsed)

    return result

def combined(filenames):
  for filename in filenames:
    with open(filename) as file:
      for line in file:
        yield line


def load_rules(blocklists=["easylist.txt", "easyprivacy.txt", "fanboy-annoyance.txt", "fanboy-social.txt"]):
  print "Loading rules:", blocklists
  # rules = AdblockRules( combined(blocklists), use_re2=True, max_mem=512*1024*1024, supported_options=['script', 'domain'] )
  # rules = AdblockRules( combined(blocklists), use_re2=True, max_mem=512*1024*1024, supported_options=['script', 'domain'] )
  rules = AdblockRules( combined(blocklists), use_re2=True, supported_options=['script', 'domain', 'image', 'stylesheet', 'object'] )
  return rules

rules = load_rules()

# for url in ["http://google.com", "http://slashdot.org", "http://doubleclick.net"]:
with open("urls.txt") as urls:
    for url in urls:
        url = url.strip()
        if bench(lambda: rules.should_block(url)):
            print "Blocked:", url
