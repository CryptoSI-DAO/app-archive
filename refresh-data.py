#!/usr/bin/env python3
"""
refresh-data.py — Regenerate data.json from the public app-ideas GitHub repo.

Usage:
  python3 refresh-data.py

No authentication needed — works with public repos via the GitHub API.
"""

import json
import urllib.request
import ssl
import os
from datetime import datetime

REPO = "CryptoSI-DAO/app-ideas"
API_BASE = f"https://api.github.com/repos/{REPO}/contents/ideas"
RAW_BASE = f"https://raw.githubusercontent.com/{REPO}/main/ideas"
OUTPUT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data.json")

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


def api_get(url):
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/vnd.github.v3+json",
    })
    with urllib.request.urlopen(req, context=ctx, timeout=15) as r:
        return json.loads(r.read().decode())


def raw_get(path):
    url = f"{RAW_BASE}/{path}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, context=ctx, timeout=15) as r:
        return r.read().decode()


def build():
    dates = api_get(API_BASE)
    structure = {}

    for d in dates:
        if d["type"] != "dir":
            continue
        date_name = d["name"]
        contents = api_get(d["url"])
        entry = {"ideas": [], "has_summary": False}

        summary = next((f for f in contents if f["name"] == "daily-summary.md"), None)
        if summary:
            entry["has_summary"] = True
            entry["summaryContent"] = raw_get(f"{date_name}/daily-summary.md")

        idea_dirs = sorted(
            [c for c in contents if c["type"] == "dir" and c["name"][:3].isdigit()],
            key=lambda x: x["name"],
        )

        for idea_dir in idea_dirs:
            idea_contents = api_get(idea_dir["url"])
            files = {}
            for f in sorted(idea_contents):
                if f["name"].endswith(".md"):
                    files[f["name"]] = raw_get(
                        f"{date_name}/{idea_dir['name']}/{f['name']}"
                    )
            if files:
                entry["ideas"].append({"slug": idea_dir["name"], "files": files})

        structure[date_name] = entry

    output = {
        "generated": datetime.utcnow().strftime("%Y-%m-%d"),
        "repo": REPO,
        "dates": structure,
    }

    with open(OUTPUT_PATH, "w") as f:
        json.dump(output, f, indent=2)

    total = sum(len(v["ideas"]) for v in structure.values())
    print(f"✅ data.json updated: {len(structure)} dates, {total} total ideas")


if __name__ == "__main__":
    build()
