#!/usr/bin/env python3
"""Rebuild data.json from the live GitHub API (authenticated with GITHUB_TOKEN)."""
import json
import os
import urllib.request
import sys

REPO = "CryptoSI-DAO/app-ideas"
TOKEN = os.environ.get("GITHUB_TOKEN", "")
API_BASE = f"https://api.github.com/repos/{REPO}/contents/ideas"
RAW_BASE = f"https://raw.githubusercontent.com/{REPO}/main/ideas"

def gh_api(url):
    req = urllib.request.Request(url, headers={
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"token {TOKEN}",
        "User-Agent": "data-sync-script"
    })
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())

def fetch_md(path):
    url = f"{RAW_BASE}/{path}"
    req = urllib.request.Request(url, headers={
        "Authorization": f"token {TOKEN}",
        "User-Agent": "data-sync-script"
    })
    with urllib.request.urlopen(req) as resp:
        return resp.read().decode()

def main():
    structure = {}
    dirs = gh_api(API_BASE)

    for d in sorted(dirs, key=lambda x: x["name"]):
        if d["type"] != "dir":
            continue
        date_name = d["name"]
        print(f"Processing {date_name}...", file=sys.stderr)

        contents = gh_api(d["url"])
        entry = {"ideas": [], "has_summary": False}

        # Summary
        summary = next((f for f in contents if f["name"] == "daily-summary.md"), None)
        if summary:
            entry["has_summary"] = True
            entry["summaryContent"] = fetch_md(f"{date_name}/daily-summary.md")

        # Idea dirs
        idea_dirs = [c for c in contents if c["type"] == "dir" and c["name"].startswith(("00", "01", "02", "03"))]
        for idea_dir in sorted(idea_dirs, key=lambda x: x["name"]):
            idea_contents = gh_api(idea_dir["url"])
            files = {}
            for f in idea_contents:
                if f["name"].endswith(".md"):
                    files[f["name"]] = fetch_md(f"{date_name}/{idea_dir['name']}/{f['name']}")
            if files:
                entry["ideas"].append({"slug": idea_dir["name"], "files": files})

        structure[date_name] = entry

    out = {
        "generated": "2026-06-01",
        "repo": REPO,
        "dates": structure
    }

    # Write to file
    paths = [
        "/workspace/app-archive/data.json",
        "/workspace/app-ideas/data.json"
    ]
    for p in paths:
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w") as f:
            json.dump(out, f, indent=2, ensure_ascii=False)
        print(f"Wrote {p}", file=sys.stderr)

    # Stats
    total_ideas = sum(len(v["ideas"]) for v in structure.values())
    print(f"Done: {len(structure)} days, {total_ideas} ideas", file=sys.stderr)

if __name__ == "__main__":
    main()
