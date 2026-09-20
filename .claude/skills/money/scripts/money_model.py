#!/usr/bin/env python3
"""money_model.py - stdlib-only calculators for the money skill.

Subcommands
  plan      read a private snapshot JSON and print the situation: income, burn,
            gap, runway, debt horizon, phase
  quick     the same situation from a few numbers on the command line - the
            ratio mode for when no snapshot exists yet
  debt      debt payoff - avalanche vs snowball vs minimums, indexation aware
  runway    months of cash at a given burn and income
  fi        FI number, years to FI, and the savings-rate table
  rate      freelance hourly / day rate from a target take-home income
  unit      subscription unit economics: LTV, CAC payback, customers needed
  score     rank business options with a weighted rubric
  job       one job's contribution and effective hourly rate against the
            target rate - the business view of a quote, not the quote itself
  forecast  month-by-month cash for the next N months; names the first
            month that goes negative
  selftest  run the built-in checks

No third-party packages, no network, no personal data inside this file.
Numbers in, numbers out; the judgement stays with the person reading them.
Percent inputs are written as percents (12.5 means 12.5 %), never as
fractions, because that is how people copy them off a bank statement.

Examples
  python money_model.py plan --snapshot ~/.preiss/finance/finance-snapshot.json
  python money_model.py quick --income 700000 --essential 450000 --cash 0 --debt-total 2100000 --rate 18
  python money_model.py debt --debts debts.json --budget 250000 --strategy compare
  python money_model.py runway --cash 900000 --burn 650000 --income 300000
  python money_model.py fi --spend 4800000 --assets 0 --savings 2400000
  python money_model.py rate --net 9000000 --tax 38 --overhead 1200000
  python money_model.py unit --price 29 --margin 85 --churn 4 --cac 120 --target-mrr 8000
  python money_model.py score --options options.json
  python money_model.py job --price 1200000 --materials 420000 --hours 60 --vat 24 --target-hourly 14000
  python money_model.py forecast --cash 300000 --income 700000,650000,900000 --burn 620000 --debt 150000 --months 12
"""

from __future__ import annotations

import argparse
import json
import math
import os
import sys
from typing import Any

MAX_MONTHS = 600


# ---------------------------------------------------------------- helpers ---

def pct(x: float) -> float:
    """Percent (12.5) -> fraction (0.125)."""
    return x / 100.0


def money(x: float, cur: str = "") -> str:
    """1234567.8 -> '1.234.568' (Icelandic style thousands separator)."""
    s = f"{round(x):,}".replace(",", ".")
    return f"{s} {cur}".strip()


def load_json(path: str) -> Any:
    with open(os.path.expanduser(path), "r", encoding="utf-8") as fh:
        return json.load(fh)


def table(rows: list[list[str]], header: list[str] | None = None) -> str:
    rows = [[str(c) for c in r] for r in rows]
    if header:
        rows = [header] + rows
    widths = [max(len(r[i]) for r in rows) for i in range(len(rows[0]))]
    out = []
    for n, r in enumerate(rows):
        out.append("  ".join(c.ljust(widths[i]) for i, c in enumerate(r)))
        if header and n == 0:
            out.append("  ".join("-" * w for w in widths))
    return "\n".join(out)


# ------------------------------------------------------------------- debt ---

def simulate_debts(debts: list[dict], budget: float, strategy: str = "avalanche",
                   max_months: int = MAX_MONTHS) -> dict:
    """Month-by-month payoff.

    debts: [{name, balance, apr (percent), min_payment, index_rate (percent,
    optional - the CPI indexation of an Icelandic verdtryggt loan, added to
    the principal every month)}]
    budget: total money per month for all debts (minimums + extra).
    strategy: avalanche (highest apr+index first), snowball (smallest balance
    first), minimums (no extra, budget ignored).

    The extra always goes to one focus debt; when it is paid off its minimum
    rolls over to the next. Both strategies roll over - only the order differs.
    """
    ds = []
    assumed = []
    for d in debts:
        m = float(d.get("min_payment", 0) or 0)
        if m <= 0:
            # people rarely know their minimums; 3 % of the balance is a
            # documented placeholder, printed as an assumption by the caller
            m = max(1000.0, 0.03 * float(d["balance"]))
            assumed.append(d["name"])
        ds.append({
            "name": d["name"],
            "balance": float(d["balance"]),
            "apr": pct(float(d.get("apr", 0))),
            "idx": pct(float(d.get("index_rate", 0))),
            "min": m,
        })
    mins_total = sum(d["min"] for d in ds)
    if strategy == "minimums":
        budget = mins_total
    if budget + 1e-9 < mins_total:
        raise ValueError(f"budget {budget:.0f} is below the sum of minimum payments {mins_total:.0f}")

    if strategy == "avalanche":
        order = sorted(range(len(ds)), key=lambda i: -(ds[i]["apr"] + ds[i]["idx"]))
    elif strategy in ("snowball",):
        order = sorted(range(len(ds)), key=lambda i: ds[i]["balance"])
    else:  # minimums - order is irrelevant, no extra
        order = list(range(len(ds)))

    total_interest = total_index = total_paid = 0.0
    payoff_month: dict[str, int] = {}
    series = []
    warnings = []
    month = 0
    while any(d["balance"] > 0.005 for d in ds) and month < max_months:
        month += 1
        # accrue
        for d in ds:
            if d["balance"] <= 0:
                continue
            i = d["balance"] * d["apr"] / 12.0
            x = d["balance"] * d["idx"] / 12.0
            d["balance"] += i + x
            total_interest += i
            total_index += x
        # minimums
        available = budget
        for d in ds:
            if d["balance"] <= 0:
                continue
            p = min(d["min"], d["balance"], available)
            d["balance"] -= p
            available -= p
            total_paid += p
        # extra to the focus debt(s) in order
        for i in order:
            d = ds[i]
            if available <= 0:
                break
            if d["balance"] <= 0:
                continue
            p = min(available, d["balance"])
            d["balance"] -= p
            available -= p
            total_paid += p
        for d in ds:
            if d["balance"] <= 0.005 and d["name"] not in payoff_month:
                payoff_month[d["name"]] = month
                d["balance"] = 0.0
        series.append(sum(d["balance"] for d in ds))
    finished = all(d["balance"] <= 0.005 for d in ds)
    if not finished:
        for d in ds:
            if d["balance"] > 0.005:
                warnings.append(f"{d['name']}: not paid off within {max_months} months - "
                                f"payment does not cover interest/indexation")
    return {
        "strategy": strategy,
        "months": month if finished else None,
        "total_interest": total_interest,
        "total_indexation": total_index,
        "total_paid": total_paid,
        "payoff_order": sorted(payoff_month.items(), key=lambda kv: kv[1]),
        "series": series,
        "warnings": warnings,
        "budget": budget,
        "assumed_minimums": assumed,
    }


