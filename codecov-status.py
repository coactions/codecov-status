#!/usr/bin/env python3
"""Replacement for CodeCov GitHub App."""
import json
import os
import sys

from urllib.request import urlopen


if os.environ.get("GITHUB_REPOSITORY", "") and os.environ.get("GITHUB_REPOSITORY", ""):
    org, repo = os.environ.get("GITHUB_REPOSITORY", "").split("/")
    pr = os.environ.get("GITHUB_REF_NAME", "").split("/")[0]
else:
    print("Unable to find GITHUB_REPOSITORY or GITHUB_REF_NAME to determine current pull request.")
    sys.exit(1)

with urlopen(f"https://api.codecov.io/api/v2/github/{org}/repos/{repo}/pulls/{pr}/") as response:
    response_content = response.read().decode("utf-8")
    data = json.loads(response_content)
    head_cov = data["head_totals"]["coverage"]
    base_cov = data["base_totals"]["coverage"]
    delta_coverage = head_cov - base_cov

msg = f"{-delta_coverage:.2f}% ({base_cov:.2f}% on base -> {head_cov:.2f}% on head).\n"
msg += f"See https://app.codecov.io/gh/{org}/{repo}/pull/{pr} for details."
if delta_coverage < 0:
    print(f"Setting coverage check as failed due to coverage going down by {msg}")
    sys.exit(2)
print(f"Setting coverage check as passed due to coverage going up by {msg}")
