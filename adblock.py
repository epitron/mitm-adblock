from adblockparser import AdblockRules

def combined(filenames):
  for filename in filenames:
    with open(filename) as file:
      for line in file:
        yield line


def load_rules(blocklists=["easylist.txt", "easyprivacy.txt", "fanboy-annoyance.txt", "fanboy-social.txt"]):
  print "Loading rules:", blocklists

  # rules = AdblockRules( combined(blocklists), use_re2=True, max_mem=512*1024*1024, supported_options=['script', 'domain'] )
  rules = AdblockRules( combined(blocklists), use_re2=True, supported_options=['script', 'domain', 'image', 'stylesheet', 'object'] )
  # rules = AdblockRules( combined(blocklists), use_re2=True )

  return rules


if __name__ == '__main__':
  rules = load_rules(["easyprivacy.txt"])
  options = {"domain": "slashdot.org"}
  print rules.should_block("http://b.scorecardresearch.com/b?c1=7&c2=2000001&c3=1&rn=1ko0g1i&c7=http%3A%2F%2Fwww.ifls", options)
  