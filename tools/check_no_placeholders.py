#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# We allow placeholders inside the template directory only.
ALLOW_TEMPLATE_DIR = ROOT / "THEOREMS" / "000_TEMPLATE_MONUMENT_ENTRY"

# Any of these strings appearing in a "real" entry is a fail.
BANNED_SNIPPETS = [
    "TEMPLATE",
    "Replace this block",
    "Write a complete proof here",
    "References (Template)",
    "Proof (Template)",
    "Theorem (Template)",
]

# Files we scan (simple, effective)
SCAN_EXTS = {".md", ".tex", ".txt", ".yml", ".yaml", ".py"}

def is_under(p: Path, parent: Path) -> bool:
    try:
        p.resolve().relative_to(parent.resolve())
        return True
    except Exception:
        return False

def main() -> int:
    failures = []

    for p in ROOT.rglob("*"):
        if not p.is_file():
            continue
        if p.suffix.lower() not in SCAN_EXTS:
            continue

        # Skip .git and other common noise
        if any(part in {".git", ".github"} for part in p.parts):
            # We DO want to scan workflow files too, so don't skip .github.
            pass

        # Allow placeholders in the template directory only
        if is_under(p, ALLOW_TEMPLATE_DIR):
            continue

        # Only enforce inside THEOREMS/ for now (keeps it clean)
        if not is_under(p, ROOT / "THEOREMS"):
            continue

        text = p.read_text(encoding="utf-8", errors="ignore")
        for s in BANNED_SNIPPETS:
            if s in text:
                failures.append((p.relative_to(ROOT).as_posix(), s))

    if failures:
        print("FAIL: placeholder/template text found in real entries:\n")
        for rel, snippet in failures:
            print(f"- {rel}  (matched: {snippet!r})")
        print("\nFix: remove placeholder text or keep it only under THEOREMS/000_TEMPLATE_MONUMENT_ENTRY/")
        return 2

    print("OK: no placeholders found outside template directory.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
