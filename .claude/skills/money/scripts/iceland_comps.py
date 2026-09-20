#!/usr/bin/env python3
"""Real recorded Icelandic property sales, queried from the public register.

The register (kaupskra) is every registered purchase agreement in Iceland,
published by Husnaedis- og mannvirkjastofnun (HMS) as a free CSV. Fasteignaskra
moved from Thjodskra to HMS in 2022, which is why it lives at hms.is and no
longer at skra.is.

Download it first (about 48 MB, no login):
  curl -sL -o kaupskra.csv "https://frs3o1zldvgn.objectstorage.eu-frankfurt-1.oci.customer-oci.com/n/frs3o1zldvgn/b/public_data_for_download/o/kaupskra.csv"

Then, for example:
  python iceland_comps.py --csv kaupskra.csv --postcode 108 --size 80 110 --months 12
  python iceland_comps.py --csv kaupskra.csv --postcode 105 --built 1960 1985 --list 15
  python iceland_comps.py --csv kaupskra.csv --street "Hofsvallagata"

Five traps in this file, all handled here and all worth knowing:
  * KAUPVERD, FASTEIGNAMAT and BRUNABOTAMAT are in THOUSANDS of krona.
  * ONOTHAEFUR_SAMNINGUR = 0 means the contract IS usable. The flag is
    inverted from what its name suggests, and the unusable rows include
    whole-block bulk transfers that would wreck any average.
  * FULLBUID = 0 is an unfinished new build sold as a shell.
  * One contract can cover several properties; those rows are dropped.
  * EINFLM is the registered unit's own area. A separately registered garage
    is its own row, so a flat with an outside garage looks dearer per square
    metre than one whose garage sits inside the unit area.

HMS applies the first three of those filters in its own public tool, and warns
that recent months are incomplete because registration lags by up to six weeks.
"""

import argparse
import csv
import datetime as dt
import os
import statistics
import sys
import unicodedata

THOUSANDS = ("KAUPVERD", "FASTEIGNAMAT", "FASTEIGNAMAT_GILDANDI",
             "FYRIRHUGAD_FASTEIGNAMAT", "BRUNABOTAMAT_GILDANDI")


def fold(s):
    """Fold accents and case so a plain ASCII argument matches Icelandic text.
    A terminal that cannot pass 'Fjolbyli' as typed should still find it."""
    s = (s or "").replace("ð", "d").replace("Ð", "D")
    s = s.replace("þ", "th").replace("Þ", "Th")
    s = unicodedata.normalize("NFKD", s)
    return "".join(c for c in s if not unicodedata.combining(c)).lower()


def money(x):
    return f"{round(x):,}".replace(",", ".")


def sniff_encoding(path):
    """The register is published as Latin-1, not UTF-8. Decoding it as UTF-8
    with replacement silently destroys every Icelandic character, which then
    makes a type or street filter match nothing at all."""
    head = open(path, "rb").read(200000)
    try:
        head.decode("utf-8")
        return "utf-8-sig"
    except UnicodeDecodeError:
        return "latin-1"


def load(path, usable_only=True):
    """Read the register, keep the clean single-property finished sales."""
    rows, by_doc = [], {}
    with open(path, "r", encoding=sniff_encoding(path), newline="") as fh:
        for r in csv.DictReader(fh, delimiter=";"):
            try:
                if usable_only:
                    if r["ONOTHAEFUR_SAMNINGUR"].strip() != "0":
                        continue
                    if r["FULLBUID"].strip() != "1":
                        continue
                area = float((r["EINFLM"] or "0").replace(",", "."))
                price = float((r["KAUPVERD"] or "0").replace(",", ".")) * 1000
                if area <= 0 or price <= 0:
                    continue
                r["_area"] = area
                r["_price"] = price
                r["_m2"] = price / area
                r["_mat"] = float((r["FASTEIGNAMAT_GILDANDI"] or "0").replace(",", ".")) * 1000
                r["_year"] = int(r["BYGGAR"] or 0)
                r["_date"] = (r["UTGDAG"] or "")[:10]
            except (ValueError, KeyError):
                continue
            rows.append(r)
            by_doc[r["SKJALANUMER"]] = by_doc.get(r["SKJALANUMER"], 0) + 1
    # One contract covering several properties says nothing about a unit price.
    return [r for r in rows if by_doc.get(r["SKJALANUMER"], 0) == 1]


def query(rows, postcodes=None, size=None, built=None, since=None,
          kind=None, street=None, rooms=None):
    out = []
    for r in rows:
        if postcodes and r["POSTNR"].strip() not in postcodes:
            continue
        if size and not (size[0] <= r["_area"] <= size[1]):
            continue
        if built and not (built[0] <= r["_year"] <= built[1]):
            continue
        if since and r["_date"] < since:
            continue
        if kind and fold(kind) not in fold(r["TEGUND"]):
            continue
        if street and fold(street) not in fold(r["HEIMILISFANG"]):
            continue
        if rooms and (r["FJHERB"] or "").strip() != str(rooms):
            continue
        out.append(r)
    return out


