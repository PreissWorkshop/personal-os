#!/usr/bin/env python3
"""Distressed Icelandic property: forced sales, from the official sources.

A derelict building never appears on an estate agent's website, because nobody
is selling it. It becomes visible when a creditor forces a sale, and that has to
be advertised in Logbirtingabladid, the official Legal Gazette, at least four
weeks before the first hearing. That notice is the earliest public sighting of a
distressed property, and this reads it.

Two sources, both public and free:

  the Legal Gazette, whose whole run of issues is downloadable as PDF from
  files.logbirtingablad.is with no login, and

  the sheriffs' live auction list, served by an open API at island.is, which is
  the only reliable place to see a continuation auction, since those are usually
  notified by registered letter rather than in the Gazette.

On privacy. The Gazette prints the name of the debtor, who is often a private
individual, and the site states that copying or distributing its content is not
permitted because of data protection. So this tool reads the notices for the
person running it and prints only the property, the municipality, the property
number, the creditor asking for the sale and the amount. It never prints the
name of a private debtor. Do not republish what it shows you.

Usage:
  python iceland_distressed.py --near 270 271 276 112 113 --issues 40
  python iceland_distressed.py --muni Mosfellsb Kjosar --issues 60
  python iceland_distressed.py --live-only

The forced-sale process, so the dates mean something (Act 90/1991):
  the Gazette notice runs at least four weeks before the first hearing (art 20),
  the first auction is held at the sheriff's office (art 26),
  the continuation auction is at the property itself within four weeks, and
  whoever occupies it must let bidders in to inspect (arts 35 and 36),
  and on the deed being issued, charges ranking below the money fall away (art 56).
"""

import argparse
import datetime as dt
import json
import os
import re
import subprocess
import sys
import urllib.request

GAZETTE = "https://files.logbirtingablad.is/adverts/issues/{year}/lbl-{n}-{year}.pdf"
ISLAND_API = "https://island.is/api/graphql"
UA = "Mozilla/5.0"

MONTHS = {"janúar": 1, "febrúar": 2, "mars": 3, "apríl": 4, "maí": 5, "júní": 6,
          "júlí": 7, "ágúst": 8, "september": 9, "október": 10, "nóvember": 11,
          "desember": 12}


def cache_dir(d):
    os.makedirs(d, exist_ok=True)
    return d


def fetch(url, dest=None, data=None, headers=None):
    req = urllib.request.Request(url, data=data,
                                 headers={"User-Agent": UA, **(headers or {})})
    with urllib.request.urlopen(req, timeout=60) as r:
        body = r.read()
    if dest:
        open(dest, "wb").write(body)
    return body


def pdf_text(path):
    txt = path[:-4] + ".txt"
    if os.path.exists(txt):
        return open(txt, encoding="utf-8", errors="replace").read()
    try:
        # -enc UTF-8 matters: without it pdftotext emits Latin-1 here and every
        # Icelandic character in the notices is destroyed.
        subprocess.run(["pdftotext", "-layout", "-enc", "UTF-8", path, txt],
                       check=True, capture_output=True)
    except (OSError, subprocess.CalledProcessError):
        try:
            import pypdf
            pages = pypdf.PdfReader(path).pages
            open(txt, "w", encoding="utf-8").write(
                "\n".join(p.extract_text() or "" for p in pages))
        except Exception as e:                      # noqa: BLE001
            print(f"   cannot read {os.path.basename(path)}: {e}", file=sys.stderr)
            return ""
    return open(txt, encoding="utf-8", errors="replace").read()


def parse_sitting_date(header):
    """'... Hlidasmara 1, 1. oktober 2026 kl. 10:00 ...' -> a date."""
    m = re.search(r"(\d{1,2})\.\s*([a-záðéíóúýþæö]+)\s+(\d{4})\s*kl\.\s*(\d{1,2}[:.]\d{2})",
                  header, re.I)
    if not m:
        return None, None
    day, mon, year, time = m.groups()
    if mon.lower() not in MONTHS:
        return None, None
    return dt.date(int(year), MONTHS[mon.lower()], int(day)), time.replace(".", ":")


def _clean(x):
    """Strip the page furniture pdftotext drags in from headers and footers."""
    x = re.sub(r"\d*\s*Lögbirtingablað.*", "", x)
    x = re.sub(r"Nr\.\s*\d+/\d{4}.*", "", x)
    x = re.sub(r"Útgáfud\..*", "", x)
    # Offices format differently; some end every field with a comma.
    return " ".join(x.split()).strip().rstrip(",")


# The Gazette writes these labels with an optional plural in brackets, for
# example "Gerðarbeiðandi (-beiðendur):", so the bracket has to be optional.
_L = r"\s*(?:\([^)]*\))?\s*:\s*"
FIELDS = {"muni": None,
          "fnr": r"Fastanr\.?" + _L + r"(.+)",
          "petitioner": r"Gerðarbeiðandi" + _L + r"(.+)",
          "amount": r"Fjárhæðir krafna í kr\.?" + _L + r"([\d.\s]+)"}


