---
name: money
description: Personal finance and business-building skill for Tenis Preiss (Iceland; Preiss Workshop, Studio Esja, HelmCNC, ScanPen; C#/.NET, Python, Claude Code), who is paying off debt with no capital while building a location-independent business. ALWAYS load this skill before answering ANY question that touches his money, income or a business decision, however small, casual or "quick" - it holds the private-numbers workflow, the phase rules, Iceland-specific tax, loan and payment facts (ehf, VAT, verðtryggð loans, Stripe not serving Iceland) and the evidence labels that a general answer gets wrong. Triggers include: which debt to pay first (overdraft, credit card, car loan, indexed loan), budget, savings, runway, buffer; what to charge and how to invoice (day rate, hourly rate, retainer, a remote contract, from the ehf or as an individual); whether something will make money (a SaaS, an app on the Play Store or App Store, a plugin, a course, files, a product, HelmCNC pricing or promotion, the Studio Esja webshop, the surveillance app); remote jobs and contracts abroad; moving to Spain, Portugal or anywhere else and what happens with Skatturinn, the ehf and residency; payments and platforms (Stripe, Paddle, Lemon Squeezy, Freemius, Wise); investing, financial independence, how many years until he can stop working; and any course, guru, agency or "passive income" pitch. Use it even when the question looks simple enough to answer directly, even for one line, and even when he never says "money" or "finance". Not for the arithmetic inside a single customer quote - the workshop-ops repo owns quoting.
---

# Money: from debt to a business that pays for freedom

The job of this skill is to turn every money question into a decision Tenis
can act on this week, using real numbers, evidence that was actually
checked, and the cheapest path that works. He is in debt, has no capital,
and already owns things most people starting out do not: a running workshop
with clients, a shipped CNC control product with paying customers, two
brands, a website with a CRM, deep C#/.NET and Python skill, and a working
agent system. The way out is built from those, not from a fresh idea that
needs money he does not have.

Two truths shape every answer. First, cash flow beats everything: nothing
compounds while the month loses money, and a plan that ignores the next
sixty days is a fantasy. Second, the evidence on what works for one person
with skills and no money is consistent and boring: sell hours or a
productized service first, build the product in fixed hours funded by
those sales, prefer business customers and recurring revenue, get
distribution before polish, and never gamble. The case studies and base
rates behind that are in `references/`, each claim labelled by how it was
verified.

## Rules that do not bend

- **Real numbers or no numbers.** The private snapshot
  (`~/.preiss/finance/finance-snapshot.json`, never inside any repo -
  personal-os is public) is the only source of balances, income and debts.
  If it is missing, ask for the six numbers below or work in ratios and say
  so. Never invent a balance, a rate, a revenue figure, a case-study number
  or a tax rule. Never write his real figures into this repo or a report.
- **Label every claim**, with the same tags the references use: [V]
  Verified (source opened, quote on the page - say "verified <date> per
  the reference" unless this session opened it) · [S] Snippet (seen only in
  a search result - "reported, not confirmed") · [SR] Self-reported (a
  founder's own claim) · [I] Inference · [A] Assumption · [G] Gap ("I
  could not verify this") · [R] Recalled from memory - usable only as a
  pointer ("Spain has a special inbound-worker regime; ask the adviser"),
  never as a figure, a rate or a rule to act on. Founders' revenue numbers
  are marketing until proven otherwise; say so. When a fact is not in
  `references/`, search, open the source, label it, or say "I could not
  verify this" and give the [R] pointer so the gap is at least named.
- **Cash first, then buffer, then the expensive debt, then product.** The
  order is the phase model below. A product idea is welcome in every phase,
  but it gets the hours the phase allows, not the hours it wants.
- **No spending, borrowing, leverage or speculation** is ever recommended
  as the path: no trading, no crypto, no new loan to "invest in the
  business", no paid course or coaching before a paying customer exists,
  no inventory. The base rates are in `references/what-fails.md`.
- **Every hour has a price.** Unpaid hours on a product are a loan from the
  future, tracked like one. `scripts/money_model.py rate` gives the number.
- **Decisions are his.** The skill models, ranks, and says clearly what it
  would do and why; it never spends, signs, applies, or commits money.
  Tax, legal and immigration specifics are checked with a licensed adviser
  before acting - the skill gets him to that meeting prepared.
- **Brand-true.** Preiss Workshop stays precise and premium, Studio Esja
  stays calm and artistic. Income ideas that cheapen either brand (discount
  blasts, generic dropshipped goods under the name) are out.

## Evidence state (read once)

The references were built on 2026-09-19 from a cloud sandbox whose proxy
refused nearly every website, so every claim started **Snippet**-level. On
2026-09-20 two passes ran from main-pc with open internet - the script
(`scripts/verify_claims.py`) and then the employee session by eye - and
40 of the 44 load-bearing claims now read `[V 2026-09-20]`: the Skatturinn
2026 rates, thresholds and fees, the three Althingi acts, the Central
Bank's 8.00 %, Hagstofa CPI, the platform fees and Iceland payout lists,
Stripe's list without Iceland, ESMA, BIS, the FTC cases, Morningstar,
the Croatia threshold - each for exactly the wording found on the page,
nothing wider. The by-eye pass also corrected four references that had
been quoted wrongly (Acquire.com multiples, the BIS source, the Chague
wording, an FTC sentence) - a reminder that a snippet is not a reading.
Four claims remain [S]: Upwork's rate pages (bot challenge), MicroConf's
28 % (report behind a form), the EEA free-movement sentence (seen only
through a summarising tool), the Estonia threshold (programme page not yet
opened). `references/sources.md` holds the log. A line that still reads [S]
is quoted as reported, and before acting on that number he opens the link.

## Workflow

1. **Load the situation.** Read the snapshot if it exists and run
   `python scripts/money_model.py plan --snapshot <path>` (`python3` on
   Linux and macOS). If it does not, ask for: monthly income by source
   (last three months' average), essential monthly burn, full monthly
   burn, cash today, each debt with balance / rate / minimum /
   indexed-or-not, and committed work for the next ninety days. With only
   some of them, run `quick` on what he gave (it prints its assumptions)
   and label the rest; with none at all, answer in ratios (months of
   runway, share of income) and say so. Never proceed on imagined numbers.
2. **Name the phase** (below) and say it. It sets what the answer may
   recommend. Read the last three entries of the private decision log
   (`~/.preiss/finance/decisions.md`, template in `assets/`) so the answer
   is consistent with what was already decided, and say so if it is not.
3. **Pick the reference for the question** (table below), read it, and use
   only claims with their labels.
4. **Run the numbers**, never estimate them in prose:
   debt strategy (`debt`), runway (`runway`), the rate he must charge
   (`rate`), the product's unit economics (`unit`), years to financial
   independence (`fi`), and the ranking of options (`score`). Paste the
   script's output; do not retype it into different figures.
5. **Decide.** One recommendation, the conditions under which it flips,
   and the next seven days as a numbered list with at least one cash
   action. Then the standard footer for any answer he will act on:
   Sources checked · Supporting evidence · Assumptions · Unverified points
   · Confidence (High / Medium / Low).
6. **Keep it short.** He reads fast and decides fast: the decision in the
   first ten lines, one table of numbers, the seven days, the footer -
   about 500-900 words for a full answer, a few lines for a quick
   question. The model, the case studies and the script runs go below the
   decision or into a follow-up he asks for, never before it.
7. **Log it.** Append the decision to the private log in the template's
   format (phase, question, decision, why, flips-if, numbers with labels,
   review date). On a review date, score the entry: held, flipped, wrong -
   and say what that changes.

Six numbers or nothing: income by source, essential burn, full burn, cash,
debts (balance, rate, minimum, indexed?), committed work. Everything else
in this skill is a function of those.

## The phases

The script labels them; the meaning is here. Numbers are monthly.

| Phase | Condition | What the month is for | Product hours |
|---|---|---|---|
| 0 Stabilise | income < full burn + minimums | Stop the bleed: collect receivables, cut, sell hours or a productized service this week, call creditors before missing a payment | 0 - every hour is for cash |
| 1 Cash | positive month, cash < 1 month of essentials | Bank every surplus króna into one month of essentials; keep selling hours | Evenings only, capped |
| 2 Buffer + kill | cash 1-3 months, debt remains | One month is banked. Any debt above ~15 % (a card, an overdraft) gets the whole surplus now - holding cash at 0 % against a 24 % balance is a loss; the buffer grows toward 3 months from windfalls, and fully once nothing that expensive is left | Fixed block, e.g. one day a week |
| 3 Kill debt | buffer done, debt remains | Whole surplus to the highest-rate debt; product in a fixed weekly block funded by sold hours | 1-2 days a week |
| 4 Compound | debt-free, buffer done | Invest the surplus; raise income through product and recurring revenue; the savings rate is the dial | As much as cash flow allows |

Why avalanche and not snowball: the math says highest rate first, and the
behavioural evidence for snowball is about motivation, which a written plan
and a monthly `plan` run replace. Icelandic indexed (verðtryggð) debt is
compared on interest plus indexation, which the script does. Tax and VAT
due are priority debts by consequence and come before the avalanche.
Details and sources: `references/fi-and-debt.md`.

## The ladder: how one person with no money builds income

Every reported case of a solo builder going from nothing to a real business
climbs the same ladder, and the ones who skipped a rung mostly failed:

1. **Sold hours** - contracting, freelancing, a remote part-time job. The
   fastest cash there is, the only rung reachable in 60 days, and the same
   skills that build the product pay for it. Invoiced from his own
   business, it is the door that survives a move abroad.
2. **Productized service** - one fixed-scope, fixed-price deliverable sold
   repeatedly (a KFLOP machine commissioning package, a shop's quote-ready
   cutlist and CNC program, a one-workflow automation for a trade
   business). Sells like a product, delivers like a service, needs no
   capital.
3. **Product** - software, files, a course or book - built in fixed hours
   from what the service taught, sold to the same customers first.
4. **Recurring revenue** - subscription, maintenance, licences with
   renewals, retainers. This is the rung financial independence is built
   on; one-off sales never compound.

Case studies with their numbers and labels: `references/case-studies.md`.
The playbook for each rung, and the first 30 days: `references/playbooks.md`.

## Testing an idea in five questions

Ask these before any modelling; a "no" on the first three ends the
discussion in the current phase:

1. Can it produce cash within 60 days without spending money? (Phase 0-2
   ideas must.)
2. Does it use what he already has - the workshop's clients, HelmCNC's
   users, the machine, the code, the agent system, the brands?
3. Is the customer a business that already pays for this kind of thing?
4. Is it recurring, or can it become recurring?
5. Can it be sold in English to the world, from anywhere, without him
   physically present?

Then the criteria the best-documented bootstrappers use (business
customer, recurring, predictable acquisition, annual prepay, an
aftermarket for an existing ecosystem) in `references/case-studies.md`,
and `scripts/money_model.py score` with `assets/options-example.json` as
the rubric template.

## His assets, in order of nearness to money

Judgement, not verified fact, except where marked; the evidence for each
is in `references/maker-leverage.md`:

1. **Skills for hire** - C#/.NET desktop and machine control, Python and
   computer vision, agent systems with Claude Code. The bridge income in
   phases 0-2, remote-capable. Label them by their highest-paid names
   (machine-control engineer, computer-vision engineer), never ".NET
   developer".
2. **HelmCNC** - shipped and licensed (Verified from its own site: $239
   perpetual, $129 founder price, six payments of $45, 24 months of updates
   included then an optional $19 a year, 14-day trial, "Built on the
   KMotion libraries with Dynomotion's permission"). The nearest product
   business he owns; its ceiling is the KFLOP/Kogna installed base, and no
   other paid front-end for that hardware was found. Sell more of what
   exists before building anything new.
3. **The workshop** - cash now, but tied to the building and to him. Its
   value online is the knowledge inside it: quoting, cutlists, CNC setup,
   film and signage processes, which small shops abroad pay for. The
   founder pattern "built it for my own shop, then sold it to my trade" is
   the strongest evidence in the maker research.
4. **Studio Esja** - high margin, low volume, brand-sensitive. Online it is
   content, drops and a waiting list, not a stocked shop; a channel, not a
   scalable income.
5. **ScanPen** - hardware-adjacent; the evidence says hardware is the
   slowest and most capital-hungry path. Software-only or parked until
   phase 4 or a paying pilot customer.

## Which reference for which question

| Question is about | Read |
|---|---|
| Debt order, buffer size, FI number, savings rate, years to FI, invest vs pay down, consolidation | `references/fi-and-debt.md` |
| Real bootstrapped case studies and the base rates (how many make it, how long, exit multiples) | `references/case-studies.md` |
| What to do first, the rungs, freelance platforms and rates, productized services, pricing, validation, first ten customers, AI work that sells, timelines | `references/playbooks.md` |
| HelmCNC, the workshop, Studio Esja, ScanPen, CNC software prices, licensing platforms, marketplaces, vertical shop software | `references/maker-leverage.md` |
| AI and software demand, platform fees, API and hosting costs, margins, distribution, what still commands a premium | `references/software-and-ai.md` |
| Iceland: ehf vs sole trader, VAT, tax brackets, rates, indexed loans, debt help, leaving, payments from Iceland, questions for the accountant | `references/iceland.md` |
| A company (ehf) that owes tax or trade debt: the director's personal exposure, penalty interest and surcharges, collection and closure, payment plans with Skatturinn, where a payment goes, insolvency duties, clawback and the business ban, stopping the company, and what a New Zealand visa asks about character | `references/iceland-company-debt.md` |
| An interior film installation course: who already sells training, online and in-person prices, the vehicle-wrap comparables, countable demand on YouTube, tools | `references/interior-film-training.md` |
| Making the videos: AI dubbing prices and rights, YouTube's own dubbing and disclosure rules, editing tools an agent can drive, which languages first | `references/video-production-and-dubbing.md` |
| Getting trade experience certified: Iceland's raunfærnimat and sveinspróf, the licensed-trade law (Act 42/1978), NZQA assessment, BCITO experience recognition, and how New Zealand visas count a trade certificate | `references/trade-qualification.md` |
| Remote jobs, contractor setups, nomad visas, tax residency, entities abroad, health and pensions, the move in order | `references/remote-and-relocation.md` |
| Courses, gurus, dropshipping, trading, crypto, MLM, "passive income", app-store odds, the red-flag checklist | `references/what-fails.md` |
| What was and was not verified, the labels, the upgrade pass | `references/sources.md`, `references/claims.json` |
| The words: contract pitch, productized offer, HelmCNC founder mail, forum post, automation offer, warm-network note, bank call, price rise, saying no | `references/templates.md` |

## Scripts

`scripts/money_model.py` (stdlib only, no network; `selftest` proves it):

| Command | Gives |
|---|---|
| `plan --snapshot <json>` | income, burn, gap, runway, debt horizon, phase |
| `quick --income --essential --cash --debt-total --rate` | the same from a few numbers, no snapshot (ratio mode; prints its assumptions) |
| `debt --debts <json> --budget N --strategy compare` | avalanche vs snowball vs minimums: months, interest, indexation, order |
| `runway --cash --burn --income` | months of cash and the income that stops the bleed |
| `fi --spend --assets --savings [--swr 3.5]` | FI number, years to FI, the savings-rate table |
| `rate --net --tax --overhead` | the hourly and day rate that actually pays (`--tax` default is a placeholder; use the accountant's effective rate) |
| `unit --price --margin --churn --cac --target-mrr` | LTV, CAC payback, customers needed, replacements per month |
| `score --options <json>` | ranked options on the nine criteria |
| `job --price --materials --hours --vat --target-hourly` | one job's contribution and effective hourly against the target rate (the business view of a quote) |
| `forecast --cash --income a,b,c --burn --debt --months` | month-by-month cash; names the first month that goes negative |
| `verify_claims.py [--only prefix] [--report out.md]` | the upgrade pass: fetches each claim in `references/claims.json` and reports VERIFIED / NOT FOUND / BLOCKED |
| `check_references.py` | before a commit: every table lines up, `claims.json` is well-formed, [V] labels carry dates |

Percent inputs are percents (12.5 means 12.5 %). Templates:
`assets/finance-snapshot.template.json` and `assets/decisions-template.md`
(copy both outside the repo), `assets/debts-example.json`,
`assets/options-example.json` - invented numbers, not anyone's real ones.

## Review list (run it every time)

- The phase is named and the recommendation fits it.
- No number in the answer was invented; script output is pasted, not
  paraphrased into different figures.
- Every case study or statistic carries its label and its source is in
  `references/`, or the answer says "I could not verify this".
- Founder revenue claims are marked Self-reported; snippet-level facts are
  "reported", with the link to open before acting.
- The answer ends with what could be wrong and what would flip it.
- The next seven days are a numbered list with at least one cash action.
- Nothing recommends spending, borrowing, trading, or a course before a
  paying customer.
- No real balance, income or debt figure is written into the repo or a
  report; the phase and the decision are enough there.
- Tax, legal and immigration specifics are marked for a licensed adviser.
- Brand tone protected; nothing cheapens Preiss Workshop or Studio Esja.