def fmt_months(m: int | None) -> str:
    if m is None:
        return "never"
    return f"{m} mo ({m / 12:.1f} y)"


def cmd_debt(a: argparse.Namespace) -> int:
    debts = load_json(a.debts)
    if isinstance(debts, dict):
        debts = debts.get("debts", [])
    cur = a.currency
    strategies = ["minimums", "avalanche", "snowball"] if a.strategy == "compare" else [a.strategy]
    results = []
    for s in strategies:
        try:
            results.append(simulate_debts(debts, a.budget, s))
        except ValueError as e:
            print(f"{s}: {e}")
    if not results:
        return 2
    print(f"Debts: {len(debts)}  total balance {money(sum(float(d['balance']) for d in debts), cur)}  "
          f"minimums {money(sum(float(d.get('min_payment', 0) or 0) for d in debts), cur)}/mo")
    if results[0]["assumed_minimums"]:
        print("ASSUMPTION: no minimum payment given for " + ", ".join(results[0]["assumed_minimums"])
              + " - 3% of balance assumed; replace with the statement figure")
    rows = []
    for r in results:
        rows.append([r["strategy"], money(r["budget"], cur) + "/mo", fmt_months(r["months"]),
                     money(r["total_interest"], cur), money(r["total_indexation"], cur),
                     money(r["total_paid"], cur)])
    print(table(rows, ["strategy", "budget", "debt-free in", "interest", "indexation", "paid"]))
    for r in results:
        if r["payoff_order"]:
            print(f"\n{r['strategy']} payoff order: " +
                  ", ".join(f"{n} (m{m})" for n, m in r["payoff_order"]))
        for w in r["warnings"]:
            print(f"  WARNING {w}")
    if len(results) >= 3 and results[1]["months"] and results[2]["months"]:
        av, sn = results[1], results[2]
        print(f"\navalanche saves {money(sn['total_interest'] - av['total_interest'], cur)} of interest "
              f"versus snowball and finishes {sn['months'] - av['months']} months earlier "
              f"(negative = snowball wins on that line).")
    return 0


# ----------------------------------------------------------------- runway ---

def runway_months(cash: float, burn: float, income: float = 0.0) -> float | None:
    net = burn - income
    if net <= 0:
        return None  # income covers burn: infinite runway
    return cash / net


def cmd_runway(a: argparse.Namespace) -> int:
    r = runway_months(a.cash, a.burn, a.income)
    cur = a.currency
    print(f"cash {money(a.cash, cur)}  burn {money(a.burn, cur)}/mo  income {money(a.income, cur)}/mo")
    if r is None:
        print(f"income covers burn; surplus {money(a.income - a.burn, cur)}/mo - runway is not the constraint")
    else:
        print(f"runway {r:.1f} months  (net burn {money(a.burn - a.income, cur)}/mo)")
        print(f"income needed to stop the bleed: {money(a.burn, cur)}/mo; "
              f"to bank a 3-month essential buffer in 12 months: {money(a.burn + 3 * a.burn / 12, cur)}/mo")
    return 0


# --------------------------------------------------------------------- fi ---

def fi_number(annual_spend: float, swr_pct: float = 4.0) -> float:
    return annual_spend / pct(swr_pct)


def years_to_fi(savings_per_year: float, current_assets: float, target: float,
                real_return_pct: float = 5.0) -> float:
    """Closed form of: assets*(1+r)^n + savings*((1+r)^n - 1)/r = target."""
    if current_assets >= target:
        return 0.0
    if savings_per_year <= 0:
        return math.inf
    r = pct(real_return_pct)
    if abs(r) < 1e-12:
        return (target - current_assets) / savings_per_year
    num = target * r + savings_per_year
    den = current_assets * r + savings_per_year
    if num <= 0 or den <= 0:
        return math.inf
    return math.log(num / den) / math.log(1 + r)


def savings_rate_table(real_return_pct: float = 5.0, swr_pct: float = 4.0) -> list[tuple[int, float]]:
    """Years to FI from zero assets for each savings rate of take-home pay."""
    out = []
    for s in (5, 10, 15, 20, 25, 30, 40, 50, 60, 70, 80):
        spend = 1 - s / 100.0
        target = fi_number(spend, swr_pct)
        out.append((s, years_to_fi(s / 100.0, 0.0, target, real_return_pct)))
    return out


def cmd_fi(a: argparse.Namespace) -> int:
    cur = a.currency
    target = fi_number(a.spend, a.swr)
    yrs = years_to_fi(a.savings, a.assets, target, a.real_return)
    print(f"annual spend {money(a.spend, cur)} -> FI number at {a.swr:g}% withdrawal: {money(target, cur)} "
          f"({100 / a.swr:.0f}x spend)")
    if a.savings > 0 or a.assets >= target:
        rate = a.savings / (a.savings + a.spend) * 100 if (a.savings + a.spend) > 0 else 0
        print(f"savings {money(a.savings, cur)}/yr (savings rate {rate:.0f}% of take-home), "
              f"assets {money(a.assets, cur)}, real return {a.real_return:g}%")
        print("years to FI: " + ("not reachable" if math.isinf(yrs) else f"{yrs:.1f}"))
    print("\nsavings rate -> years to FI from zero (real return "
          f"{a.real_return:g}%, withdrawal {a.swr:g}%):")
    rows = [[f"{s}%", f"{y:.0f}"] for s, y in savings_rate_table(a.real_return, a.swr)]
    print(table(rows, ["savings rate", "years"]))
    return 0


# ------------------------------------------------------------------- rate ---

def freelance_rate(net_target: float, tax_pct: float, overhead: float, hours_per_week: float,
                   weeks: float, utilization_pct: float) -> dict:
    profit_needed = net_target / (1 - pct(tax_pct)) if tax_pct < 100 else math.inf
    revenue = profit_needed + overhead
    billable = hours_per_week * weeks * pct(utilization_pct)
    hourly = revenue / billable if billable > 0 else math.inf
    return {"profit": profit_needed, "revenue": revenue, "billable_hours": billable,
            "hourly": hourly, "day": hourly * 8, "month": revenue / 12}


