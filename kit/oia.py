#!/usr/bin/env python3
"""
OIA CLI, v0.1.

Single-file, stdlib-only (Python 3.10+). Installs the Outside-In Alignment
constitution and supporting files into any project so an LLM session run
in that directory inherits operator-side discipline.

Usage:
  oia init [PATH]          # install constitution + supporting files
  oia version              # print version
  oia eval --quick         # run a small benchmark sanity check (3 tasks)
  oia uninstall [PATH]     # remove OIA files from a project

By default, `oia init` writes:
  ./CLAUDE.md                       (alias to constitution, picked up by Claude Code)
  ./.oia/CONSTITUTION.md            (canonical copy)
  ./.oia/version                    (version marker)
  ./.oia/README.md                  (one-paragraph explanation)

Existing CLAUDE.md is preserved with a backup and merged-with-banner.
"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path
from datetime import datetime, timezone

VERSION = "0.3.0"
CONSTITUTION_FILENAME = "CONSTITUTION_v0.3.md"  # default to v0.3
CONSTITUTION_TARGET = "CONSTITUTION.md"
OIA_BANNER_TOP = "<!-- BEGIN OIA, Outside-In Alignment v{version} -->"
OIA_BANNER_BOTTOM = "<!-- END OIA -->"


# ---------------------------- helpers --------------------------------------- #


def find_constitution() -> Path:
    """Resolve the constitution file relative to this script's repo root."""
    here = Path(__file__).resolve().parent
    candidates = [
        here.parent / CONSTITUTION_FILENAME,
        here.parent / "CONSTITUTION_v0.2.md",
        here.parent / "CONSTITUTION_v0.1.md",
    ]
    for c in candidates:
        if c.exists():
            return c
    raise FileNotFoundError(
        f"Constitution file not found. Looked in: {[str(c) for c in candidates]}"
    )


def utcnow_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


# ---------------------------- commands -------------------------------------- #


def cmd_init(args: argparse.Namespace) -> int:
    target_dir = Path(args.path).resolve()
    if not target_dir.exists():
        print(f"error: {target_dir} does not exist", file=sys.stderr)
        return 2
    if not target_dir.is_dir():
        print(f"error: {target_dir} is not a directory", file=sys.stderr)
        return 2

    constitution_src = find_constitution()
    constitution_text = constitution_src.read_text(encoding="utf-8")

    oia_dir = target_dir / ".oia"
    oia_dir.mkdir(exist_ok=True)
    (oia_dir / CONSTITUTION_TARGET).write_text(constitution_text, encoding="utf-8")
    (oia_dir / "version").write_text(f"{VERSION}\n{utcnow_iso()}\n", encoding="utf-8")
    (oia_dir / "README.md").write_text(
        "# OIA, Outside-In Alignment, installed here\n\n"
        "This directory contains the operator-side constitution that disciplines\n"
        "LLM sessions running in this project. See CONSTITUTION.md for the\n"
        f"rule set. Installed via `oia init` at {utcnow_iso()}.\n\n"
        "Remove with: `oia uninstall .`\n",
        encoding="utf-8",
    )

    claude_md = target_dir / "CLAUDE.md"
    banner_top = OIA_BANNER_TOP.format(version=VERSION)
    banner_bottom = OIA_BANNER_BOTTOM
    payload = f"{banner_top}\n\n{constitution_text}\n\n{banner_bottom}\n"

    if claude_md.exists():
        existing = claude_md.read_text(encoding="utf-8")
        if banner_top in existing and banner_bottom in existing:
            # Replace previous OIA block in place.
            before = existing.split(banner_top)[0]
            after = existing.split(banner_bottom, 1)[1] if banner_bottom in existing else ""
            merged = before + payload + after.lstrip("\n")
            claude_md.write_text(merged, encoding="utf-8")
            print(f"updated OIA block in {claude_md}")
        else:
            backup = claude_md.with_suffix(".md.bak")
            shutil.copy2(claude_md, backup)
            claude_md.write_text(payload + "\n---\n\n" + existing, encoding="utf-8")
            print(f"prepended OIA block to {claude_md} (backup: {backup.name})")
    else:
        claude_md.write_text(payload, encoding="utf-8")
        print(f"created {claude_md}")

    print(f"installed OIA v{VERSION} into {target_dir}")
    print("  .oia/CONSTITUTION.md  canonical copy")
    print("  CLAUDE.md             picked up by Claude Code")
    print(f"\nNext: start a Claude Code session in {target_dir} and verify the constitution loads.")
    return 0


def cmd_version(args: argparse.Namespace) -> int:
    print(f"oia {VERSION}")
    src = find_constitution()
    print(f"using constitution: {src.name}")
    return 0


def cmd_eval(args: argparse.Namespace) -> int:
    import subprocess

    here = Path(__file__).resolve().parent
    harness = here / "run_benchmark.py"
    if not harness.exists():
        print(f"error: harness not found at {harness}", file=sys.stderr)
        return 2

    cmd = [sys.executable, str(harness)]
    if args.quick:
        cmd.append("--smoke")
    else:
        cmd.extend(["--full", "--n", str(args.n)])
    if args.model:
        cmd.extend(["--model", args.model])
    if args.judge_model:
        cmd.extend(["--judge-model", args.judge_model])
    if args.with_v03:
        cmd.append("--with-v03")

    print(f"running: {' '.join(cmd)}")
    return subprocess.call(cmd)


def cmd_uninstall(args: argparse.Namespace) -> int:
    target_dir = Path(args.path).resolve()
    oia_dir = target_dir / ".oia"
    claude_md = target_dir / "CLAUDE.md"
    removed = []

    if oia_dir.exists():
        shutil.rmtree(oia_dir)
        removed.append(".oia/")

    if claude_md.exists():
        text = claude_md.read_text(encoding="utf-8")
        for v in ("0.3.0", "0.2.0", "0.1.0"):
            top = OIA_BANNER_TOP.format(version=v)
            if top in text and OIA_BANNER_BOTTOM in text:
                before = text.split(top)[0]
                after = text.split(OIA_BANNER_BOTTOM, 1)[1].lstrip("\n")
                new_text = (before + after).strip() + "\n"
                if new_text.strip():
                    claude_md.write_text(new_text, encoding="utf-8")
                else:
                    claude_md.unlink()
                removed.append("CLAUDE.md (OIA block stripped)")
                break

    if removed:
        for r in removed:
            print(f"removed {r}")
    else:
        print("nothing to remove")
    return 0


# ---------------------------- main ------------------------------------------ #


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="oia", description="Outside-In Alignment CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    p_init = sub.add_parser("init", help="Install OIA constitution into a project")
    p_init.add_argument("path", nargs="?", default=".", help="Target project dir")
    p_init.set_defaults(func=cmd_init)

    p_version = sub.add_parser("version", help="Print version")
    p_version.set_defaults(func=cmd_version)

    p_eval = sub.add_parser("eval", help="Run the benchmark")
    p_eval.add_argument("--quick", action="store_true", help="Smoke test")
    p_eval.add_argument("--n", type=int, default=3)
    p_eval.add_argument("--model", default=None)
    p_eval.add_argument("--judge-model", default=None)
    p_eval.add_argument("--with-v03", action="store_true")
    p_eval.set_defaults(func=cmd_eval)

    p_un = sub.add_parser("uninstall", help="Remove OIA files from a project")
    p_un.add_argument("path", nargs="?", default=".", help="Target project dir")
    p_un.set_defaults(func=cmd_uninstall)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
