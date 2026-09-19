#!/usr/bin/env python3
"""verify_claims.py - the upgrade pass, made mechanical.

Fetches every claim's page in references/claims.json and reports whether
the quote is on it. Stdlib only. Run from a machine with open internet
(main-pc, the laptop); the sandbox that built the skill could reach almost
nothing, so every claim started life as "reported, not confirmed".

  python verify_claims.py                 # all claims
  python verify_claims.py --only is-      # ids starting with "is-"
  python verify_claims.py --report out.md # write a markdown table too

Result per claim:
  VERIFIED   page fetched and the expectation holds (quote present / absent)
  NOT FOUND  page fetched, no quote matched (wording changed, or the number
             differs - open the page and correct the reference)
  BLOCKED    fetch failed (proxy, 403, timeout) - try from another machine
Nothing is written to the references; the person does that, with the date.
"""
from __future__ import annotations

import argparse
import html
import json
import os
import re
import sys
import urllib.error
import urllib.request

UA = "Mozilla/5.0 (compatible; money-skill-verify/1.0; +https://github.com/PreissWorkshop/personal-os)"


def fetch(url: str, timeout: int = 25) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "en,is;q=0.8"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        raw = resp.read()
    for enc in ("utf-8", "latin-1"):
        try:
            return raw.decode(enc)
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8", errors="replace")


def to_text(page: str) -> str:
    page = re.sub(r"(?is)<(script|style|noscript).*?</\1>", " ", page)
    page = re.sub(r"(?s)<[^>]+>", " ", page)
    page = html.unescape(page)
    page = page.replace(" ", " ").replace(" ", " ").replace(" ", " ")
    return re.sub(r"\s+", " ", page).lower()


def norm(q: str) -> str:
    return re.sub(r"\s+", " ", q.replace(" ", " ")).lower()


def check(claim: dict, timeout: int) -> tuple[str, str]:
    try:
        page = fetch(claim["url"], timeout)
    except urllib.error.HTTPError as e:
        return "BLOCKED", f"HTTP {e.code}"
    except Exception as e:  # noqa: BLE001 - any transport failure is BLOCKED
        return "BLOCKED", type(e).__name__
    # visible text first; the raw page second, so a quote that lives in a
    # meta description or an attribute still counts
    text = to_text(page) + " " + re.sub(r"\s+", " ", html.unescape(page)).lower()
    hits = [q for q in claim["quotes"] if norm(q) in text]
    if claim.get("expect", "present") == "absent":
        return ("VERIFIED", "absent as expected") if not hits else ("NOT FOUND", f"present: {hits[0]!r}")
    return ("VERIFIED", f"found {hits[0]!r}") if hits else ("NOT FOUND", "no quote on page")


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--claims", default=os.path.join(os.path.dirname(__file__), "..", "references", "claims.json"))
    p.add_argument("--only", default="", help="only ids starting with this prefix")
    p.add_argument("--timeout", type=int, default=25)
    p.add_argument("--report", default="", help="write a markdown table to this path")
    a = p.parse_args(argv)
    claims = json.load(open(a.claims, encoding="utf-8"))["claims"]
    claims = [c for c in claims if c["id"].startswith(a.only)]
    rows = []
    counts = {"VERIFIED": 0, "NOT FOUND": 0, "BLOCKED": 0}
    for c in claims:
        status, detail = check(c, a.timeout)
        counts[status] += 1
        tag = " (control)" if c.get("control") else ""
        print(f"{status:9} {c['id']:24} {detail:28} {c['file']}{tag}")
        rows.append((status, c["id"], c["file"], c["claim"], c["url"], detail))
    print(f"\n{counts['VERIFIED']} verified, {counts['NOT FOUND']} not found, {counts['BLOCKED']} blocked, of {len(claims)}")
    if a.report:
        with open(a.report, "w", encoding="utf-8") as fh:
            fh.write("| status | id | file | claim | detail |\n|---|---|---|---|---|\n")
            for status, cid, f, claim, url, detail in rows:
                fh.write(f"| {status} | {cid} | {f} | [{claim}]({url}) | {detail} |\n")
        print(f"report: {a.report}")
    return 0 if counts["NOT FOUND"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
