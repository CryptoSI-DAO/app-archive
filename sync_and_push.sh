#!/bin/bash
export GITHUB_TOKEN=$(cat /proc/1/environ 2>/dev/null | tr '\0' '\n' | grep '^GITHUB_TOKEN=' | cut -d= -f2-)
cd /workspace/app-archive
python3 sync_data_json.py
