#!/usr/bin/env python3
from pathlib import Path
import re
import sys

ROOT = Path("THEOREMS")
OK = True

req = [
    r"^Theorem\s+\d{3}\s+—\s+",
    r"^Status:",
    r"^License:",
    r"^Authors:",
]

for p in sorted(ROOT.glob("[0-9][0-9][0-9]-*/README.md")):
    txt = p.read_text(encoding="utf-8", errors="ignore")
    for pat in req:
        if not re.search(pat, txt, flags=re.MULTILINE):
            print(f"FAIL: {p} missing pattern: {pat}")
            OK = False

if not OK:
    sys.exit(2)

print("OK: theorem format sanity passed")
