#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "PROOFPACK" / "MANIFEST.json"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    if not MANIFEST.exists():
        print(f"Missing {MANIFEST}. Run: python tools/make_manifest.py", file=sys.stderr)
        return 2

    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if data.get("schema") != "vireon_proofpack_manifest_v1":
        print("Bad manifest schema.", file=sys.stderr)
        return 2

    files = data.get("files", [])
    if not isinstance(files, list):
        print("Bad manifest format.", file=sys.stderr)
        return 2

    for entry in files:
        rel = entry["path"]
        expected = entry["sha256"]
        p = ROOT / rel
        if not p.exists():
            print(f"Missing file listed in manifest: {rel}", file=sys.stderr)
            return 2
        got = sha256_file(p)
        if got != expected:
            print(f"Hash mismatch for {rel}\n expected={expected}\n got={got}", file=sys.stderr)
            return 2

    print(f"[verify_manifest] OK: {len(files)} files verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
