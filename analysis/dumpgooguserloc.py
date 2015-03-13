#!/usr/bin/env python2

from libmproxy import flow
from datetime import datetime
import re, sys, os


def dot():
  sys.stdout.write(".")
  sys.stdout.flush()

for arg in sys.argv[1:]:
  print "-"*50
  print "Processing:", arg
  print "="*50
  print

  stream  = flow.FlowReader(open(arg)).stream()
  matcher = re.compile(r"googleapis\.com/userlocation")

  for f in stream:
    req = f.request

    dot()

    if matcher.search(req.url) and len(req.content) > 0:

      t = datetime.fromtimestamp(req.timestamp_start)
      outfile = t.strftime('goog/userloc-%Y-%m-%d_%H:%M:%S.json')

      print
      print "* [{time}] {url}".format(time=t, url=req.url)
      print "  |_ writing:", outfile

      with open(outfile, "w") as f:
        f.write(req.content)

  print
  print
