# FI and debt: the math, the evidence, the order of operations

Researched 2026-09-19 from a sandbox whose egress proxy refused every host
(mrmoneymustache.com, federalreserve.gov, consumerfinance.gov, moneyhelper,
aaii, morningstar, ssrn, vanguard - all 403). Labels: **[S]** snippet (the
claim appeared in a search result attributed to the URL; page not opened)
· **[I]** inference or arithmetic · **[R]** recalled from background
knowledge, not seen this session - never cite · **[G]** gap. Nothing here is
[V] verified yet; `sources.md` lists the upgrade pass. The arithmetic is
implemented in `scripts/money_model.py` and checked by its `selftest`.

Contents: 1 the FI number · 2 savings rate and years · 3 debt order ·
4 debt vs investing · 5 buffers · 6 which debt first by consequence ·
7 consolidation · 8 behaviour rules · 9 income vs frugality · 10 sources

## 1. The FI number

| Finding | Value | Label | Source |
|---|---|---|---|
| Bengen 1994, origin of the 4 % rule | "limiting annual withdrawals to 4%, adjusted for inflation, was effective in keeping the portfolio from depleting for the entire 30 years" - 50/50 stocks/bonds, US data from 1926, 30-year periods | [S] | Journal of Financial Planning Oct 1994 via robberger.com summary |
| Trinity Study 1998 (Cooley, Hubbard, Walz) | "a 4% withdrawal rate on accounts with 50% and 75% stocks had success rates of 95% and 98%, respectively over 30-year horizons" | [S] | AAII Journal Feb 1998 via thepoorswiss.com / Wikipedia |
| Morningstar, State of Retirement Income | safe starting rate 3.7 % (2025 edition), 3.9 % (2026 edition, released 2025-12-03): "applies to portfolios that hold between 30% and 50% in equities", 30-year horizon, 90 % success; flexible strategies up to 5.7 % | [V 2026-09-20] for 3.9 % (morningstar.com); rest [S] | morningstar.com; fa-mag.com |
| Early Retirement Now, SWR series | "With a withdrawal rate in the 3.25-3.50% range, you would have survived even during the most catastrophic historical market conditions."; "All failures of the naive 4% Rule occurred when the Shiller CAPE Ratio was elevated." | [S] | earlyretirementnow.com series (2016-2026) |
| Pfau 2010, international data | "a 4 percent real withdrawal rate is surprisingly risky ... it would have only provided 'safety' in 4 of the 17 countries" (1900-2008); "In Italy, the 4% rule failed 62.5% of the time" | [S] | SSRN 1699526; JFP Dec 2010 |
| FI multiplier | spending ÷ withdrawal rate: 25× at 4 %, 25.6× at 3.9 %, 27× at 3.7 %, 28.6× at 3.5 %, 30.8× at 3.25 % | [I] | arithmetic |

Planning rule [I]: the 4 % rule is a US, 30-year result. For an Icelander
investing globally with a horizon well past 30 years, plan at 3.25-3.5 %
(29-31× debt-free annual spending) and treat 4 % as the optimistic case.
The base is **debt-free spending that includes what an employer would
otherwise carry** - pension, health, tax. Run `fi --swr 3.5` beside the
default.

## 2. Savings rate → years to FI

Mr. Money Mustache, "The Shockingly Simple Math Behind Early Retirement"
(2012-01-13): "The calculation assumes a 5% real return (after inflation)
and the Trinity-Study-based 4% safe withdrawal rate."; "save 10% → 51
years; 25% → 32 years; 50% → 17 years; 75% → 7 years"; "Your time to
reach retirement depends on only one factor: your savings rate, as a
percentage of your take-home pay." [S: mrmoneymustache.com via
enoughmoney.ai, totalbalance.blog; the page itself was fetched 2026-09-20 from
main-pc and names the Trinity study - the quoted sentences were not checked
word for word]