def cmd_rate(a: argparse.Namespace) -> int:
    cur = a.currency
    r = freelance_rate(a.net, a.tax, a.overhead, a.hours, a.weeks, a.utilization)
    print(f"take-home target {money(a.net, cur)}/yr, effective tax {a.tax:g}%"
          + (" (ASSUMPTION: default placeholder, not his real rate)" if a.tax == 35.0 else "")
          + f", overhead {money(a.overhead, cur)}/yr")
    print(f"-> profit before tax {money(r['profit'], cur)}, revenue needed {money(r['revenue'], cur)}/yr "
          f"= {money(r['month'], cur)}/mo")
    print(f"billable hours: {a.hours:g} h/wk x {a.weeks:g} wk x {a.utilization:g}% = {r['billable_hours']:.0f} h/yr")
    print(f"hourly {money(r['hourly'], cur)}   day (8 h) {money(r['day'], cur)}")
    print("sanity: every hour you sell below this rate is paid for by an unpaid hour somewhere else.")
    return 0


# ------------------------------------------------------------------- unit ---

def unit_economics(price: float, margin_pct: float, churn_pct: float, cac: float,
                   target_mrr: float) -> dict:
    gm = pct(margin_pct)
    churn = pct(churn_pct)
    contribution = price * gm
    ltv = contribution / churn if churn > 0 else math.inf
    payback = cac / contribution if contribution > 0 else math.inf
    customers = target_mrr / price if price > 0 else math.inf
    replacements = customers * churn
    return {"contribution": contribution, "ltv": ltv, "ltv_cac": (ltv / cac if cac > 0 else math.inf),
            "payback_months": payback, "customers": customers, "monthly_replacements": replacements,
            "lifetime_months": (1 / churn if churn > 0 else math.inf)}


def cmd_unit(a: argparse.Namespace) -> int:
    cur = a.currency
    u = unit_economics(a.price, a.margin, a.churn, a.cac, a.target_mrr)
    print(f"price {money(a.price, cur)}/mo, gross margin {a.margin:g}%, churn {a.churn:g}%/mo, CAC {money(a.cac, cur)}")
    print(f"contribution {money(u['contribution'], cur)}/mo per customer; average lifetime "
          f"{u['lifetime_months']:.0f} months; LTV {money(u['ltv'], cur)}; LTV/CAC {u['ltv_cac']:.1f}; "
          f"CAC payback {u['payback_months']:.1f} months")
    print(f"for {money(a.target_mrr, cur)} MRR you need {u['customers']:.0f} customers and must win "
          f"{u['monthly_replacements']:.1f} new ones every month just to stand still")
    if u["ltv_cac"] < 3:
        print("flag: LTV/CAC under 3 - acquisition is too expensive or churn too high for this price")
    if u["payback_months"] > 12:
        print("flag: payback over 12 months - cash-poor businesses cannot fund this growth")
    return 0


# ------------------------------------------------------------------ score ---

DEFAULT_CRITERIA = {
    # criterion: weight. 1-5 scores per option; 5 is always "better for a
    # debt-carrying solo builder with no capital".
    "cash_within_60_days": 5,
    "no_capital_needed": 4,
    "uses_existing_assets": 4,
    "recurring_revenue": 3,
    "b2b_customer": 3,
    "location_independent": 3,
    "market_reachable_in_english": 2,
    "defensible": 2,
    "energy_and_fit": 2,
}


def score_options(options: list[dict], criteria: dict[str, float] | None = None) -> list[dict]:
    crit = criteria or DEFAULT_CRITERIA
    wsum = sum(crit.values())
    out = []
    for o in options:
        sc = o.get("scores", {})
        total = 0.0
        missing = []
        for k, w in crit.items():
            if k in sc:
                total += float(sc[k]) * w
            else:
                missing.append(k)
        out.append({"name": o["name"], "score": total / (wsum * 5) * 100, "missing": missing,
                    "note": o.get("note", "")})
    return sorted(out, key=lambda r: -r["score"])


def cmd_score(a: argparse.Namespace) -> int:
    data = load_json(a.options)
    options = data.get("options", data) if isinstance(data, dict) else data
    criteria = data.get("criteria") if isinstance(data, dict) else None
    ranked = score_options(options, criteria)
    rows = [[f"{i + 1}", r["name"], f"{r['score']:.0f}/100",
             ("missing: " + ", ".join(r["missing"])) if r["missing"] else r["note"]] for i, r in enumerate(ranked)]
    print(table(rows, ["#", "option", "score", "note"]))
    print("\nscore is weighted 1-5 per criterion; the rubric is a tie-breaker, not an oracle.")
    return 0


# ------------------------------------------------------------------- plan ---

def phase(gap: float, cash: float, essential: float, debt_total: float) -> str:
    """Phase labels used by SKILL.md. gap = income - full burn - minimum payments."""
    if gap < 0:
        return "0 STABILISE - the month loses money; cut, collect, sell hours"
    buffer_months = cash / essential if essential > 0 else math.inf
    if buffer_months < 1:
        return "1 CASH - positive month, no buffer; every surplus króna builds one month of essentials"
    if debt_total > 0 and buffer_months < 3:
        return ("2 BUFFER+KILL - one month is banked; any debt above ~15% gets the surplus now, "
                "the buffer grows to 3 months from windfalls or once nothing that expensive is left")
    if debt_total > 0:
        return "3 KILL DEBT - buffer done; surplus goes to the highest-rate debt, product work in fixed hours"
    return "4 COMPOUND - debt-free; invest the surplus, raise income with product/recurring revenue"


def cmd_plan(a: argparse.Namespace) -> int:
    snap = load_json(a.snapshot)
    return report_situation(snap, snap.get("currency", a.currency))


def cmd_quick(a: argparse.Namespace) -> int:
    """Ratio mode: a snapshot built from the command line, nothing stored."""
    debts = []
    if a.debt_total > 0:
        debts = [{"name": "all debts (one line)", "balance": a.debt_total, "apr": a.rate,
                  "min_payment": a.minimums if a.minimums > 0 else max(1000.0, 0.03 * a.debt_total)}]
    snap = {
        "as_of": "quick (nothing stored)", "currency": a.currency or "",
        "monthly_income": {"income": a.income},
        "monthly_burn": {"essential": a.essential, "full": a.full if a.full > 0 else a.essential},
        "cash": a.cash, "debts": debts, "debt_budget": a.debt_budget,
    }
    if a.debt_total > 0 and a.minimums <= 0:
        print("ASSUMPTION: minimum payments not given - 3% of the debt total assumed")
    if a.debt_total > 0:
        print(f"ASSUMPTION: all debt treated as one line at {a.rate:g}% - run `debt` with the real list for the order")
    return report_situation(snap, snap["currency"])


