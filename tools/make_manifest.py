#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]
PROOFPACK = ROOT / "PROOFPACK"
MANIFEST = PROOFPACK / "MANIFEST.json"

EXCLUDE_DIRS = {".git", ".github", "__pycache__", ".pytest_cache", ".mypy_cache", ".venv", "dist", "build"}
EXCLUDE_FILES = {"PROOFPACK/MANIFEST.json"}  # don't hash the manifest into itself


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def list_files(root: Path) -> List[Path]:
    files: List[Path] = []
    for p in root.rglob("*"):
        if not p.is_file():
            continue
        rel = p.relative_to(root).as_posix()
        if any(part in EXCLUDE_DIRS for part in p.parts):
            continue
        if rel in EXCLUDE_FILES:
            continue
        files.append(p)
    files.sort(key=lambda x: x.relative_to(root).as_posix())
    return files


def canonical_json_bytes(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def atomic_write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    with tmp.open("wb") as f:
        f.write(data)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, path)


def main() -> int:
    PROOFPACK.mkdir(parents=True, exist_ok=True)

    entries: List[Dict[str, Any]] = []
    for p in list_files(ROOT):
        rel = p.relative_to(ROOT).as_posix()
        entries.append(
            {
                "path": rel,
                "sha256": sha256_file(p),
                "bytes": p.stat().st_size,
            }
        )

    manifest = {
        "schema": "vireon_proofpack_manifest_v1",
        "root": ROOT.name,
        "files": entries,
    }

    atomic_write(MANIFEST, canonical_json_bytes(manifest) + b"\n")
    print(f"[make_manifest] wrote {MANIFEST.relative_to(ROOT).as_posix()} with {len(entries)} entries")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