The full table, recomputed from the formula n = ln(1 + target·r/s) /
ln(1+r) (reproduces MMM's four rows: 51.4 / 31.9 / 16.6 / 7.1) [I]:

| Savings rate | 5 % real, 4 % SWR | 5 % real, 3.5 % SWR | 3 % real, 4 % SWR |
|---|---|---|---|
| 10 % | 51 | 54 | 69 |
| 20 % | 37 | 39 | 47 |
| 30 % | 28 | 30 | 34 |
| 40 % | 22 | 24 | 26 |
| 50 % | 17 | 18 | 19 |
| 60 % | 12 | 14 | 14 |
| 70 % | 9 | 10 | 9 |
| 80 % | 6 | 6 | 6 |

Starting net worth is zero in that table; with debt, the first job is
reaching zero. `fi` takes assets, savings and spending directly.

## 3. Debt order: avalanche, with the snowball evidence in view

- The math [I]: with a fixed monthly budget, every extra króna on the
  highest-rate balance stops the largest future charge, so avalanche
  minimises interest and time. Worked example from the research (three
  debts 1,000,000 at 20 %, 400,000 at 9 %, 150,000 at 30 %; 40,000 a
  month): avalanche ≈ 717,678 interest in 57 months, snowball ≈ 815,347 in
  60 months, a 12 % difference. The gap is small when rates are similar and
  large when a big high-rate balance sits behind small low-rate ones.
- The behavioural evidence: Gal & McShane 2012, *Journal of Marketing
  Research* 49(4): "closing debt accounts is predictive of debt elimination
  regardless of the dollar balance of the closed accounts"; "the dollar
  balance of closed accounts is not predictive of debt elimination when
  controlling for the fraction of accounts closed" [S: scholars.northwestern.edu;
  DOI 10.1509/jmr.11.0272]. Observational data from a debt-settlement
  population: correlation with completion, not proof that snowball beats
  avalanche on cost [I]. Brown & Lahey 2015 "Small Victories" exists (CFPB
  hosted) - title only [G].
- Practical rule [I]: avalanche by default; the written plan and the monthly
  `plan` run supply the motivation the snowball is meant to give; use
  snowball only where he has abandoned plans before and the reordering
  costs little. Icelandic indexed loans are ranked on interest plus
  indexation (`iceland.md` §5).

## 4. Debt vs investing

- Repaying debt at rate i is a risk-free, tax-free return of i. Fidelity's
  rule of thumb: "you would only choose investing (the riskier bet) if it
  has at least a 70% chance of beating the more certain return you would
  earn by paying down debt" [S: fidelity.com pay-down-debt-vs-invest].
  An unattributed snippet, low confidence: "Paying off high-interest debt
  provides an immediate, guaranteed return equal to the interest rate
  you're avoiding" [S: westernsouthern.com].
- When investing first is rational [I]: (i) a contribution attracts an
  immediate match or subsidy above the debt rate - in Iceland the 15.5 %
  pension is mandatory, not a match, so it sits in the burn, not in this
  test (`iceland.md` §3); (ii) the debt's rate is below the risk-free
  rate; (iii) no cash buffer exists yet - liquidity first, because a forced
  new borrowing at 15 % costs more than the interest saved; (iv) the debt
  is tax-deductible or indexed at a low real rate. With Icelandic overdraft
  and card rates around 15 % [S] and the policy rate at 8 % [S], nothing
  liquid beats paying the card.

## 5. Buffers

| Finding | Value | Label | Source |
|---|---|---|---|
| Fed SHED (2024 data, May 2025) | "Sixty-three percent of adults said they would cover a hypothetical $400 emergency expense exclusively using cash, savings, or a credit card paid off at the next statement"; 13 % could not pay it by any means | [S] | federalreserve.gov SHED 2025 |
| Fed SHED (2025 data, May 2026) | "12 percent of all adults said they would be unable to pay a $400 expense by any means in 2025" | [S] | federalreserve.gov fact sheet 2026-05-13 |
| Vanguard | spending shocks vs income shocks; "Having at least $2,000 in emergency savings results in a 21% increase in financial well-being"; "aim to build three to six months' worth of living expenses ... for potential income shocks" (+13 % well-being) | [S] | investor.vanguard.com; Vanguard research 2023, 2025 |
| Self-employed | "a buffer of nine to 12 months is recommended due to the varying nature of freelance income and more frequent tax payments" | [S] low authority (bank/adviser pages) | usbank.com; epwealth.com |
| Where "3-6 months" comes from | not established; industry convention | [G] | - |

Rule for Tenis [I]: three accounts, in this order - a tax and VAT reserve
(a priority debt the day it is due, §6), a spending-shock tier of roughly
one month of essentials, then the expensive debt. Holding three months of
cash at 0 % while a 24 % card runs costs about 2 % of the card balance a
month; so once one month is banked, any balance above ~15 % gets the whole
surplus, the buffer grows toward three months from windfalls, and reaches
three months fully once nothing that expensive is left (phase 2). The
self-employed "9-12 months" is a phase-4 luxury.

## 6. Which debt first, by consequence (regulator template)

UK MoneyHelper's split, a template until the Icelandic enforcement ranking
is confirmed (`iceland.md` §6): "Priority debts are those that carry the
most serious consequences if you don't pay them." - court fines, council
tax, child maintenance, energy, "Income Tax, National Insurance and VAT,
mortgage, rent and any loans secured against your home"; non-priority:
"credit cards, overdrafts, and personal loans" (the creditor needs a
judgment first); on tax: "extra charges, debt collectors, money taken from
your account, court action or even prison in serious cases" [S:
moneyhelper.org.uk how-to-prioritise-your-debts].

