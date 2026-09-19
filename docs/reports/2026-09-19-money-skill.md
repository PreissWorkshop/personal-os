# Money skill — built 2026-09-19

Cloud session on branch `claude/profitable-business-debt-situation-6d7hq3`.
Tenis's ask: the best possible skill for finances, money, building
businesses and online nomad businesses that may involve coding, AI and
software, because he needs to build a profitable business and reach
financial independence from a position of debt with no capital; find case
studies, investigate what actually works and the fastest route, and cover
remote work that survives a relocation.

## What exists now

`.claude/skills/money/`

| File | What it is |
|---|---|
| `SKILL.md` | Trigger description (pushy on purpose), the rules that do not bend, the evidence state, a five-step workflow, the five-phase model (stabilise → cash → buffer + kill → kill debt → compound), the four-rung ladder (sold hours → productized service → product → recurring), the five-question idea test, his assets ranked by nearness to money, a question-to-reference table, the script table, a review list |
| `references/fi-and-debt.md` | The FI number (Bengen, Trinity, Morningstar, ERN, Pfau), the savings-rate table, avalanche vs snowball with the behavioural evidence, debt vs investing, buffers, priority-by-consequence, consolidation rules, behaviour rules, income vs frugality |
| `references/iceland.md` | ehf vs sole trader, VAT, 2026 tax brackets and levies, reiknað endurgjald, corporate tax and the 20/50 rule, policy rate and inflation, indexed loans, UMS debt mitigation, limitation periods, leaving Iceland (3-year tail, ehf residency exemption, treaties), cost of living, payments from Iceland, questions for the accountant |
| `references/case-studies.md` | Fourteen bootstrapped cases with fields (product, start, ramp, channel, key decision), time-to-living-wage table, base rates (MicroConf, secondary aggregations), exit multiples, the patterns |
| `references/playbooks.md` | The first 30 days; freelance platforms, fees and Upwork medians; productized services (DesignJoy, Draft.dev); consulting-to-product transitions; recurring revenue and retainers; pricing; validation with money; first ten customers; AI work that sells; saying no; timelines |
| `references/maker-leverage.md` | HelmCNC (verified pricing) and the CNC-control price landscape; licensing platforms and fees; digital files; vertical shop software; makers with own-account income models; ScanPen's competitive set; the opportunity map |
| `references/software-and-ai.md` | Demand signals; what solo developers sell and platform fees (Apple, Microsoft Store verified); AI products with public numbers; SMB AI use vs spend; verified Anthropic API prices and a margin sketch; developers vs businesses as buyers; distribution; remote AI work; the limits |
| `references/remote-and-relocation.md` | Remote job market; employer-of-record vs contractor and permanent establishment; visa thresholds and EEA free movement; tax residency tie-breakers; cost of living; payments abroad; entity options (Estonia, US LLC, stay put); health and pensions; GitLab's async rules; the move in order |
| `references/what-fails.md` | Base-rate table (CFDs, day trading, crypto, MLM, coaching schemes, Amazon sellers, startup survival, creators, app stores, BNPL); regulator cases; the red-flag checklist; how to answer a "course" question |
| `references/sources.md` | The labels, what was verified on the page, the ordered upgrade pass, stream-to-file map, the blocked hosts |
| `scripts/money_model.py` | Stdlib-only calculators: `plan` (snapshot → phase), `quick` (the same from a few numbers, no snapshot), `debt` (avalanche / snowball / minimums, indexation aware, minimums assumed and flagged when missing), `runway`, `fi`, `rate`, `unit`, `score`; `selftest` passes 33 checks |
| `assets/` | `finance-snapshot.template.json` (zeros, to be copied outside the repo), `debts-example.json`, `options-example.json` (invented numbers) |
| `evals/evals.json`, `evals/trigger-evals.json` | Four test prompts with eight assertions each; twenty trigger queries (ten should load the skill, ten should not) |