def quantile(values, q):
    if not values:
        return 0.0
    s = sorted(values)
    i = (len(s) - 1) * q
    lo, hi = int(i), min(int(i) + 1, len(s) - 1)
    return s[lo] + (s[hi] - s[lo]) * (i - lo)


def describe(hits, label):
    if not hits:
        print(f"{label}: no matching recorded sales")
        return None
    m2 = [h["_m2"] for h in hits]
    prices = [h["_price"] for h in hits]
    areas = [h["_area"] for h in hits]
    ratios = [h["_price"] / h["_mat"] for h in hits if h["_mat"] > 0]
    d = {"n": len(hits), "median_m2": statistics.median(m2), "mean_m2": statistics.mean(m2),
         "p25_m2": quantile(m2, 0.25), "p75_m2": quantile(m2, 0.75),
         "median_price": statistics.median(prices), "median_area": statistics.median(areas),
         "median_ratio": statistics.median(ratios) if ratios else 0.0,
         "first": min(h["_date"] for h in hits), "last": max(h["_date"] for h in hits)}
    print(f"{label}")
    print(f"  recorded sales      {d['n']}, contracts dated {d['first']} to {d['last']}")
    print(f"  price per m2        median {money(d['median_m2'])}  "
          f"(quarter of sales below {money(d['p25_m2'])}, quarter above {money(d['p75_m2'])})")
    print(f"  typical sale        {money(d['median_price'])} for {d['median_area']:.1f} m2")
    if d["median_ratio"]:
        print(f"  price vs official   median {d['median_ratio']:.3f} x fasteignamat")
    return d


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--csv", required=True, help="path to kaupskra.csv")
    p.add_argument("--postcode", nargs="+", help="one or more postcodes, e.g. 108 109")
    p.add_argument("--size", nargs=2, type=float, metavar=("MIN", "MAX"), help="square metres")
    p.add_argument("--built", nargs=2, type=int, metavar=("FROM", "TO"), help="year built")
    p.add_argument("--rooms", type=int, help="number of rooms (FJHERB)")
    p.add_argument("--kind", help="Fjolbyli, Serbyli, Einbyli (matched loosely)")
    p.add_argument("--street", help="match part of the address")
    p.add_argument("--months", type=int, default=12, help="look back this many months (default 12)")
    p.add_argument("--list", type=int, default=0, help="also print this many recent sales")
    p.add_argument("--split-built", action="store_true",
                   help="break the result down by era built, which is the closest public proxy for condition")
    a = p.parse_args(argv)

    if not os.path.exists(a.csv):
        sys.exit(f"register not found at {a.csv}; the download command is in this file's header")

    since = (dt.date.today() - dt.timedelta(days=int(a.months * 30.44))).isoformat()
    rows = load(a.csv)
    pcs = set(a.postcode) if a.postcode else None
    size = (a.size[0], a.size[1]) if a.size else None
    built = (a.built[0], a.built[1]) if a.built else None

    bits = []
    if pcs:
        bits.append("postcode " + "/".join(sorted(pcs)))
    if size:
        bits.append(f"{size[0]:.0f}-{size[1]:.0f} m2")
    if built:
        bits.append(f"built {built[0]}-{built[1]}")
    if a.rooms:
        bits.append(f"{a.rooms} rooms")
    if a.kind:
        bits.append(a.kind)
    if a.street:
        bits.append(a.street)
    bits.append(f"last {a.months} months")
    label = ", ".join(bits)

    hits = query(rows, pcs, size, built, since, a.kind, a.street, a.rooms)
    print(f"register: {len(rows)} usable single-property finished sales\n")
    describe(hits, label)

    if a.split_built and hits:
        print("\n  by era built (location is mixed in, so read it as a hint, not a discount)")
        eras = [(0, 1959), (1960, 1979), (1980, 1999), (2000, 2014), (2015, 2100)]
        for lo, hi in eras:
            sub = [h for h in hits if lo <= h["_year"] <= hi]
            if len(sub) >= 3:
                med = statistics.median([h["_m2"] for h in sub])
                print(f"    {lo if lo else 'pre'}-{hi if hi < 2100 else 'now':<5} "
                      f"n={len(sub):<4} median {money(med)} per m2")

    if a.list and hits:
        print(f"\n  most recent {min(a.list, len(hits))} sales")
        for h in sorted(hits, key=lambda x: x["_date"], reverse=True)[:a.list]:
            print(f"    {h['_date']}  {h['HEIMILISFANG'][:28]:<28} {h['POSTNR']:<5} "
                  f"{h['_area']:>6.1f} m2  {h['_year']}  {money(h['_price']):>14}  "
                  f"{money(h['_m2']):>10}/m2")

    print("\nrecent months are incomplete: registration lags by up to six weeks")
    return 0


if __name__ == "__main__":
    sys.exit(main())