def parse_issue(text):
    """Pull every forced-sale entry out of one issue, one record at a time.

    The fields sit on consecutive lines under each 'Heiti eignar:', so each
    record is read within its own short window. A single regex across the whole
    issue runs past the end of a record and picks up the next one's creditor.
    The debtor's line is deliberately never read.
    """
    out = []
    sittings = []            # (position in text, date, time, office, address)
    for m in re.finditer(r"Nauðungarsala\s*[-–]\s*(.+)", text):
        head = text[m.start():m.start() + 900]
        when, at = parse_sitting_date(head)
        mw = re.search(r"embættisins\s+(.{3,60}?),\s*\d{1,2}\.", head)
        sittings.append((m.start(), when, at, _clean(m.group(1)),
                         _clean(mw.group(1)) if mw else ""))

    for m in re.finditer(r"Heiti eignar:\s*(.+)", text):
        window = text[m.end():m.end() + 500]
        lines = [_clean(l) for l in window.splitlines()]
        lines = [l for l in lines if l][:7]
        rec = {"property": _clean(m.group(1)), "muni": "", "fnr": "",
               "petitioner": "", "amount": None}
        for l in lines:
            if l.startswith("Gerðarþoli"):          # the debtor: skipped on purpose
                continue
            hit = False
            for key, pat in FIELDS.items():
                if pat and re.match(pat, l):
                    v = re.match(pat, l).group(1).strip()
                    if key == "amount":
                        v = v.replace(".", "").replace(" ", "")
                        rec["amount"] = int(v) if v.isdigit() else None
                    else:
                        rec[key] = v
                    hit = True
                    break
            if not hit and not rec["muni"] and not rec["fnr"] and ":" not in l:
                rec["muni"] = l                     # the bare line under the name
        # attach the sitting this record falls under
        prior = [x for x in sittings if x[0] < m.start()]
        _, when, at, office, where = prior[-1] if prior else (0, None, None, "", "")
        rec.update({"date": when, "time": at, "office": office, "where": where})
        if rec["fnr"]:
            out.append(rec)
    return out


def live_auctions():
    q = json.dumps({"query": "query{getSyslumennAuctions{office location "
                             "auctionType lotName lotId lotType auctionDate "
                             "auctionTime petitioners}}"}).encode()
    try:
        d = json.loads(fetch(ISLAND_API, data=q,
                             headers={"Content-Type": "application/json"}))
        return d.get("data", {}).get("getSyslumennAuctions") or []
    except Exception as e:                          # noqa: BLE001
        print(f"live auction list unavailable: {e}", file=sys.stderr)
        return []


def isk(n):
    return f"{n:,}".replace(",", ".") if isinstance(n, int) else "?"


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--near", nargs="*", default=[],
                   help="postcodes to highlight, e.g. 270 271 112")
    p.add_argument("--muni", nargs="*", default=[],
                   help="municipality name fragments, e.g. Mosfellsb Kjosar")
    p.add_argument("--issues", type=int, default=30,
                   help="how many recent Gazette issues to read (default 30)")
    p.add_argument("--year", type=int, default=dt.date.today().year)
    p.add_argument("--cache", default=os.path.join(os.path.expanduser("~"),
                                                   ".cache", "lbl"))
    p.add_argument("--live-only", action="store_true",
                   help="skip the Gazette, just show the sheriffs' live list")
    p.add_argument("--all", action="store_true",
                   help="show everything, not only what is still ahead")
    a = p.parse_args(argv)

    today = dt.date.today()

    print("SHERIFFS' LIVE AUCTION LIST")
    rows = live_auctions()
    ahead = [r for r in rows if "lokið" not in (r.get("auctionType") or "")]
    for r in ahead:
        lot = (r.get("lotName") or "").strip()
        hot = "  <<<" if any(n in lot for n in a.near + a.muni) else ""
        print(f"   {(r.get('auctionDate') or '')[:10]:<12} {r.get('auctionTime') or '':<6}"
              f"{(r.get('auctionType') or ''):<18}{lot[:44]:<46}{hot}")
    print(f"   {len(rows)} cases listed, {len(ahead)} not yet sold\n")
    if a.live_only:
        return 0

    d = cache_dir(a.cache)
    print(f"LEGAL GAZETTE, last {a.issues} issues of {a.year}")
    # Find the newest issue number by walking back from an optimistic guess.
    newest = None
    n = min(400, (today.timetuple().tm_yday * 170) // 265 + 12)
    while n > 0 and newest is None:
        try:
            urllib.request.urlopen(urllib.request.Request(
                GAZETTE.format(year=a.year, n=n), headers={"User-Agent": UA},
                method="HEAD"), timeout=30)
            newest = n
        except Exception:                           # noqa: BLE001
            n -= 1
    if newest is None:
        print("   no issues reachable")
        return 1
    print(f"   newest issue is {newest}\n")

    found = []
    for i in range(newest, max(0, newest - a.issues), -1):
        path = os.path.join(d, f"lbl-{i}-{a.year}.pdf")
        if not os.path.exists(path):
            try:
                fetch(GAZETTE.format(year=a.year, n=i), path)
            except Exception:                       # noqa: BLE001
                continue
        found.extend(parse_issue(pdf_text(path)))

    def wanted(e):
        if not a.near and not a.muni:
            return True
        hay = f"{e['muni']} {e['property']}"
        return any(x.lower() in hay.lower() for x in a.near + a.muni)

    hits = [e for e in found if wanted(e)]
    if not a.all:
        hits = [e for e in hits if e["date"] and e["date"] >= today]
    hits.sort(key=lambda e: (e["date"] or dt.date.max))

    print(f"   {len(found)} forced-sale entries read, {len(hits)} matching"
          + ("" if a.all else " and still ahead"))
    if hits:
        print(f"\n   {'sitting':<12}{'property':<30}{'municipality':<24}"
              f"{'claim':>16}  creditor")
        for e in hits:
            print(f"   {str(e['date']):<12}{e['property'][:29]:<30}"
                  f"{e['muni'][:23]:<24}{isk(e['amount']):>16}  "
                  f"{e['petitioner'][:34]}")
        print("\n   debtors' names are in the notices but are deliberately not shown;")
        print("   the Gazette restricts redistribution of its content")
    print("\n   a notice runs at least four weeks before the sitting, so this is")
    print("   the earliest public sighting of a property in trouble")
    return 0


if __name__ == "__main__":
    sys.exit(main())