def report_situation(snap: dict, cur: str) -> int:
    income = snap.get("monthly_income", {})
    income_total = sum(float(v) for v in income.values()) if isinstance(income, dict) else float(income)
    burn = snap.get("monthly_burn", {})
    essential = float(burn.get("essential", 0))
    full = float(burn.get("full", essential))
    cash = float(snap.get("cash", 0))
    debts = snap.get("debts", [])
    debt_total = sum(float(d.get("balance", 0)) for d in debts)
    mins = sum(float(d.get("min_payment", 0)) for d in debts)
    w_apr = (sum(float(d.get("balance", 0)) * (float(d.get("apr", 0)) + float(d.get("index_rate", 0)))
                 for d in debts) / debt_total) if debt_total > 0 else 0.0
    gap = income_total - full - mins
    essential_gap = income_total - essential - mins

    print(f"snapshot as of {snap.get('as_of', '?')}  ({cur})")
    if income_total == 0 and essential == 0 and cash == 0 and debt_total == 0:
        print("the snapshot is empty - copy assets/finance-snapshot.template.json outside the repo, "
              "fill in the real numbers, and run plan again")
        return 1
    print(table([
        ["income", money(income_total, cur) + "/mo", "  ".join(f"{k} {money(float(v), cur)}" for k, v in income.items()) if isinstance(income, dict) else ""],
        ["burn essential", money(essential, cur) + "/mo", "rent, food, insurance, transport, minimum obligations"],
        ["burn full", money(full, cur) + "/mo", "everything actually spent"],
        ["debt minimums", money(mins, cur) + "/mo", f"{len(debts)} debts, {money(debt_total, cur)} total, weighted rate {w_apr:.1f}%"],
        ["gap (full)", money(gap, cur) + "/mo", "income - full burn - minimums"],
        ["gap (essential)", money(essential_gap, cur) + "/mo", "income - essential burn - minimums"],
        ["cash", money(cash, cur), f"{(cash / essential):.1f} months of essentials" if essential > 0 else ""],
    ]))
    r = runway_months(cash, full + mins, income_total)
    print("\nrunway at full burn: " + ("not the constraint (positive month)" if r is None else f"{r:.1f} months"))
    if debts:
        budget = float(snap.get("debt_budget", 0)) or mins
        try:
            base = simulate_debts(debts, mins, "minimums")
            print(f"debt-free at minimums only: {fmt_months(base['months'])}, interest {money(base['total_interest'], cur)}"
                  + (f", indexation {money(base['total_indexation'], cur)}" if base['total_indexation'] else ""))
            for w in base["warnings"]:
                print(f"  WARNING {w}")
            if budget > mins:
                av = simulate_debts(debts, budget, "avalanche")
                print(f"debt-free at {money(budget, cur)}/mo avalanche: {fmt_months(av['months'])}, "
                      f"interest {money(av['total_interest'], cur)}; order: "
                      + ", ".join(f"{n} (m{m})" for n, m in av["payoff_order"]))
        except ValueError as e:
            print(f"debt simulation: {e}")
    print(f"\nphase: {phase(gap, cash, essential, debt_total)}")
    if gap < 0:
        print(f"income to add (or cost to cut) to break even at full burn: {money(-gap, cur)}/mo; "
              f"at essential burn: {money(max(0.0, -essential_gap), cur)}/mo")
    else:
        months_to_buffer = (3 * essential - cash) / gap if gap > 0 and cash < 3 * essential else 0
        print(f"3-month essential buffer ({money(3 * essential, cur)}) at the current gap: "
              + ("already there" if months_to_buffer <= 0 else f"{months_to_buffer:.1f} months"))
    return 0


# -------------------------------------------------------------------- job ---

def job_economics(price: float, materials: float, hours: float, other: float = 0.0,
                  vat_pct: float = 0.0, target_hourly: float = 0.0) -> dict:
    """Contribution of one job. price is what the customer pays; if vat_pct > 0
    the price includes VAT and the net is used (VAT is never income)."""
    net = price / (1 + pct(vat_pct)) if vat_pct > 0 else price
    contribution = net - materials - other
    hourly = contribution / hours if hours > 0 else math.inf
    margin = contribution / net if net > 0 else 0.0
    shortfall = (target_hourly - hourly) * hours if target_hourly > 0 and hourly < target_hourly else 0.0
    return {"net": net, "contribution": contribution, "hourly": hourly, "margin": margin,
            "shortfall": shortfall, "break_even_hours": (contribution / target_hourly if target_hourly > 0 else math.inf)}


def cmd_job(a: argparse.Namespace) -> int:
    cur = a.currency
    j = job_economics(a.price, a.materials, a.hours, a.other, a.vat, a.target_hourly)
    print(f"price {money(a.price, cur)}" + (f" incl. {a.vat:g}% VAT -> net {money(j['net'], cur)}" if a.vat > 0 else "")
          + f"; materials {money(a.materials, cur)}; other {money(a.other, cur)}; {a.hours:g} h")
    print(f"contribution {money(j['contribution'], cur)} ({j['margin'] * 100:.0f}% of net) = {money(j['hourly'], cur)} per hour")
    if a.target_hourly > 0:
        if j["shortfall"] > 0:
            print(f"BELOW the target rate of {money(a.target_hourly, cur)}/h by {money(j['shortfall'], cur)} on this job; "
                  f"at the target it must take no more than {j['break_even_hours']:.0f} h, or the price rises, or the scope shrinks")
        else:
            print(f"above the target rate of {money(a.target_hourly, cur)}/h - take it if the month has the hours")
    print("rule: cut scope before cutting the rate; a job below the rate is paid for by an unpaid hour elsewhere")
    return 0


# ------------------------------------------------------------------- flip ---