Wired in: `CLAUDE.md` (new "Money and business" section), `docs/employee.md`
(new "Money" section: research and model, never spend or commit, never
real figures in the repo), `docs/agent-system.md`, the bootstrap doc (a
junction to expose the skill user-wide, and the private snapshot location
`~\.preiss\finance\` — both unverified on Windows), `.gitignore`
(`finance/`, `*finance-snapshot*.json`, template excepted).

Privacy: personal-os is public on GitHub. The skill contains no real
balance, income, debt or customer figure; the eval prompts use invented
numbers. It does state the situation in general terms (debt, no capital)
because the advice depends on it — one more reason to take the open
decision to make this repo private (tracker, 🔒 "Is this repo meant to be
public?"). Real figures live only in the private snapshot outside every
repo, and the employee rules say a report quotes the phase and the
decision, never the balances.

## What was read

Eight research workers ran in parallel, one per stream: FI math and debt;
Iceland money, tax and legal; indie software case studies and base rates;
the services-to-product path; remote work and relocation; what fails;
maker leverage (his own assets against their markets); software and AI
money. About 3,200 lines of sourced findings, kept in the session
scratchpad; the reference files carry what survived a second reading.

**The sandbox's egress proxy refused nearly every website** (403 on
CONNECT: skatturinn.is, sedlabanki.is, island.is, althingi.is, stripe.com,
the FTC, ESMA, BIS, the Fed, every founder's blog, every vendor's pricing
page, Wikipedia, even web.archive.org). Only WebSearch worked, plus
github.com, raw.githubusercontent.com, platform.claude.com and
developer.apple.com. Consequence: **most claims in the references are
snippet-level** — the number appeared in a search result attributed to the
source, and the page was not opened. Every such claim is labelled [S] (or
[SR] for a founder's own figure), and `references/sources.md` gives the
ordered upgrade pass to run from a machine with open internet.

Verified on the page this session: HelmCNC's own site (pricing, trial,
rent-to-own, the update line, the Dynomotion relationship), Anthropic's
API pricing page, Apple's Small Business Program page, and the Cloudflare
Workers, Fly.io and Microsoft Store docs via their public source repos;
Anthropic's plugin-directory README (no revenue mechanism for plugins).

Also read: the registry, the tracker, the employee and agent-system docs,
and the Icelandic skill branch for the skill convention this one follows.

## What the evidence says (short)

- **Cash flow first.** Nothing in the case studies started from zero income
  and zero audience and reached a living wage inside six months, except a
  founder whose partner was the customer. Every winner bridged income
  (freelancing, a job until launch, ramen profitability as a checkpoint);
  the year-of-savings, twelve-launches approach shows up only in the failed
  batches. Plan for a 12-24 month ramp with sold hours underneath.
- **The ladder is the pattern.** Sold hours → productized service →
  product → recurring revenue. DesignJoy and Draft.dev (self-reported)
  show the productized rung; Basecamp, Mailchimp and Tailwind show the
  service-funded product; Storemapper, FeedbackPanda, Bannerbear, Plausible
  and Sidekiq show recurring B2B revenue as the sellable asset.
- **Base rates are harsh and labelled.** MicroConf 2024: 28 % of
  independent SaaS under $1k MRR (survivors only); Levels' own hit rate
  about 5 %; BLS: half of new employer establishments gone by year five;
  ESMA: 74-89 % of retail CFD accounts lose; a Brazilian study: 97 % of
  persistent day traders lose; four FTC cases against "$10k a month"
  coaching and done-for-you store sellers.
- **Iceland specifics that change the plan** (all snippet-level, to be
  confirmed): Stripe does not list Iceland, so a merchant of record
  (Freemius, Paddle, Lemon Squeezy) is the payment stack; a former resident
  stays fully tax-liable for three years unless taxed elsewhere; an ehf's
  director-residency rule exempts EEA residents, so Spain or Portugal keeps
  it compliant; the policy rate is 8 % and card/overdraft rates about 15 %,
  which makes paying the card the best risk-free investment available;
  indexed loans drift up with 5 % inflation and must be ranked on interest
  plus indexation.
- **His nearest money** (judgement): skills for hire labelled by their
  highest-paid names; HelmCNC sold into the KFLOP/Kogna base it was built
  for (no other paid front-end found); the workshop's know-how as a
  productized service and then the shop tool, English-first; Studio Esja
  as a channel, not a scalable income; ScanPen software-only or parked.
- **AI money** (verified where it matters): Anthropic's list prices allow a
  75-82 % gross margin on a $10/month metered product; MCP servers and
  Claude Code plugins have no stated revenue path and are distribution
  only; what SMBs pay for AI, by category, was not found.

## Test results

Four prompts from `evals/evals.json` (invented figures), each run by a
fresh subagent with the skill and by another without it, eight assertions
per prompt, graded by a separate subagent per prompt with the
skill-creator's grader instructions (burden of proof on the assertion, no
partial credit). Both configurations ran after the research workers had
exhausted the session's web-search budget, so both answered from
references or memory - a comparison of discipline, not of research.

| Prompt | With skill | Without | What the grader saw |
|---|---|---|---|
| 1 Debt, what to do this month | 8/8 | 4/8 | Skill: phase named, the six numbers requested, card first with tax/VAT ahead by consequence, every figure labelled, the payoff table pasted from the script (the grader re-simulated all nine rows, exact match). Baseline: sound week-by-week plan, but no phase, no labels, the formula only in its notes, and an arithmetic slip on the card's share of interest. |
| 2 SaaS tool vs remote contract | 8/8 | 4/8 | Skill: contract first with a bounded product block; Storemapper, Wathan and Bannerbear correctly attributed; MicroConf base rate labelled; rubric and script outputs reproduced by the grader. Baseline: same call, but no named funded-product cases, no criteria, founder figures unlabelled; its Icelandic tax arithmetic was accurate. |
| 3 Moving to Spain/Portugal, ehf, Stripe | 7/8 | 5/8 | Skill: Act 138/1994 EEA exemption quoted, Stripe and the merchant-of-record stack complete, every number labelled; it failed to state EEA free movement outright (an aside only). Baseline: covered Spain's and Portugal's own regimes from memory, which the references lack, but never mentioned the ehf residency rule, omitted Freemius, and put dozens of unlabelled rates behind one disclaimer (none found wrong). |
| 4 The $1,997 AI-agency course | 8/8 | 6/8 | Skill: the FTC cases matched to the pitch line by line, a red-flag count, the price in billable hours, a zero-cost alternative for this week. Baseline: also a clear no with accurate cases and a 30-day test, but assumptions stated as fact and no assumptions/confidence footer. |

Means: with the skill 97 % (31 of 32 assertions), without 59 % (19 of
32); wall time about equal (411 s vs 435 s); the skill runs used roughly
60 % more tokens (about 121k vs 76k) because they read the references.
Outputs, gradings and a static review page (`money-skill-review.html`)
are in the session scratchpad; the page was sent to Tenis.

My own read of two full answers (prompts 1 and 4): the skill's answers
are the ones he would act on - one decision, the numbers in a table, the
seven days, the footer - and they are long. A brevity rule went into the
skill afterwards. The baseline answers are competent general advice with
invisible assumptions; the skill's value is discipline (no invented
number, every claim labelled, cash first) more than knowledge, except
where the references carry Iceland-specific facts the baseline lacked.

**Trigger accuracy** (`claude -p` on the twenty trigger queries, one run
each): the first description scored 12 of 20 - all ten negatives right,
two of ten money questions loaded the skill. The rewritten, pushier
description scored 13 of 20 (three positives). A bounded two-iteration
optimisation loop (skill-creator `run_loop`, 40 % held out) found nothing
better: held-out 8 of 8, training 8 of 12. Precision is 100 %, recall
low: in a bare session Claude answers casual money questions directly.
Mitigation, not a fix: `CLAUDE.md`'s Money section is always in context
in this repo, and the bootstrap doc now adds a one-line rule to the
machine-wide `~\.claude\CLAUDE.md` so every project root loads it.

**Folded back from the runs** (second iteration, not re-run): `quick`
ratio mode and assumed minimums in the calculator; the tax default marked
as a placeholder; the buffer-versus-card rule (no cash held at 0 % against
a 24 % card); the brevity rule; harmonised labels, the [R] pointer rule
and "verified per the reference" wording; the churn-benchmark gap; the
destination-tax gap with one recalled pointer on how Spain's inbound
regime may interact with Iceland's three-year rule. The graders' critique
of the assertions themselves (one depends on context absent from the
prompt; one measures labelling, not invention; none covers the
destination country's taxes) is the to-do list for the next iteration.

## Second round, same day: what else would improve it

Tenis asked how the skill could improve further and for a rating against
two days earlier. Rating, my judgement with the test scores as the only
measured part: two days ago (no skill) about 5/10 for his situation -
competent general answers, invisible assumptions, nothing Icelandic, 19
of 32 test assertions; now about 7.5/10 - 31 of 32, phase discipline,
calculators, labelled evidence; held below 9 by unverified numbers,
under-triggering, missing destination-country taxes and no live data.
Built in the second round:

| Improvement | What exists now |
|---|---|
| Verification made mechanical | `references/claims.json` (44 load-bearing claims with URL and quote) and `scripts/verify_claims.py`, which fetches each page and prints VERIFIED / NOT FOUND / BLOCKED. Tested here: the three controls (HelmCNC site, Anthropic pricing, Apple) verify; stripe.com reports BLOCKED, as expected from this sandbox. |
| Trigger reliability | `.claude/hooks/money_trigger.py` plus `.claude/settings.json`: a prompt hook that injects a one-line "load the money skill" note when money or business words appear (English and Icelandic). Pipe-tested on five prompts (three positives, two negatives); not provable in-session because prompt hooks fire outside the turn - `[UNVERIFIED — needs check]` on the next session. The bootstrap doc gives the user-level version for other roots. |
| Real numbers, continuously | A private decision log (`assets/decisions-template.md`, kept beside the snapshot): the skill reads the last three entries before answering and scores each on its review date. The employee gains a monthly money review (`docs/employee.md`): run `plan`, compare phases, score due decisions, report five lines with no figures. |
| Calculator | `job` (one job's contribution and effective hourly against the target rate, VAT stripped) and `forecast` (month-by-month cash, names the first negative month); self-test 40/40. |
| Sales assets | `references/templates.md`: contract pitch, productized offer one-pager, HelmCNC founder-price mail, KFLOP forum post, automation offer, warm-network note, bank call script, price rise, saying no - in his register, prices always from the scripts. |
| Evals | Six prompts now (HelmCNC pricing and a below-budget kitchen job added); two assertions the graders called ambiguous were tightened. Not re-run. |

Still needing open internet or him: the verification run itself; Spain's
and Portugal's own tax regimes (one recalled pointer was added on how an
inbound special regime may interact with Iceland's three-year rule); SMB
churn benchmarks and what SMBs pay for AI; feeds from the website CRM
(receivables, pipeline) and Freemius (HelmCNC sales) into the snapshot -
those belong in the website and HelmCNC repos, one session each.

## Blocked or not done

- No external page except the seven listed could be opened; the upgrade
  pass is Tenis's (or the employee's, from main-pc) to run.
- The skill-creator's description-optimisation loop needs the `claude` CLI
  and was skipped; the trigger description was written by hand.
- The Windows junction and the `~\.preiss\finance\` snapshot location are
  unverified on Windows.
- Nothing Iceland-specific on consumer protection (Neytendastofa), the
  collection-cost regulation, wage attachment, or the FME transposition of
  ESMA's CFD rules was found.
- What SMBs actually pay for AI, by category and amount, was not found —
  the key missing input for a trades-vertical product thesis.

## Sources checked

- HelmCNC public site and repo; platform.claude.com pricing;
  developer.apple.com small-business-program; cloudflare-docs, superfly
  and MicrosoftDocs public repos; anthropics/claude-plugins-official —
  opened.
- Search-result snippets attributed to: skatturinn.is, stjornarradid.is,
  government.is, sedlabanki.is, hagstofa.is, althingi.is, island.is;
  taxsummaries.pwc.com, KPMG and Deloitte Legal 2026 booklets;
  numbeo.com; stripe.com/global via secondary lists; Freemius, Paddle,
  Lemon Squeezy, Gumroad, Etsy, Creative Fabrica; Upwork's rate and fee
  pages and Q2 2026 release; Fiverr, Toptal, Contra; DesignJoy, Draft.dev,
  37signals, Mailchimp, Tailwind, Bannerbear, Buffer, Storemapper,
  FeedbackPanda, ConvertKit, ShipFast, TypingMind, Small Bets, Plausible,
  Sidekiq, HeadshotPro founders' posts; MicroConf, Acquire.com; Bengen,
  Trinity, Morningstar, Early Retirement Now, Pfau, Mr. Money Mustache,
  Gal & McShane, Fidelity, Fed SHED, Vanguard, Dynan et al., MoneyHelper,
  CFPB, Thaler & Benartzi, Arkes, Milkman & Beshears; ESMA, Chague et al.,
  Barber & Odean, BIS, FTC cases and Consumer Sentinel, Jungle Scout, BLS,
  CB Insights, Linktree, Sensor Tower; Indeed Hiring Lab, Deel, Remote,
  Oyster, OECD commentary via intermediaries, visa pages via law-firm
  summaries, EFTA, e-Residency, Stripe Atlas via intermediaries, island.is
  health and pension pages, GitLab handbook source; Stack Overflow 2025
  survey, US Chamber 2025, McKinsey State of AI, Levels.fyi via pin.com.
  Full lists, per file, in each reference and in `references/sources.md`.

## Supporting evidence

- Verified quotes: "$129 founder price (first 30 days), $239 after — yours
  forever."; "After the included 24 months, an optional $19/yr keeps
  updates coming"; "Built on the KMotion libraries with Dynomotion's
  permission"; Anthropic Sonnet 5 "$2/$10 ... is now the standard price";
  Apple "a reduced commission rate of 15% on paid apps and Apple In-App
  Purchases"; the plugin directory README's silence on any paid mechanism.
- Snippet-level quotes carried with their URLs in every reference file;
  the direction of every base rate is consistent across at least two
  independent sources, which is what the skill leans on when it says no.
- The calculator's self-test reproduces Mr. Money Mustache's published
  rows (10 % → 51 years, 50 % → 17 years) from the closed-form formula and
  checks a 24-payment annuity against the annuity formula to within a few
  króna.

## Assumptions

- Tenis is an Icelandic citizen or otherwise holds EEA free-movement
  rights (the relocation file says so where it matters).
- The private snapshot will live at `~/.preiss/finance/` on his machines;
  any other location works if the skill is told.
- The eval prompts' figures are invented and do not describe his finances.
- A 3.25-3.5 % withdrawal rate is the prudent planning default for a
  globally invested Icelander with a long horizon; 4 % is the optimistic
  case.

## Unverified points

- Everything labelled [S] or [SR] in the references — in particular Stripe's
  Iceland status on stripe.com itself, every Skatturinn 2026 figure, the
  ehf residency exemption's exact wording, the visa thresholds, every
  vendor price except HelmCNC's, MicroConf's distribution, Acquire.com's
  multiples, and the founders' revenue figures.
- The corporate tax rate of 20 % and the 183-day framing of Icelandic
  residence are inference; Skatturinn's own wording is "six months or
  longer in a twelve-month period".
- Whether a merchant of record removes the Icelandic VAT-registration
  burden for foreign B2C software sales — an accountant question.
- The Windows junction and snapshot-path steps in the bootstrap doc.

Confidence: **High** that the structure is right — the phase model, the
ladder, the idea test and the calculator encode what the evidence
consistently says, and the skill cannot invent numbers because it reads
them from a snapshot or asks. **Medium** on individual figures until the
upgrade pass runs; **Low** on anything Icelandic that only a secondary
site reported (reiknað endurgjald amounts, current bank rates).
