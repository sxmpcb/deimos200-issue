#!/usr/bin/env python3
"""Create one GitHub issue per entry in docs/defect-log.md.

Prerequisites
-------------
    brew install gh
    gh auth login

Usage
-----
    python3 scripts/create_issues.py --dry-run   # preview
    python3 scripts/create_issues.py             # create

The script is idempotent: issues whose title already exists are skipped.
"""

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

REPO = "sxmpcb/deimos200-issue"
DOC = Path(__file__).resolve().parent.parent / "docs" / "defect-log.md"

LABEL_COLORS = {
    "bug": ("d73a4a", "Something is not working"),
    "safety": ("b60205", "Safety relevant - escalate immediately"),
    "need-more-info": ("d876e3", "More information required"),
    "P0": ("b60205", "Severity P0 - blocker"),
    "P1": ("d93f0b", "Severity P1 - critical"),
    "P2": ("fbca04", "Severity P2 - normal"),
    "P3": ("0e8a16", "Severity P3 - minor"),
}
DEFAULT_LABEL = ("1d76db", "")


def parse():
    text = DOC.read_text(encoding="utf-8")
    parts = re.split(r"^## (\d+)\s*$", text, flags=re.M)
    issues = []
    for i in range(1, len(parts), 2):
        num, block = parts[i], parts[i + 1]
        title_m = re.search(r"\*\*Title:\*\* `([^`]+)`", block)
        if not title_m:
            continue
        labels_m = re.search(r"^\*\*Labels:\*\*\s*(.+)$", block, flags=re.M)
        prio_m = re.search(r"\*\*Priority:\*\*\s*(P[0-3])", block)
        fw_m = re.search(r"\*\*Firmware:\*\*\s*(\S+)", block)

        labels = re.findall(r"`([^`]+)`", labels_m.group(1)) if labels_m else []
        if prio_m and prio_m.group(1) not in labels:
            labels.append(prio_m.group(1))

        keep = [
            line for line in block.splitlines()
            if not re.match(r"\*\*(Title|Labels|Priority):\*\*", line)
        ]
        body = "\n".join(keep).strip()
        meta = (
            f"Firmware: {fw_m.group(1) if fw_m else 'n/a'}  \n"
            f"Priority: {prio_m.group(1) if prio_m else 'n/a'}  \n"
            f"Source: `mars abnormal.xlsx` row {num}\n\n---\n\n"
        )
        issues.append({
            "num": num,
            "title": title_m.group(1),
            "labels": labels,
            "body": meta + body,
        })
    return issues


def gh(*args, **kwargs):
    return subprocess.run(["gh", *args], text=True, capture_output=True, **kwargs)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    if not shutil.which("gh") and not args.dry_run:
        sys.exit("gh not found. Install it first: brew install gh && gh auth login")

    issues = parse()
    print(f"parsed {len(issues)} issues from {DOC.relative_to(DOC.parents[1])}")

    existing = set()
    if not args.dry_run:
        r = gh("issue", "list", "--repo", REPO, "--state", "all",
               "--limit", "200", "--json", "title")
        if r.returncode != 0:
            sys.exit(f"gh issue list failed:\n{r.stderr}")
        existing = {t["title"] for t in json.loads(r.stdout)}

        wanted = sorted({l for i in issues for l in i["labels"]})
        for name in wanted:
            color, desc = LABEL_COLORS.get(name, DEFAULT_LABEL)
            gh("label", "create", name, "--repo", REPO,
               "--color", color, "--description", desc, "--force")

    for it in issues:
        if it["title"] in existing:
            print(f"  skip   {it['title']}")
            continue
        if args.dry_run:
            print(f"  create {it['title']}  [{', '.join(it['labels'])}]")
            continue
        r = gh("issue", "create", "--repo", REPO,
               "--title", it["title"],
               "--body-file", "-",
               "--label", ",".join(it["labels"]),
               input=it["body"])
        if r.returncode == 0:
            print(f"  created {r.stdout.strip()}")
        else:
            print(f"  FAILED  {it['title']}\n{r.stderr}")


if __name__ == "__main__":
    main()