def flip_economics(price: float, stamp_pct: float, fees_buy: float,
                   materials: float, sub_trades: float, hours: float, rate: float,
                   vat_pct: float, vat_refund_pct: float, contingency_pct: float,
                   fixed_price: bool, months: int, loan: float, loan_rate: float,
                   holding_monthly: float, sale: float, agent_pct: float,
                   agent_vat_pct: float, agent_fixed: float,
                   tax_pct: float, share_pct: float) -> dict:
    """One buy-renovate-resell deal, from the investor's side and the builder's.

    Every input is a number someone supplied; nothing here is a market fact.
    Interest is simple interest on the loan for the whole hold, which is how a
    short interest-only facility behaves; an amortising loan costs slightly less.
    """
    buy_costs = price * pct(stamp_pct) + fees_buy
    labour = hours * rate
    reno_base = materials + sub_trades + labour
    contingency = reno_base * pct(contingency_pct)
    # On a fixed price the overrun is the builder's, not the investor's.
    reno_to_investor = reno_base if fixed_price else reno_base + contingency
    builder_exposure = contingency if fixed_price else 0.0

    refund_base = labour + sub_trades
    vat_element = refund_base - refund_base / (1 + pct(vat_pct)) if vat_pct > 0 else 0.0
    vat_refund = vat_element * pct(vat_refund_pct)

    interest = loan * pct(loan_rate) * months / 12.0
    holding = holding_monthly * months
    total_in = price + buy_costs + reno_to_investor + interest + holding - vat_refund

    commission = sale * pct(agent_pct) * (1 + pct(agent_vat_pct))
    selling = commission + agent_fixed
    net_sale = sale - selling

    gross_gain = net_sale - total_in
    tax = max(0.0, gross_gain) * pct(tax_pct)
    net_gain = gross_gain - tax
    builder_share = max(0.0, net_gain) * pct(share_pct)
    investor_net = net_gain - builder_share

    cash_in = max(0.0, total_in - loan)
    roi = investor_net / cash_in if cash_in > 0 else math.inf
    annualised = roi * 12.0 / months if months > 0 and cash_in > 0 else math.inf

    # Sale price at which the investor's net is zero, holding costs as they are.
    denom = (1 - pct(agent_pct) * (1 + pct(agent_vat_pct)))
    break_even = (total_in + agent_fixed) / denom if denom > 0 else math.inf

    builder_total = labour + builder_share
    builder_hourly = builder_total / hours if hours > 0 else math.inf
    builder_hourly_worst = labour / (hours * (1 + pct(contingency_pct))) if hours > 0 else math.inf
    month_cost = loan * pct(loan_rate) / 12.0 + holding_monthly

    return {"buy_costs": buy_costs, "labour": labour, "reno_base": reno_base,
            "contingency": contingency, "reno_to_investor": reno_to_investor,
            "builder_exposure": builder_exposure, "vat_refund": vat_refund,
            "interest": interest, "holding": holding, "total_in": total_in,
            "commission": commission, "selling": selling, "net_sale": net_sale,
            "gross_gain": gross_gain, "tax": tax, "net_gain": net_gain,
            "builder_share": builder_share, "investor_net": investor_net,
            "cash_in": cash_in, "roi": roi, "annualised": annualised,
            "break_even": break_even, "builder_total": builder_total,
            "builder_hourly": builder_hourly, "builder_hourly_worst": builder_hourly_worst,
            "month_cost": month_cost}


def cmd_flip(a: argparse.Namespace) -> int:
    cur = a.currency
    f = flip_economics(a.price, a.stamp_pct, a.fees_buy, a.materials, a.sub_trades,
                       a.hours, a.rate, a.vat, a.vat_refund, a.contingency,
                       a.fixed_price, a.months, a.loan, a.loan_rate, a.holding,
                       a.sale, a.agent_pct, a.agent_vat, a.agent_fixed,
                       a.tax_pct, a.share_pct)

    print("MONEY IN")
    rows = [["purchase price", money(a.price, cur)],
            [f"buying costs ({a.stamp_pct:g}% stamp duty + fees)", money(f["buy_costs"], cur)],
            ["materials", money(a.materials, cur)],
            ["subcontracted trades", money(a.sub_trades, cur)],
            [f"builder's labour ({a.hours:g} h at {money(a.rate, cur)})", money(f["labour"], cur)]]
    if a.fixed_price:
        rows.append([f"contingency {a.contingency:g}% (builder carries it)", money(0, cur)])
    else:
        rows.append([f"contingency {a.contingency:g}% (investor carries it)", money(f["contingency"], cur)])
    rows += [[f"VAT refund on labour ({a.vat_refund:g}% of the VAT)", "-" + money(f["vat_refund"], cur)],
             [f"loan interest, {a.months} months at {a.loan_rate:g}%", money(f["interest"], cur)],
             [f"holding costs, {a.months} months", money(f["holding"], cur)],
             ["TOTAL INTO THE DEAL", money(f["total_in"], cur)]]
    print(table(rows))

    print("\nMONEY OUT")
    print(table([["sale price", money(a.sale, cur)],
                 [f"agent commission {a.agent_pct:g}% incl. {a.agent_vat:g}% VAT", "-" + money(f["commission"], cur)],
                 ["other selling costs", "-" + money(a.agent_fixed, cur)],
                 ["net from the sale", money(f["net_sale"], cur)]]))

    print("\nRESULT")
    print(table([["gain before tax", money(f["gross_gain"], cur)],
                 [f"tax at {a.tax_pct:g}%", "-" + money(f["tax"], cur)],
                 ["gain after tax", money(f["net_gain"], cur)],
                 [f"builder's share {a.share_pct:g}% of the gain", money(f["builder_share"], cur)],
                 ["investor keeps", money(f["investor_net"], cur)]]))

    print(f"\ninvestor's own cash in the deal {money(f['cash_in'], cur)}"
          + (f" (loan {money(a.loan, cur)})" if a.loan else " (no loan)"))
    if f["cash_in"] > 0:
        print(f"return on that cash {f['roi'] * 100:.1f}% over {a.months} months, "
              f"{f['annualised'] * 100:.1f}% a year at the same pace")
    print(f"break-even sale price {money(f['break_even'], cur)} - below this the investor loses money")
    print(f"every extra month unsold costs {money(f['month_cost'], cur)}")

    print(f"\nbuilder is paid {money(f['labour'], cur)} for the work"
          + (f" plus {money(f['builder_share'], cur)} share = {money(f['builder_total'], cur)}" if a.share_pct else "")
          + f", {money(f['builder_hourly'], cur)} an hour")
    if a.fixed_price:
        print(f"on a fixed price a {a.contingency:g}% overrun costs the builder {money(f['builder_exposure'], cur)}, "
              f"dropping the rate to {money(f['builder_hourly_worst'], cur)} an hour")

    print("\nIF IT GOES WORSE (investor's net after tax; materials and subcontractors over budget)")
    sale_steps = [0, -5, -10, -15]
    over_steps = [0, 20, 40]
    header = ["sale"] + [f"materials +{o}%" for o in over_steps]
    grid = []
    for s_adj in sale_steps:
        s_price = a.sale * (1 + pct(s_adj))
        row = [f"{s_adj:+d}% = {money(s_price, cur)}" if s_adj else f"as planned {money(s_price, cur)}"]
        for o in over_steps:
            g = flip_economics(a.price, a.stamp_pct, a.fees_buy, a.materials * (1 + pct(o)),
                               a.sub_trades * (1 + pct(o)), a.hours, a.rate, a.vat, a.vat_refund,
                               a.contingency, a.fixed_price, a.months, a.loan, a.loan_rate,
                               a.holding, s_price, a.agent_pct, a.agent_vat, a.agent_fixed,
                               a.tax_pct, a.share_pct)
            row.append(money(g["investor_net"], cur))
        grid.append(row)
    print(table(grid, header))
    print("\nevery figure above is an input someone supplied, not a market fact;"
          " label each one before it goes in front of anybody")
    return 0


