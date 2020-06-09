"""
An mitmproxy adblock script!
(Required python modules: re2 and adblockparser)

(c) 2015-2019 epitron
"""

import re2
from mitmproxy.script import concurrent
from mitmproxy import http
from adblockparser import AdblockRules
from glob import glob

__version__ = '0.1.0'

IMAGE_MATCHER      = re2.compile(r"\.(png|jpe?g|gif)$")
SCRIPT_MATCHER     = re2.compile(r"\.(js)$")
STYLESHEET_MATCHER = re2.compile(r"\.(css)$")

def log(msg):
    print(msg)

def combined(filenames):
  '''
  Open and combine many files into a single generator which returns all
  of their lines. (Like running "cat" on a bunch of files.)
  '''
  for filename in filenames:
    with open(filename) as file:
      for line in file:
        yield line


def load_rules(blocklists=None):
    rules = AdblockRules(
        combined(blocklists),
        use_re2=True,
        max_mem=512*1024*1024
        # supported_options=['script', 'domain', 'image', 'stylesheet', 'object']
    )

    return rules


blocklists = glob("blocklists/*")

if len(blocklists) == 0:
  log("Error, no blocklists found in 'blocklists/'. Please run the 'update-blocklists' script.")
  raise SystemExit

else:
  log("* Available blocklists:")
  for list in blocklists:
    log("  |_ %s" % list)

log("* Loading blocklists...")
rules = load_rules(blocklists)
log("")
log("* Done! Proxy server is ready to go!")


@concurrent
def request(flow):
    global rules

    req = flow.request

    options = {'domain': req.host}

    if IMAGE_MATCHER.search(req.path):
        options["image"] = True
    elif SCRIPT_MATCHER.search(req.path):
        options["script"] = True
    elif STYLESHEET_MATCHER.search(req.path):
        options["stylesheet"] = True

    if rules.should_block(req.url, options):
        log("vvvvvvvvvvvvvvvvvvvv BLOCKED vvvvvvvvvvvvvvvvvvvvvvvvvvv")
        log("accept: %s" % flow.request.headers.get("Accept"))
        log("blocked-url: %s" % flow.request.url)
        log("^^^^^^^^^^^^^^^^^^^^ BLOCKED ^^^^^^^^^^^^^^^^^^^^^^^^^^^")

        flow.response = http.HTTPResponse.make(
            200,
            b"BLOCKED.",
            {"Content-Type": "text/html"}
        )
    else:
        log("url: %s" % flow.request.url)
