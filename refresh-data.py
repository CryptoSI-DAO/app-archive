#!/usr/bin/env python3
"""
refresh-data.py — Regenerate data.json from the app-ideas GitHub repo.

Usage:
  python3 refresh-data.py

Requirements:
  pip install requests

This clones (or pulls) the app-ideas repo and rebuilds data.json
so the archive site always has the latest ideas.
"""

import os
import json
import subprocess
import sys
from datetime import datetime

REPO_URL = "https://github.com/CryptoSI-DAO/app-ideas.git"
REPO_DIR = "/tmp/app-ideas-repo"
OUTPUT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data.json")


def clone_or_pull():
    if os.path.isdir(os.path.join(REPO_DIR, ".git")):
        print("Pulling latest changes...")
        subprocess.run(["git", "-C", REPO_DIR, "pull", "--quiet"], check=True)
    else:
        print("Cloning repo...")
        subprocess.run(["git", "clone", "--depth", "1", REPO_URL, REPO_DIR], check=True)


def build_data():
    ideas_dir = os.path.join(REPO_DIR, "ideas")
    if not os.path.isdir(ideas_dir):
        print("ERROR: ideas/ directory not found in repo", file=sys.stderr)
        sys.exit(1)

    structure = {}
    for date_dir in sorted(os.listdir(ideas_dir)):
        date_path = os.path.join(ideas_dir, date_dir)
        if not os.path.isdir(date_path):
            continue

        entry = {"ideas": [], "has_summary": False}

        summary_path = os.path.join(date_path, "daily-summary.md")
        if os.path.exists(summary_path):
            entry["has_summary"] = True
            with open(summary_path) as f:
                entry["summaryContent"] = f.read()

        for item in sorted(os.listdir(date_path)):
            item_path = os.path.join(date_path, item)
            if not os.path.isdir(item_path):
                continue
            files = {}
            for fname in sorted(os.listdir(item_path)):
                fpath = os.path.join(item_path, fname)
                if os.path.isfile(fpath) and fname.endswith(".md"):
                    with open(fpath) as f:
                        files[fname] = f.read()
            if files:
                entry["ideas"].append({"slug": item, "files": files})

        structure[date_dir] = entry

    output = {
        "generated": datetime.utcnow().strftime("%Y-%m-%d"),
        "repo": "CryptoSI-DAO/app-ideas",
        "dates": structure,
    }

    with open(OUTPUT_PATH, "w") as f:
        json.dump(output, f, indent=2)

    total = sum(len(d["ideas"]) for d in structure.values())
    print(f"✅ data.json updated: {len(structure)} dates, {total} ideas")


if __name__ == "__main__":
    clone_or_pull()
    build_data()