# --------------------------------------------------------------- forecast ---

def forecast(cash: float, incomes: list[float], burn: float, debt: float, months: int) -> list[dict]:
    """Monthly cash path. incomes repeats its last value once exhausted."""
    rows = []
    for m in range(1, months + 1):
        inc = incomes[min(m - 1, len(incomes) - 1)] if incomes else 0.0
        cash = cash + inc - burn - debt
        rows.append({"month": m, "income": inc, "cash": cash})
    return rows


def cmd_forecast(a: argparse.Namespace) -> int:
    cur = a.currency
    incomes = [float(x) for x in a.income.split(",") if x.strip()]
    rows = forecast(a.cash, incomes, a.burn, a.debt, a.months)
    print(table([[str(r["month"]), money(r["income"], cur), money(a.burn + a.debt, cur), money(r["cash"], cur)] for r in rows],
                ["month", "income", "out (burn+debt)", "cash at end"]))
    neg = next((r for r in rows if r["cash"] < 0), None)
    low = min(rows, key=lambda r: r["cash"])
    if neg:
        print(f"\nCASH GOES NEGATIVE in month {neg['month']} - that is the deadline for new income or a cut; "
              f"lowest point {money(low['cash'], cur)} in month {low['month']}")
    else:
        print(f"\ncash stays positive; lowest point {money(low['cash'], cur)} in month {low['month']}")
    return 0


# --------------------------------------------------------------- selftest ---

