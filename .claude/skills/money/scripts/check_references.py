#!/usr/bin/env python3
"""Sanity checks for the money skill's references. Run before committing.

  python scripts/check_references.py            # from the skill root or anywhere

Checks (stdlib only):
  1. every Markdown table row in references/*.md has the header's cell count
  2. references/claims.json parses; ids unique; each claim has id, file, url,
     quotes, expect; the file exists; expect is "present" or "absent"
  3. every [V ...] label that is not the legacy "[V]" or "[V: ..." form
     carries a YYYY-MM-DD date (warning only)
Exit 1 on a failure in 1 or 2, else 0.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REFS = ROOT / "references"


def check_tables() -> list[str]:
    problems = []
    for f in sorted(REFS.glob("*.md")):
        lines = f.read_text(encoding="utf-8").splitlines()
        i = 0
        while i < len(lines):
            if lines[i].startswith("|") and i + 1 < len(lines) and re.match(r"^\|[\s:|-]+\|$", lines[i + 1]):
                n = lines[i].count("|")
                j = i + 2
                while j < len(lines) and lines[j].startswith("|"):
                    if lines[j].count("|") != n:
                        problems.append(f"{f.name}:{j + 1}: {lines[j].count('|')} pipes, header has {n}")
                    j += 1
                i = j
            else:
                i += 1
    return problems


def check_claims() -> list[str]:
    problems = []
    p = REFS / "claims.json"
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except Exception as e:  # noqa: BLE001
        return [f"claims.json does not parse: {e}"]
    claims = data["claims"] if isinstance(data, dict) and "claims" in data else data
    seen = set()
    for c in claims:
        cid = c.get("id", "<no id>")
        if cid in seen:
            problems.append(f"claims.json: duplicate id {cid}")
        seen.add(cid)
        for k in ("id", "file", "url", "quotes", "expect"):
            if k not in c:
                problems.append(f"claims.json {cid}: missing {k}")
        if c.get("expect") not in ("present", "absent"):
            problems.append(f"claims.json {cid}: expect must be present or absent")
        if not isinstance(c.get("quotes"), list) or not c.get("quotes"):
            problems.append(f"claims.json {cid}: quotes must be a non-empty list")
        if "file" in c and not (REFS / c["file"]).exists():
            problems.append(f"claims.json {cid}: file {c['file']} not in references/")
    return problems


def check_labels() -> list[str]:
    warnings = []
    pat = re.compile(r"\[V(?P<rest>[^\]]*)\]")
    for f in sorted(REFS.glob("*.md")):
        for n, line in enumerate(f.read_text(encoding="utf-8").splitlines(), 1):
            for m in pat.finditer(line):
                rest = m.group("rest")
                if rest == "" or rest.startswith(":") or re.search(r"\d{4}-\d{2}-\d{2}", rest):
                    continue
                warnings.append(f"{f.name}:{n}: [V{rest}] has no date")
    return warnings


def main() -> int:
    failures = check_tables() + check_claims()
    warnings = check_labels()
    for w in warnings:
        print("WARN ", w)
    for p in failures:
        print("FAIL ", p)
    print(f"check_references: {len(failures)} failure(s), {len(warnings)} warning(s)")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
