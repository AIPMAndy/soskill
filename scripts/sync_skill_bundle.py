#!/usr/bin/env python3
"""Sync mirrored project files into the installable SoSkill bundle."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path
from typing import Iterable, Tuple


MIRRORED_PATHS: Tuple[Tuple[str, str], ...] = (
    ("scripts/fetch_skills.py", "skills/public/soskill/scripts/fetch_skills.py"),
    ("scripts/print_stats.py", "skills/public/soskill/scripts/print_stats.py"),
    ("scripts/organize_collections.py", "skills/public/soskill/scripts/organize_collections.py"),
    ("scripts/bootstrap_collections.py", "skills/public/soskill/scripts/bootstrap_collections.py"),
    ("scripts/audit_skills.py", "skills/public/soskill/scripts/audit_skills.py"),
    ("scripts/run_workflow.py", "skills/public/soskill/scripts/run_workflow.py"),
    ("config/sources.json", "skills/public/soskill/references/sources.json"),
    ("config/collections.seed.json", "skills/public/soskill/references/collections.seed.json"),
    ("docs/ARCHITECTURE.md", "skills/public/soskill/references/architecture.md"),
    ("docs/collections.md", "skills/public/soskill/references/collections.md"),
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Sync mirrored files into skills/public/soskill")
    parser.add_argument(
        "--repo-root",
        default="",
        help="Repository root (default: inferred from script location)",
    )
    parser.add_argument("--check", action="store_true", help="Only check drift; do not write files")
    return parser.parse_args()


def iter_pairs(repo_root: Path) -> Iterable[Tuple[Path, Path]]:
    for src_rel, dst_rel in MIRRORED_PATHS:
        yield repo_root / src_rel, repo_root / dst_rel


def same_content(src: Path, dst: Path) -> bool:
    if not dst.exists():
        return False
    return src.read_bytes() == dst.read_bytes()


def ensure_sources_exist(pairs: Iterable[Tuple[Path, Path]]) -> None:
    missing = [str(src) for src, _ in pairs if not src.exists()]
    if missing:
        joined = "\n".join(f"- {item}" for item in missing)
        raise SystemExit(f"Missing source files:\n{joined}")


def main() -> None:
    args = parse_args()
    repo_root = Path(args.repo_root).expanduser().resolve() if args.repo_root else Path(__file__).resolve().parent.parent
    pairs = list(iter_pairs(repo_root))
    ensure_sources_exist(pairs)

    drift = []
    for src, dst in pairs:
        if not same_content(src, dst):
            drift.append((src, dst))

    if args.check:
        if drift:
            print("[drift] mirrored files are out of sync:")
            for src, dst in drift:
                print(f"- {src.relative_to(repo_root)} -> {dst.relative_to(repo_root)}")
            raise SystemExit(1)
        print("[ok] mirrored files are in sync")
        return

    for src, dst in drift:
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        print(f"[sync] {src.relative_to(repo_root)} -> {dst.relative_to(repo_root)}")

    if not drift:
        print("[ok] nothing to sync")
        return

    print(f"[done] synced {len(drift)} mirrored file(s)")


if __name__ == "__main__":
    main()
