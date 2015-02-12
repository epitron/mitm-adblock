#!/usr/bin/env python2

from libmproxy import flow
from datetime import datetime
import re, sys, os, json
from IPython import embed

def dot():
  sys.stdout.write(".")
  sys.stdout.flush()

for arg in sys.argv[1:]:
  print "-"*50
  print "Processing:", arg
  print "="*50
  print

  stream  = flow.FlowReader(open(arg)).stream()
  matcher = re.compile(r"instapaper\.com/api/(1\.1/bookmarks|list2)")

  for f in stream:
    req = f.request
    res = f.response

    dot()

    if matcher.search(req.url):
      res.decode()
      if len(res.content) <= 1:
        continue

      t = datetime.fromtimestamp(req.timestamp_start)
      outfile = t.strftime('insta/list-%Y-%m-%d_%H:%M:%S.json')

      print
      print "* [{time}] {url}".format(time=t, url=req.url)
      print "  |_ writing:", outfile

      with open(outfile, "w") as f:
        parsed = json.loads(res.content)
        json.dump(parsed, f, indent=2)

  print
  print
