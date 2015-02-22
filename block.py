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

import re2
from libmproxy.script import concurrent
from libmproxy.protocol.http import HTTPResponse
from netlib.odict import ODictCaseless
from adblockparser import AdblockRules

def combined(filenames):
  for filename in filenames:
    with open(filename) as file:
      for line in file:
        yield line


def load_rules(blocklists=None):
  if blocklists is None:
    import glob
    blocklists = glob.glob("lists/*")

  print blocklists

  # rules = AdblockRules( combined(blocklists), use_re2=True, max_mem=512*1024*1024, supported_options=['script', 'domain'] )
  # rules = AdblockRules( combined(blocklists), use_re2=True, supported_options=['script', 'domain', 'image', 'stylesheet', 'object'] )
  rules = AdblockRules( 
    combined(blocklists), 
    use_re2=True, 
    max_mem=512*1024*1024
    # supported_options=['script', 'domain', 'image', 'stylesheet', 'object'] 
  )

  return rules

def start(context, argv):
    """
        Called once on script startup, before any other events.
    """
    global rules

    context.log("* Loading adblock rules...")
    rules = load_rules()
    context.log("  |_ done!")

IMAGE_MATCHER = re2.compile(r"\.(png|jpe?g|gif)$")
SCRIPT_MATCHER = re2.compile(r"\.(js)$")
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

        resp = HTTPResponse((1,1), 404, "OK",
            ODictCaseless([["Content-Type", "text/html"]]),
            "A terrible ad has been removed!")

        flow.reply(resp)

# def response(context, flow):
#     """
#        Called when a server response has been received.
#     """
#     context.log("response")

# def error(context, flow):
#     """
#         Called when a flow error has occured, e.g. invalid server responses, or
#         interrupted connections. This is distinct from a valid server HTTP error
#         response, which is simply a response with an HTTP error code.
#     """
#     context.log("error on %s", flow)
