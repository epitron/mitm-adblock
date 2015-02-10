#!/usr/bin/env python2
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

from libmproxy.script import concurrent
from libmproxy.protocol.http import HTTPResponse
from netlib.odict import ODictCaseless
from time import time


class History:
  """ A history of loaded URLs, with an associated time """

  def __init__(self, timeout=3*60):
    self.hist    = {}
    self.timeout = timeout

  def should_skip(self, url):
    """ Did we recently load this page? """

    last_fetch = self.hist.get(url, 0)
    elapsed    = time() - last_fetch

    if elapsed > self.timeout:
      self.hist[url] = time()
      return False
    else:
      return True


history = History()

@concurrent
def request(context, flow):
  req = flow.request

  if history.should_skip(req.url):
    context.log("skipping: %s" % req.url)

    resp = HTTPResponse((1,1), 304, "NOT MODIFIED", ODictCaseless(), None)

    flow.reply(resp)


if __name__ == '__main__':
  from time import sleep
  history = History(1)
  print history.should_skip("http://google.com")
  print history.should_skip("http://google.com")
  print history.should_skip("http://google.com")
  sleep(2)
  print history.should_skip("http://google.com")
  print history.should_skip("http://google.com")
  print history.should_skip("http://google.com")