Order of payment [I]: consequence first (tax, VAT, secured, rent), then
rate. The avalanche runs inside the non-priority group.

## 7. Consolidation

US CFPB: "a debt consolidation loan probably won't help you get out of
debt unless you reduce your spending or increase your income"; "If you
don't pay back the loan, you could lose your home in foreclosure."; "If
you continue using the paid-off cards, you can end up with both the
consolidation loan payment and new credit card balances"; "A debt
settlement company may try to convince you to stop paying your debts and
instead pay into a special account." [S: consumerfinance.gov ask-cfpb 1861,
1859]

Decision rule [I]: consolidate only if all five hold - lower all-in rate;
lower total interest over the new term (longer terms hide cost; `debt`
shows it); no unsecured debt becomes secured on a home; old lines closed
or frozen; the cash-flow cause fixed. Free public help (UMS in Iceland)
before any fee-charging settlement firm.

## 8. Behaviour rules that survive contact with real months

- Thaler & Benartzi, *Save More Tomorrow* (JPE 2004): "people commit in
  advance to allocating a portion of their future salary increases toward
  retirement savings" [S: journals.uchicago.edu; eric.ed.gov]. Headline
  numbers (78 % joined; 3.5 % → 13.6 %) are [R] - do not cite.
- Windfalls: Arkes et al. 1994 - "unexpected small windfalls ($3-5) are
  more likely to be spent on gambling or at a basketball game than
  anticipated windfalls of the same size" [S: ideas.repec.org]; Milkman &
  Beshears 2009 - "grocery spending increases by $1.59 when a $10-off
  coupon is redeemed, with the extra spending focused on groceries that a
  customer does not typically buy" [S: hbs.edu].
- Self-employed translation [I]: a standing rule moves x % of every paid
  invoice to the reserve and the debt account on the day it lands; the
  percentage steps up with each rate increase; the destination of every
  irregular receipt (VAT refund, large project payment, a HelmCNC sales
  spike) is written down before it arrives. The `plan` run each month is
  the commitment device.

## 9. Income vs frugality

- Dynan, Skinner & Zeldes 2004, *Journal of Political Economy*: "a strong
  positive relationship between saving rates and lifetime income" [S:
  nber.org w7906]. Below a threshold, spending is near its floor and the
  savings rate is capped [I].
- Arithmetic [I]: at spending 90 and income 100 (10 % rate) a 20 % income
  rise to 120 makes the rate 25 % - the jump frugality could only match by
  cutting a sixth of spending. Income has no ceiling; cutting does.
- Fed SCF 2022: "families that owned businesses had higher income and
  wealth than those that did not"; 20 % of families owned a private
  business, "nearly half of families in the top decile" [S:
  federalreserve.gov Oct 2023 bulletin]. Correlational; wealth also causes
  ownership [I]. "The Millionaire Next Door" self-employment share is [R]
  and carries survivorship bias - never cite it.

## 10. Sources (search-result URLs; none opened)

robberger.com Bengen summary; aaii.com/journal/199802/feature.pdf;
thepoorswiss.com/trinity-study; morningstar.com whats-safe-retirement-
withdrawal-rate-2026; fa-mag.com 85940; earlyretirementnow.com
safe-withdrawal-rate-series; papers.ssrn.com 1699526;
financialplanningassociation.org Pfau Dec 2010 PDF;
mrmoneymustache.com/2012/01/13/the-shockingly-simple-math-behind-early-
retirement; enoughmoney.ai; totalbalance.blog; scholars.northwestern.edu
Gal & McShane; journals.sagepub.com 10.1509/jmr.11.0272;
files.consumerfinance.gov Brown Small Victories PDF; fidelity.com
pay-down-debt-vs-invest; westernsouthern.com; federalreserve.gov SHED
2025 and 2026 pages and fact sheet other20260513a1; investor.vanguard.com
emergency-fund; corporate.vanguard.com research PDFs 2023, 2025;
usbank.com; epwealth.com; moneyhelper.org.uk how-to-prioritise-your-debts;
consumerfinance.gov ask-cfpb en-1861, en-1859; journals.uchicago.edu
10.1086/380085; eric.ed.gov EJ696088; ideas.repec.org jobhdp v59;
hbs.edu Milkman & Beshears PDF; nber.org w7906; federalreserve.gov
October 2023 SCF bulletin.
Blocked: all of the above hosts (403 on CONNECT), plus web.archive.org.
Gaps: Trinity's full table; ERN's long-horizon failure rates; Morningstar
2022-2024 rates; Networthify defaults; Brown & Lahey findings; a
regulator's own "guaranteed return" sentence; the origin of "3-6 months";
regulator evidence on self-employed buffer size; Dynan's quintile rates;
FTC guidance on negotiating with creditors; SMarT statistics.
