#!/usr/bin/env python


import json
import sys
import urllib2
from datetime import datetime

def fmt_dt(ds):
    """Accepts wc3 time and prints utc date."""
    dt =  datetime.strptime(ds, "%Y-%m-%dT%H:%M:%SZ")
    return dt.strftime('%Y-%m-%d')


url = "https://api.github.com/users/%s/repos?type=owner&sort=created" % sys.argv[1]
repos = json.loads(
    urllib2.urlopen(url).read()
)

output = [(repo['name'], fmt_dt(repo['created_at']), repo['html_url']) for repo in repos]

biggest_title = max(map(lambda x: len(x[0]), output))

format_str = "%%-%ds\t%%s\t%%s" % (biggest_title)
print format_str
for attributes in output:
    print format_str % attributes
