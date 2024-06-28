#!/usr/bin/env python3

import json
import sys
import urllib.request
from datetime import datetime

def fmt_dt(ds):
    """Accepts ISO 8601 time and prints UTC date."""
    dt = datetime.strptime(ds, "%Y-%m-%dT%H:%M:%SZ")
    return dt.strftime('%Y-%m-%d')

def get_repos(username):
    """Fetches the list of repositories for a given GitHub username, handling pagination."""
    repos = []
    page = 1
    while True:
        url = f"https://api.github.com/users/{username}/repos?type=owner&sort=created&per_page=100&page={page}"
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode())
            if not data:
                break
            repos.extend(data)
            page += 1
    return repos

def filter_owned_repos(repos, username):
    """Filters repositories to include only those owned by the given username and excludes forks."""
    owned_repos = [repo for repo in repos if repo['owner']['login'] == username and not repo['fork']]
    return owned_repos

def create_exhibit_c(repos):
    """Constructs an Exhibit C with repository details."""
    exhibit_c = []
    for repo in repos:
        title = repo['name']
        date = fmt_dt(repo['created_at'])
        url = repo['html_url']
        exhibit_c.append((title, date, url))
    return exhibit_c

def print_exhibit_c(exhibit_c):
    """Prints the Exhibit C details."""
    if not exhibit_c:
        print("No repositories found.")
        return

    # Determine the column widths
    col_widths = [max(len(str(item[i])) for item in exhibit_c) for i in range(3)]
    col_widths = [max(col_widths[i], len(header)) for i, header in enumerate(["Repository Name", "Creation Date", "URL"])]

    # Print the header
    header = "{:<{w0}}\t{:<{w1}}\t{:<{w2}}".format("Repository Name", "Creation Date", "URL", w0=col_widths[0], w1=col_widths[1], w2=col_widths[2])
    print(header)
    print('-' * (sum(col_widths) + 2 * len(col_widths)))

    # Print each row
    for title, date, url in exhibit_c:
        print("{:<{w0}}\t{:<{w1}}\t{:<{w2}}".format(title, date, url, w0=col_widths[0], w1=col_widths[1], w2=col_widths[2]))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: script.py <github_username>")
        sys.exit(1)

    username = sys.argv[1]
    repos = get_repos(username)
    owned_repos = filter_owned_repos(repos, username)
    exhibit_c = create_exhibit_c(owned_repos)
    print_exhibit_c(exhibit_c)