def selftest() -> int:
    fails = 0

    def check(name: str, cond: bool, detail: str = "") -> None:
        nonlocal fails
        print(f"  {'ok  ' if cond else 'FAIL'} {name} {detail}")
        if not cond:
            fails += 1

    # FI closed form against a brute-force simulation
    def brute(s, a0, target, r):
        a, n = a0, 0
        while a < target and n < 500:
            a = a * (1 + r) + s
            n += 1
        return n

    for s, a0, spend, r in ((0.5, 0.0, 0.5, 0.05), (0.25, 0.0, 0.75, 0.05), (2.4e6, 0.0, 4.8e6, 0.05)):
        tgt = fi_number(spend, 4.0)
        cf = years_to_fi(s, a0, tgt, r * 100)
        br = brute(s, a0, tgt, r)
        check(f"fi closed form ~ brute (s={s}, spend={spend})", abs(cf - br) <= 1.0, f"{cf:.2f} vs {br}")
    tbl = dict(savings_rate_table(5.0, 4.0))
    check("50% savings rate -> ~17 years (MMM table says 17)", 16 <= tbl[50] <= 17.5, f"{tbl[50]:.1f}")
    check("10% savings rate -> ~51 years (MMM table says 51)", 49 <= tbl[10] <= 52, f"{tbl[10]:.1f}")
    check("75%+ savings rate -> under 8 years", tbl[80] < 8, f"{tbl[80]:.1f}")
    check("FI number = 25x spend at 4%", abs(fi_number(4.8e6, 4.0) - 120e6) < 1e-6)
    check("already FI -> 0 years", years_to_fi(1.0, 200.0, 100.0) == 0.0)
    check("no savings, not FI -> inf", math.isinf(years_to_fi(0.0, 10.0, 100.0)))

    # debt: single loan amortisation against the annuity formula
    bal, apr, n = 1_000_000.0, 12.0, 24
    r = pct(apr) / 12
    pay = bal * r / (1 - (1 + r) ** -n)
    res = simulate_debts([{"name": "a", "balance": bal, "apr": apr, "min_payment": pay}], pay, "minimums")
    check("annuity: 24 payments clear the loan", res["months"] == n, f"{res['months']}")
    check("annuity: total interest ~ n*pay - principal", abs(res["total_interest"] - (n * pay - bal)) < 5,
          f"{res['total_interest']:.0f} vs {n * pay - bal:.0f}")
    # avalanche never pays more interest than snowball, both finish with the same budget
    debts = [{"name": "card", "balance": 600_000, "apr": 24, "min_payment": 20_000},
             {"name": "car", "balance": 1_800_000, "apr": 9, "min_payment": 45_000},
             {"name": "small", "balance": 150_000, "apr": 15, "min_payment": 8_000}]
    av = simulate_debts(debts, 150_000, "avalanche")
    sn = simulate_debts(debts, 150_000, "snowball")
    mn = simulate_debts(debts, 0, "minimums")
    check("avalanche interest <= snowball interest", av["total_interest"] <= sn["total_interest"] + 1e-6,
          f"{av['total_interest']:.0f} vs {sn['total_interest']:.0f}")
    check("avalanche months <= snowball months", av["months"] <= sn["months"], f"{av['months']} vs {sn['months']}")
    check("extra budget beats minimums", av["months"] < mn["months"], f"{av['months']} vs {mn['months']}")
    check("avalanche focuses the 24% card first", av["payoff_order"][0][0] == "card")
    check("snowball focuses the smallest first", sn["payoff_order"][0][0] == "small")
    # indexation: a verdtryggt loan at 0% interest and 4% indexation still grows
    idx = simulate_debts([{"name": "ix", "balance": 1_000_000, "apr": 0, "index_rate": 4, "min_payment": 3_000}], 3_000, "minimums")
    check("indexation alone can outrun a small payment (warning raised)", idx["months"] is None and idx["warnings"])
    # missing minimums are assumed at 3% and reported
    am = simulate_debts([{"name": "x", "balance": 100_000, "apr": 20}], 5_000, "avalanche")
    check("missing minimum -> 3% assumed and flagged", am["assumed_minimums"] == ["x"] and am["months"])
    # budget below minimums is refused
    try:
        simulate_debts(debts, 10, "avalanche")
        check("budget below minimums raises", False)
    except ValueError:
        check("budget below minimums raises", True)

    # runway
    check("runway 900k cash, 650k burn, 300k income -> 2.57 months", abs(runway_months(900_000, 650_000, 300_000) - 900_000 / 350_000) < 1e-9)
    check("runway with covering income -> None", runway_months(1, 5, 10) is None)

    # rate
    fr = freelance_rate(9_000_000, 38, 1_200_000, 40, 46, 60)
    check("rate: profit grosses up the tax", abs(fr["profit"] - 9_000_000 / 0.62) < 1)
    check("rate: hourly = revenue / billable", abs(fr["hourly"] - fr["revenue"] / (40 * 46 * 0.6)) < 1e-6)

    # unit economics
    u = unit_economics(29, 85, 4, 120, 8000)
    check("unit: LTV = price*margin/churn", abs(u["ltv"] - 29 * 0.85 / 0.04) < 1e-6)
    check("unit: customers for target = target/price", abs(u["customers"] - 8000 / 29) < 1e-9)
    check("unit: payback = cac/contribution", abs(u["payback_months"] - 120 / (29 * 0.85)) < 1e-9)

    # score
    ranked = score_options([
        {"name": "A", "scores": {k: 5 for k in DEFAULT_CRITERIA}},
        {"name": "B", "scores": {k: 1 for k in DEFAULT_CRITERIA}},
    ])
    check("score: all-5 option scores 100 and ranks first", ranked[0]["name"] == "A" and abs(ranked[0]["score"] - 100) < 1e-9)
    check("score: all-1 option scores 20", abs(ranked[1]["score"] - 20) < 1e-9)

    # job and forecast
    j = job_economics(1_240_000, 400_000, 50, 40_000, 24, 12_000)
    check("job: VAT stripped from the price", abs(j["net"] - 1_000_000) < 1e-6)
    check("job: contribution = net - materials - other", abs(j["contribution"] - 560_000) < 1e-6)
    check("job: hourly = contribution / hours", abs(j["hourly"] - 11_200) < 1e-6)
    check("job: shortfall against the target rate", abs(j["shortfall"] - (12_000 - 11_200) * 50) < 1e-6)
    fc = forecast(100_000, [500_000, 500_000, 800_000], 460_000, 100_000, 6)
    first_neg = next((r["month"] for r in fc if r["cash"] < 0), None)
    check("forecast: first negative month is 2", first_neg == 2, f"{[round(r['cash']) for r in fc]}")
    check("forecast: last income repeats", fc[-1]["income"] == 800_000)

    fl = flip_economics(price=50_000_000, stamp_pct=0.8, fees_buy=100_000,
                        materials=5_000_000, sub_trades=2_000_000, hours=500, rate=10_000,
                        vat_pct=24, vat_refund_pct=0, contingency_pct=10, fixed_price=False,
                        months=6, loan=0, loan_rate=0, holding_monthly=0,
                        sale=70_000_000, agent_pct=0, agent_vat_pct=0, agent_fixed=0,
                        tax_pct=0, share_pct=0)
    check("flip: buying costs = stamp + fees", abs(fl["buy_costs"] - (400_000 + 100_000)) < 1e-6)
    check("flip: labour = hours x rate", abs(fl["labour"] - 5_000_000) < 1e-6)
    check("flip: contingency on the whole renovation", abs(fl["contingency"] - 1_200_000) < 1e-6)
    check("flip: total in adds up", abs(fl["total_in"] - (50_000_000 + 500_000 + 13_200_000)) < 1e-6)
    check("flip: gain is net sale less total in", abs(fl["gross_gain"] - (70_000_000 - fl["total_in"])) < 1e-6)
    flf = flip_economics(price=50_000_000, stamp_pct=0.8, fees_buy=100_000,
                         materials=5_000_000, sub_trades=2_000_000, hours=500, rate=10_000,
                         vat_pct=24, vat_refund_pct=60, contingency_pct=10, fixed_price=True,
                         months=6, loan=0, loan_rate=0, holding_monthly=0,
                         sale=70_000_000, agent_pct=0, agent_vat_pct=0, agent_fixed=0,
                         tax_pct=0, share_pct=0)
    check("flip: a fixed price keeps the overrun off the investor",
          abs(flf["reno_to_investor"] - 12_000_000) < 1e-6 and abs(flf["builder_exposure"] - 1_200_000) < 1e-6)
    check("flip: VAT refund is a share of the VAT inside the labour",
          abs(flf["vat_refund"] - (7_000_000 - 7_000_000 / 1.24) * 0.6) < 1e-6)
    check("flip: break-even with no selling costs equals total in",
          abs(flf["break_even"] - flf["total_in"]) < 1e-6)

    # phases
    check("phase 0 when the month loses", phase(-1, 0, 100, 0).startswith("0"))
    check("phase 1 with no buffer", phase(10, 50, 100, 500).startswith("1"))
    check("phase 2 with 1-3 months buffer and debt", phase(10, 200, 100, 500).startswith("2"))
    check("phase 3 with buffer and debt", phase(10, 400, 100, 500).startswith("3"))
    check("phase 4 debt-free with buffer", phase(10, 400, 100, 0).startswith("4"))

    print(f"\nselftest: {'PASS' if fails == 0 else f'{fails} FAILED'}")
    return 0 if fails == 0 else 1


# ------------------------------------------------------------------- main ---

