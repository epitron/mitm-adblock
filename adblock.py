"""
An mitmproxy adblock script!
(Required python modules: re2 and adblockparser)

(c) 2015 epitron
"""

import re2
from libmproxy.script import concurrent
from libmproxy.protocol.http import HTTPResponse
from netlib.odict import ODictCaseless
from adblockparser import AdblockRules
from glob import glob



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

def start(context, argv):
    '''
    Called once on script startup, before any other events.
    '''

    global rules

    blocklists = glob("easylists/*")

    if len(blocklists) == 0:
      context.log("Error, no blocklists found in 'easylists/'. Please run the 'update-blocklists' script.")
      raise SystemExit

    else:
      context.log("* Loading adblock rules...")
      for list in blocklists:
        context.log("  |_ %s" % list)

    rules = load_rules(blocklists)
    context.log("")
    context.log("* Done! Proxy server is ready to go!")



IMAGE_MATCHER      = re2.compile(r"\.(png|jpe?g|gif)$")
SCRIPT_MATCHER     = re2.compile(r"\.(js)$")
STYLESHEET_MATCHER = re2.compile(r"\.(css)$")

@concurrent
def request(context, flow):
    req = flow.request
    # accept = flow.request.headers["Accept"]
    # context.log("accept: %s" % flow.request.accept)

    options = {'domain': req.host}

    if IMAGE_MATCHER.search(req.path):
        options["image"] = True
    elif SCRIPT_MATCHER.search(req.path):
        options["script"] = True
    elif STYLESHEET_MATCHER.search(req.path):
        options["stylesheet"] = True

    if rules.should_block(req.url, options):
        context.log("vvvvvvvvvvvvvvvvvvvv BLOCKED vvvvvvvvvvvvvvvvvvvvvvvvvvv")
        context.log("accept: %s" % flow.request.headers.get("Accept"))
        context.log("blocked-url: %s" % flow.request.url)
        context.log("^^^^^^^^^^^^^^^^^^^^ BLOCKED ^^^^^^^^^^^^^^^^^^^^^^^^^^^")

        # resp = HTTPResponse((1,1), 404, "OK",
        #     ODictCaseless([["Content-Type", "text/html"]]),
        #     "A terrible ad has been removed!")
    
        # HTTPResponse(http_version, status_code, reason, headers, content, timestamp_start=None, timestamp_end=None)

        # resp = HTTPResponse(
        #     (1,1), 
        #     200, 
        #     "OK",
        #     ODictCaseless(
        #         [
        #             ["Content-Type", "text/html"]
        #         ]
        #     ),
        #     "BLOCKED."
        # )

        resp = HTTPResponse(
            (1,1), 
            200, 
            "OK",
            Headers(content_type="text/html"),
            "BLOCKED."
        )

        flow.reply(resp)
    else:
        context.log("url: %s" % flow.request.url)


"""
An HTTP request.

Exposes the following attributes:

    method: HTTP method

    scheme: URL scheme (http/https)

    host: Target hostname of the request. This is not neccessarily the
    directy upstream server (which could be another proxy), but it's always
    the target server we want to reach at the end. This attribute is either
    inferred from the request itself (absolute-form, authority-form) or from
    the connection metadata (e.g. the host in reverse proxy mode).

    port: Destination port

    path: Path portion of the URL (not present in authority-form)

    httpversion: HTTP version tuple, e.g. (1,1)

    headers: ODictCaseless object

    content: Content of the request, None, or CONTENT_MISSING if there
    is content associated, but not present. CONTENT_MISSING evaluates
    to False to make checking for the presence of content natural.

    form_in: The request form which mitmproxy has received. The following
    values are possible:

         - relative (GET /index.html, OPTIONS *) (covers origin form and
           asterisk form)
         - absolute (GET http://example.com:80/index.html)
         - authority-form (CONNECT example.com:443)
         Details: http://tools.ietf.org/html/draft-ietf-httpbis-p1-messaging-25#section-5.3

    form_out: The request form which mitmproxy will send out to the
    destination

    timestamp_start: Timestamp indicating when request transmission started

    timestamp_end: Timestamp indicating when request transmission ended
"""
