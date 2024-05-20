#!/usr/bin/env python3
"""Replacement for CodeCov GitHub App."""
import datetime
import json
import os
import sys

import time
from urllib.request import urlopen

DELAY = 5
MAX_RETRIES = 12
# 5s, 10s, 15s, 20s,...
MIN_AGE_IN_SECONDS = 10

if __name__ == "__main__":

    start_time = datetime.datetime.now(tz=datetime.UTC) - datetime.timedelta(seconds=2)
    if os.environ.get("GITHUB_REPOSITORY", "") and os.environ.get(
        "GITHUB_REPOSITORY", ""
    ):
        org, repo = os.environ.get("GITHUB_REPOSITORY", "").split("/")
        pr = os.environ.get("GITHUB_REF_NAME", "").split("/")[0]
    else:
        print(
            "::warning::GITHUB_REPOSITORY and GITHUB_REF_NAME are needed to determine current pull request."
        )
        sys.exit(0)

    if not pr.isnumeric():
        print(
            "::warning::Codecov.io status check skipped because a pull request was not detected."
        )
        sys.exit(0)

    retries = 0
    sleep = DELAY
    while retries < MAX_RETRIES:
        time.sleep(sleep)
        url = f"https://api.codecov.io/api/v2/github/{org}/repos/{repo}/pulls/{pr}/"
        print(f"Getting codecov.io status from {url}")
        with urlopen(url) as response:
            response_content = response.read().decode("utf-8")
            data = json.loads(response_content)
            print(data, file=sys.stdout)
            base_cov = 0.0
            head_cov = 0.0
            updatestamp = datetime.datetime.fromisoformat(data["updatestamp"])
            if data["base_totals"] is not None:
                base_cov = data["base_totals"]["coverage"]
            if data["head_totals"] is not None:
                head_cov = data["head_totals"]["coverage"]
            delta_coverage = head_cov - base_cov
        if updatestamp > start_time:
            break
        retries += 1
        sleep = DELAY * (retries + 1)
        print(
            f"::notice::Codecov API returned previous stats, we will retry the request in {sleep} seconds."
        )

    msg = f"{abs(delta_coverage):.2f}% ({base_cov:.2f}% on base -> {head_cov:.2f}% on head).\n"
    msg += f"See https://app.codecov.io/gh/{org}/{repo}/pull/{pr} for details."
    if delta_coverage < 0:
        print(
            f"::error::Setting coverage check as failed due to coverage going down by {msg}"
        )
        sys.exit(2)
    print(
        f"::notice::Setting coverage check as passed due to coverage going up by {msg}"
    )
