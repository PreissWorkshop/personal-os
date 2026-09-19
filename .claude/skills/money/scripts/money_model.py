#!/usr/bin/env python3
"""money_model.py - stdlib-only calculators for the money skill.

Subcommands
  plan      read a private snapshot JSON and print the situation: income, burn,
            gap, runway, debt horizon, phase
  debt      debt payoff - avalanche vs snowball vs minimums, indexation aware
  runway    months of cash at a given burn and income
  fi        FI number, years to FI, and the savings-rate table
  rate      freelance hourly / day rate from a target take-home income
  unit      subscription unit economics: LTV, CAC payback, customers needed
  score     rank business options with a weighted rubric
  selftest  run the built-in checks

No third-party packages, no network, no personal data inside this file.
Numbers in, numbers out; the judgement stays with the person reading them.
Percent inputs are written as percents (12.5 means 12.5 %), never as
fractions, because that is how people copy them off a bank statement.

Examples
  python money_model.py plan --snapshot ~/.preiss/finance/finance-snapshot.json
  python money_model.py debt --debts debts.json --budget 250000 --strategy compare
  python money_model.py runway --cash 900000 --burn 650000 --income 300000
  python money_model.py fi --spend 4800000 --assets 0 --savings 2400000
  python money_model.py rate --net 9000000 --tax 38 --overhead 1200000
  python money_model.py unit --price 29 --margin 85 --churn 4 --cac 120 --target-mrr 8000
  python money_model.py score --options options.json
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
    for d in debts:
        ds.append({
            "name": d["name"],
            "balance": float(d["balance"]),
            "apr": pct(float(d.get("apr", 0))),
            "idx": pct(float(d.get("index_rate", 0))),
            "min": float(d.get("min_payment", 0)),
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
          f"minimums {money(sum(float(d.get('min_payment', 0)) for d in debts), cur)}/mo")
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
    print(f"take-home target {money(a.net, cur)}/yr, effective tax {a.tax:g}%, overhead {money(a.overhead, cur)}/yr")
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
        return "2 BUFFER+KILL - build 3 months of essentials, then avalanche the expensive debt"
    if debt_total > 0:
        return "3 KILL DEBT - buffer done; surplus goes to the highest-rate debt, product work in fixed hours"
    return "4 COMPOUND - debt-free; invest the surplus, raise income with product/recurring revenue"


def cmd_plan(a: argparse.Namespace) -> int:
    snap = load_json(a.snapshot)
    cur = snap.get("currency", a.currency)
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
    s.add_argument("--tax", type=float, default=38.0, help="effective tax+contributions percent on profit")
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

    sub.add_parser("selftest", help="run built-in checks")

    a = p.parse_args(argv)
    if a.cmd == "selftest":
        return selftest()
    return {"plan": cmd_plan, "debt": cmd_debt, "runway": cmd_runway, "fi": cmd_fi,
            "rate": cmd_rate, "unit": cmd_unit, "score": cmd_score}[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())