def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--currency", default="", help="label for amounts, e.g. ISK, EUR")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("plan", help="read a private snapshot JSON and print the situation")
    s.add_argument("--snapshot", required=True, help="path to finance-snapshot.json (outside any repo)")

    s = sub.add_parser("quick", help="the situation from a few numbers, no snapshot (ratio mode)")
    s.add_argument("--income", type=float, required=True, help="monthly income to the owner, all sources")
    s.add_argument("--essential", type=float, required=True, help="essential monthly burn")
    s.add_argument("--full", type=float, default=0.0, help="full monthly burn (default: essential)")
    s.add_argument("--cash", type=float, default=0.0)
    s.add_argument("--debt-total", type=float, default=0.0)
    s.add_argument("--rate", type=float, default=15.0, help="weighted debt rate percent (default 15)")
    s.add_argument("--minimums", type=float, default=0.0, help="total minimum payments (default 3%% of debt)")
    s.add_argument("--debt-budget", type=float, default=0.0, help="monthly money for debts incl. minimums")

    s = sub.add_parser("debt", help="debt payoff strategies")
    s.add_argument("--debts", required=True, help="JSON file: list of debts or {\"debts\": [...]}")
    s.add_argument("--budget", type=float, default=0, help="total monthly money for all debts")
    s.add_argument("--strategy", choices=["avalanche", "snowball", "minimums", "compare"], default="compare")

    s = sub.add_parser("runway", help="months of cash")
    s.add_argument("--cash", type=float, required=True)
    s.add_argument("--burn", type=float, required=True, help="monthly outflow incl. debt minimums")
    s.add_argument("--income", type=float, default=0.0, help="expected monthly income")

    s = sub.add_parser("fi", help="FI number and years to FI")
    s.add_argument("--spend", type=float, required=True, help="annual spending in retirement (today's money)")
    s.add_argument("--assets", type=float, default=0.0, help="invested assets today")
    s.add_argument("--savings", type=float, default=0.0, help="annual amount invested")
    s.add_argument("--real-return", type=float, default=5.0, help="real return percent (MMM uses 5)")
    s.add_argument("--swr", type=float, default=4.0, help="withdrawal rate percent (4 = the classic rule)")

    s = sub.add_parser("rate", help="freelance rate from a take-home target")
    s.add_argument("--net", type=float, required=True, help="annual take-home wanted")
    s.add_argument("--tax", type=float, default=35.0, help="effective tax+contributions percent on profit (35 is a placeholder - use the accountant's figure)")
    s.add_argument("--overhead", type=float, default=0.0, help="annual business costs")
    s.add_argument("--hours", type=float, default=40.0, help="working hours per week")
    s.add_argument("--weeks", type=float, default=46.0, help="working weeks per year")
    s.add_argument("--utilization", type=float, default=60.0, help="billable share of hours, percent")

    s = sub.add_parser("unit", help="subscription unit economics")
    s.add_argument("--price", type=float, required=True, help="monthly price per customer")
    s.add_argument("--margin", type=float, default=80.0, help="gross margin percent")
    s.add_argument("--churn", type=float, default=5.0, help="monthly churn percent")
    s.add_argument("--cac", type=float, default=0.0, help="cost to acquire one customer")
    s.add_argument("--target-mrr", type=float, default=0.0)

    s = sub.add_parser("score", help="rank business options")
    s.add_argument("--options", required=True, help="JSON: {criteria?: {...}, options: [{name, scores{}}]}")

    s = sub.add_parser("job", help="one job's contribution and effective hourly rate")
    s.add_argument("--price", type=float, required=True, help="what the customer pays (incl. VAT if --vat given)")
    s.add_argument("--materials", type=float, default=0.0)
    s.add_argument("--hours", type=float, required=True)
    s.add_argument("--other", type=float, default=0.0, help="subcontractors, transport, consumables")
    s.add_argument("--vat", type=float, default=0.0, help="VAT percent included in the price (24 in Iceland)")
    s.add_argument("--target-hourly", type=float, default=0.0, help="the rate from `rate`")

    s = sub.add_parser("forecast", help="month-by-month cash path")
    s.add_argument("--cash", type=float, required=True)
    s.add_argument("--income", required=True, help="monthly incomes, comma separated; the last value repeats")
    s.add_argument("--burn", type=float, required=True, help="monthly burn excluding debt payments")
    s.add_argument("--debt", type=float, default=0.0, help="monthly debt payments")
    s.add_argument("--months", type=int, default=12)

    s = sub.add_parser("flip", help="buy-renovate-resell: the full cost stack, both sides, and the downside")
    s.add_argument("--price", type=float, required=True, help="purchase price")
    s.add_argument("--sale", type=float, required=True, help="expected sale price")
    s.add_argument("--months", type=int, required=True, help="months from purchase to sale proceeds")
    s.add_argument("--stamp-pct", type=float, default=0.0, help="stamp duty percent on the deed")
    s.add_argument("--fees-buy", type=float, default=0.0, help="registration, legal, survey")
    s.add_argument("--materials", type=float, default=0.0)
    s.add_argument("--sub-trades", type=float, default=0.0, help="plumber, electrician, others")
    s.add_argument("--hours", type=float, default=0.0, help="the builder's own hours")
    s.add_argument("--rate", type=float, default=0.0, help="the builder's charge-out rate per hour")
    s.add_argument("--vat", type=float, default=0.0, help="VAT percent included in labour figures")
    s.add_argument("--vat-refund", type=float, default=0.0, help="percent of the VAT on labour refunded")
    s.add_argument("--contingency", type=float, default=0.0, help="percent overrun allowance on the renovation")
    s.add_argument("--fixed-price", action="store_true", help="builder quoted a fixed price, so the overrun is the builder's")
    s.add_argument("--loan", type=float, default=0.0)
    s.add_argument("--loan-rate", type=float, default=0.0, help="annual percent")
    s.add_argument("--holding", type=float, default=0.0, help="monthly property charges, insurance, utilities")
    s.add_argument("--agent-pct", type=float, default=0.0, help="estate agent commission percent")
    s.add_argument("--agent-vat", type=float, default=0.0, help="VAT percent added to the commission")
    s.add_argument("--agent-fixed", type=float, default=0.0, help="marketing, documents, other selling costs")
    s.add_argument("--tax-pct", type=float, default=0.0, help="tax percent on the gain")
    s.add_argument("--share-pct", type=float, default=0.0, help="builder's share of the gain after tax")

    sub.add_parser("selftest", help="run built-in checks")

    a = p.parse_args(argv)
    if a.cmd == "selftest":
        return selftest()
    return {"plan": cmd_plan, "quick": cmd_quick, "debt": cmd_debt, "runway": cmd_runway, "fi": cmd_fi,
            "rate": cmd_rate, "unit": cmd_unit, "score": cmd_score, "job": cmd_job,
            "forecast": cmd_forecast, "flip": cmd_flip}[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())
