#!/usr/bin/python


import sys
from github2.client import Github

github = Github()


repos = github.repos.list(sys.argv[1])

output = [(repo.name, repo.created_at.date(), repo.url) for repo in repos]

biggest_title = max(map(lambda x: len(x[0]), output))

format_str = "%%-%ds\t%%s\t%%s" % (biggest_title)
for attributes in output:
    print format_str % attributes
