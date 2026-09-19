# Remote work and relocation: the bridge income that survives a move

Researched 2026-09-19. Every official page (immigration sites, OECD,
Skatturinn, island.is, Deel, Remote, Stripe, Paddle, GitLab's handbook)
was refused by the sandbox proxy, so every claim is **[S]** snippet
(search-result text attributed to the URL; page not opened) or **[I]**
inference; **[G]** gap. Confirm each threshold on the official page before
it is acted on, and take the tax questions to a licensed adviser. The
Icelandic side of leaving is in `iceland.md` §7.

Contents: 1 the remote job market · 2 how companies hire abroad ·
3 visas and EEA free movement · 4 tax residency · 5 cost of living and
nomad data · 6 payments and banking · 7 where to put the company ·
8 health and pensions · 9 what remote employers need from him ·
10 the move, in order · 11 sources

## 1. The remote job market

| Finding | Value | Label | Source |
|---|---|---|---|
| Indeed Hiring Lab UK, mid-year 2026 | "The share of UK job postings mentioning remote or hybrid working arrangements was 16.9% as of end-June", described as stable | [S] | hiringlab.indeed.com 2026-08-03 |
| Indeed's open remote tracker | "Share of job postings containing remote/hybrid work-related terms" - the primary trend source | [S] | github.com/hiring-lab/remote-tracker |
| Aggregator claims 2026 | "36% of new job postings include some remote component (24% hybrid, 12% fully remote)"; US "only 6% are fully remote"; "55% of Fortune 100 companies now mandating a five-day office week"; a claimed "6.8% wage premium" for fully remote | [S] unattributed, low confidence | roberthalf.com; remotive.com; amraandelma.com |
| Share of "remote worldwide" vs "remote in one country" listings on Remote OK, We Work Remotely, Working Nomads, Wellfound | not obtained | [G] | - |

Read [I]: fully remote roles are a minority and shrinking at large US
employers; the reachable market for someone in Iceland is the company
that already hires cross-border, usually as a contractor (§2), plus
platforms that specialise in vetted contract work (§9). The job boards
themselves must be checked for "worldwide" vs "US only" one by one.

## 2. How companies hire people abroad

| Item | Value | Label | Source |
|---|---|---|---|
| Employer-of-record fees | Deel "$599 per employee per month"; Remote.com "699 USD per employee per month" ($599 on annual commitment); Oyster "USD 699 per employee per month" | [S] third-party trackers; official pages not opened | pin.com; eorhq.com; gloroots.com; support.remote.com |
| On top of the fee | "employer taxes, 13th-month pay, and FX fees often adding 20-50% or more"; "13-40% on top of gross pay" | [S] | same |
| Contractor management | Deel "the platform lists it as free while multiple third-party sources cite $49 per contractor per month"; a "Contractor of Record" tier at $325/month | [S] conflicting | same |
| Permanent establishment (PE) | "A single employee working from a home office or co-working space in the wrong jurisdiction for too long can create obligations for corporate income tax, payroll filings, and penalties."; dependent agent: "If your remote employee concludes contracts or generates revenue in the host country, they could be deemed a dependent agent" | [S] | remote.com PE posts; kpmg.com/ch; ogletree.com |
| OECD Nov-2025 commentary update (reported) | "If an employee spends less than 50% of their working hours at a foreign workplace over a 12-month period, remote work is unlikely to result in a PE." | [S] verify against OECD text | centuroglobal.com; countrytaxcalc.com |

What it means [I]: employing him abroad costs a company ~$7-8k a year in
platform fees plus 20-50 % on-costs and a PE worry; contracting with his
own entity costs them $0-49 a month and no PE fear. "Contractor invoicing
from his own business" is the door, and it is the same door whether he is
in Reykjavík or Lisbon. That also decides the pitch: a business, an
invoice, a scope - not a CV.

## 3. Visas, and why an Icelander mostly does not need one

| Country, scheme | Income threshold (2026, as reported) | Duration | Label | Source |
|---|---|---|---|---|
| **EEA (Icelandic citizen)** | none - free movement: "the same right as EU citizens to take up an economic activity anywhere in the EU/EEA"; beyond three months, residence is conditional on not being "an undue burden" and holding "comprehensive health insurance" | indefinite | [S], conclusion [I] | efta.int; government.is EEA pages; Wikipedia Citizens' Rights Directive |
| Spain, Startup Act teleworker visa (non-EU) | "EUR 2,849 per month (EUR 34,188 per year, 200% of Spain's minimum wage)"; "No more than 20% of your income can come from Spanish sources" | not captured | [S] | vissumlex.com; startupvisa.barcelona |
| Portugal, D8 (non-EU) | "the minimum D8 Visa income requirement threshold €3,680 per month" (4 × €920); +50 % spouse, +30 % per child | not captured | [S] | globallawexperts.com; remoteworkeurope.eu |
| Estonia, Digital Nomad Visa (non-EU) | "€4,500 gross monthly income over the prior six months" (raised from €3,504) | not captured | [S] | jobbatical.com |
| Croatia | "EUR 3,622.50/month (or EUR 43,470 in savings for 12 months)"; "extended to 18 months ... cannot be renewed"; foreign income exempt from Croatian tax | 18 months | [S] | croatiaimmigrationadvisory.com |
| Italy (non-EU) | "€28,000 (US$30,300) per year"; health cover ≥ €30,000 | 1 year, renewable | [S] | citizenremote.com |
| Greece | "€3,500" net/month; consulate-only since Feb 2026 (Law 5275/2026) | 12 + 12 months | [S] | remoteworkeurope.eu |
| Malaysia, DE Rantau | "US$24,000 annually" | 12 + 12 months | [S] | asialifestylemagazine.com |
| Thailand, DTV | "minimum bank balance of 500,000 baht ... valid for five years"; 180 days per entry, one extension | 5 years multi-entry | [S] | thethaiger.com; dtv.in.th |
| Japan | "at least 10 million Japanese yen" a year | 6 months, not renewable in-country | [S] | Asia comparison pages; mofa.go.jp blocked |

Read [I]: Spain and Portugal need no visa for him; the thresholds above
matter only as a signal of what those countries consider a self-supporting
remote income (roughly EUR 2,850-3,700 a month), a useful floor for the
`rate` command. Outside the EEA, Thailand's DTV is a deposit test, not an
income test; Japan and Estonia are the expensive ones.

## 4. Tax residency

| Item | Value | Label | Source |
|---|---|---|---|
| Iceland, becoming resident | "If the stay in Iceland is six months or longer in a twelve-month period, the individual is considered to be a resident of Iceland" (unlimited liability from arrival) | [S] | skatturinn.is/english/individuals/tax-liability/ |
| Iceland, leaving | "Former residents remain subject to unlimited tax liability for 3 years after leaving the country, unless they prove that they have become subject to taxation in another country." | [S] | KPMG TIES Iceland Jan 2025; PwC; Skatturinn |
| OECD Model Art. 4(2) tie-breaker for dual residents | "four tests in strict sequence: permanent home, centre of vital interests, habitual abode, nationality"; "It is possible to have a permanent home in both countries, which pushes the analysis to the next step." | [S] | ggi.com; innovires.com; dlapiper.com 2021 |
| Centre of vital interests | "family location, primary employment, business oversight, investment management activity, and community ties" | [S] | innovires.com |
| A nomad visa does not settle tax | Croatia's exemption is a domestic carve-out; 183 days is the usual trigger elsewhere | [S] third party | affordwhere.com |

Read [I]: a nomad who keeps a flat, family and the workshop in Iceland
stays Icelandic-resident under a treaty even with 183+ days abroad. To
leave properly: deregister with Þjóðskrá, take up real residence (lease,
local tax number, registration) and get the new country's tax residence
certificate, which is what lifts the 3-year tail. The adviser confirms
the sequence before the first flight, not after.

## 5. Cost of living and nomad data (crowd-sourced, indicative)

- Numbeo 2026: "Reykjavik comes in at number 8 among the most expensive
  cities when looking at the cost of living index without rent included."
  [S: timeout.com 2026-01-26]; Numbeo "measures the price of everyday
  expenses, including rent, relative to New York City (baseline of 100)"
  and is user-entered [S: visualcapitalist.com]. City pairs Reykjavík →
  Lisbon → Bangkok are in `iceland.md` §8; Valencia, Chiang Mai, Tbilisi,
  Buenos Aires, Medellín not captured [G].
- MBO Partners 2025: "In 2025, 18.5 million Americans work as digital
  nomads." [S: x.com/MBOpartners]; "a 153 percent increase since 2019";
  "13% of digital nomads with traditional jobs reported that their employer
  does not know that they are nomadic." [S: pumble.com, sqmagazine.co.uk].
  No income figure captured [G]. Nomad List: "US citizens make up 44% of
  digital nomads on the Nomad List platform." [S].
- Read [I]: cost of living is the second lever on the FI number; the
  employer-doesn't-know pattern is a PE and contract risk, never the plan.

## 6. Payments and banking from abroad

| Platform | Finding | Label | Source |
|---|---|---|---|
| Stripe | "Stripe currently operates in 46 fully supported countries worldwide as of December 2025"; "Stripe does not serve Iceland."; "Stripe doesn't support Iceland, which is a contributing factor to why Shopify Payments is also unavailable in the country." | [S] secondary; stripe.com/global not opened | dodopayments.com; community.shopify.com 206472 |
| "Open a Stripe account in Iceland" workaround pages | exist; treat as a red flag, not advice | [I] | smartbizfreedom.com |
| Paddle (merchant of record) | "5% + $0.50 with no monthly fee"; "can payout to anywhere in the world with exception to sanctioned countries"; possible $15 SWIFT fee | [S] | dodopayments.com; paddle.com/help (not opened) |
| Lemon Squeezy (merchant of record) | "5% + $0.50" plus "1.5% for international transactions, 1.5% for PayPal transactions, 0.5% for subscription payments"; 2026: "Lemon Squeezy + Stripe Managed Payments"; Iceland seller status not captured (a 2021 post lists bank payouts to 79 countries; `iceland.md` §9 has Iceland on the payout list) | [S] | swell.is; lemonsqueezy.com/blog/2026-update |
| Wise Business | "available in selected regions including the UK, EEA, US, Canada ..."; "Wise opens accounts to clients residing in Iceland."; features vary by country; wise.is is an unrelated Icelandic firm | [S] | statrys.com; wise.com/is/availability |
| Payoneer | "does not publish a public list of supported countries" - visible at sign-up | [S] | freemius.com docs; payoneer.com |

Rule [I]: the entity's country decides the payment stack. An Icelandic sole
trader or ehf sells through a merchant of record (Freemius for licences,
Paddle or Lemon Squeezy for SaaS and digital goods) and banks through
Wise Business; a foreign entity to get Stripe is a tax decision (§7).

## 7. Where to put the company

| Option | Finding | Label | Source |
|---|---|---|---|
| Stay a sole trader / ehf where he actually lives | Iceland taxes residents on worldwide income with the 3-year tail; a foreign entity does not change that and adds filings; the entity's country only matters for payments | [I] | from §4, §6 |
| Estonian e-Residency + OÜ | "The state fee to register a private limited company (OÜ) online is €265, while the e-Residency state fee is around €150."; "legal address and contact person service, typically €200-400 per year"; "e-Residency does not make you an Estonian tax resident, though the company itself is an Estonian tax resident"; "0% corporate income tax on profits it keeps ... tax is triggered only when profit is distributed, at a 22/78 rate"; a reported "2% tax surcharge on e-resident board member fees from 2026" | [S] | learn.e-resident.gov.ee; corpenza.com; nomadgate.com; taxravens.com; remoteworkeurope.eu |
| The catch | an OÜ run day to day from his home country risks a permanent-establishment or place-of-management claim there (§2) | [I] | - |
| US LLC via Stripe Atlas (non-resident) | "your home country may tax the income."; "file IRS Form 5472 (informational return) and a pro-forma 1120 annually. Penalty for non-filing: $25,000."; Atlas fee not captured | [S] | taxhavendirectory.com; myfreetaxamerica.com; docs.stripe.com/atlas blocked |

Read [I]: none of the foreign-entity routes reduces his tax while he is
tax-resident in Iceland or another EEA state; they are payment plumbing
with filing risk. Not before phase 4, and then only with the adviser.

## 8. Health insurance and pensions when abroad

- "The European Health Insurance Card entitles you to healthcare in other
  EEA countries, the United Kingdom and Switzerland."; "only valid for
  services that are within the public health insurance system" - temporary
  stays only [S: island.is EHIC pages].
- "If you move from Iceland you are no longer covered by the social
  security legislation in Iceland. However, any pension entitlement that
  you may have earned will remain in effect." [S: island.is health
  insurance upon transfer; norden.org]
- "If you are employed in another EEA country, the general rule applies
  that you will fall under the social security legislation of the country
  to which you move"; "Pension rights accrued by EEA nationals in Iceland
  ... are protected under the relevant rules of Regulation 883/2004" [S:
  island.is; lifeyrismal.is]; state pension already in payment continues,
  "social payments are canceled" [S: norden.org].
- Read [I]: a move ends Icelandic health cover on departure; private or
  local public cover must start the same day; earned pension rights stay
  and each fund is asked in writing about export.

## 9. What remote employers and clients need from him

GitLab's all-remote handbook [S: gitlab.com content-sites handbook;
handbook.gitlab.com]: "mastering asynchronous workflows is vital to avoiding
dysfunction and enjoying outsized efficiencies and lifestyle flexibility";
"requires a mental shift that can feel unusual or even uncomfortable for
those who come from a colocated environment"; "effective asynchronous
communication requires enough context, clear language, appropriate
resources, and a record that can be found later"; "people should be able
to do their work without getting interrupted by chat"; "look it up in the
handbook" before asking [S third-party: workinvirtual.com].

Read [I]: he already works this way - HELMCNC_NOTES, HANDOFF.md, the
tracker, the employee's reports. The portfolio for a remote contract is
those artefacts plus HelmCNC itself: a shipped, licensed, safety-tested
product with a self-test suite is a stronger proof than any interview.

Contract platforms (from `software-and-ai.md`): Braintrust "charges a 15%
flat fee of the total amount the client pays ... freelancers keep 100%";
Toptal "algorithmic interviews, live coding, and test projects" and a
client deposit; Mercor "uses an AI interviewer" [S].

## 10. The move, in order (all [I])

1. Income first: a contract or retainer that is explicitly location-free,
   invoiced from his own entity, signed before any lease abroad.
2. Adviser meeting with `iceland.md` §10 plus: the 3-year tail, the ehf's
   management location, VAT on services from the new country.
3. Real residence in the new country: lease, registration, tax number,
   residence certificate; Þjóðskrá deregistration the same month.
4. Health cover from day one; pension funds asked about export in writing.
5. Payments: merchant of record and Wise Business set up before leaving,
   tested with one real sale.
6. The workshop: what stays, who runs it, or how it winds down - decided on
   paper, with the CRM's open jobs closed or handed over.
7. Re-run `plan` with the new country's real rent and the new tax rate.

## 11. Sources (search-result URLs; none opened)

hiringlab.indeed.com 2026-08-03; github.com/hiring-lab/remote-tracker;
roberthalf.com; remotive.com; breeze.pm; distantjob.com; amraandelma.com;
pin.com/blog/deel-pricing; eorhq.com guides; gloroots.com;
whichpayroll.com; support.remote.com 37480463833229; oysterhr.com/pricing;
remote.com PE posts; kpmg.com/ch; ogletree.com; centuroglobal.com;
countrytaxcalc.com; vissumlex.com; startupvisa.barcelona;
nimextranjeria.com; globallawexperts.com; remoteworkeurope.eu;
citizenremote.com; jobbatical.com; croatiaimmigrationadvisory.com;
globalcitizensolutions.com; movingto.com; visasupdate.com;
asialifestylemagazine.com; kerja-remote.com; timeout.com/asia;
thethaiger.com; dtv.in.th; greenbacktaxservices.com; efta.int;
government.is EEA pages; en.wikipedia.org Citizens' Rights Directive;
skatturinn.is tax-liability; taxsummaries.pwc.com; KPMG TIES Iceland PDF
(Jan 2025); ggi.com; innovires.com; dlapiper.com; affordwhere.com;
timeout.com 2026-01-26; numbeo.com; visualcapitalist.com;
x.com/MBOpartners; pumble.com; sqmagazine.co.uk; dodopayments.com;
redstagfulfillment.com; community.shopify.com 206472;
smartbizfreedom.com; paddle.com/help; swell.is; lemonsqueezy.com
2026-update; docs.lemonsqueezy.com; statrys.com; alexontrading.com;
wise.com/is/availability; freemius.com docs; payoneer.com;
learn.e-resident.gov.ee; corpenza.com; taxhavendirectory.com;
nomadgate.com; blog.wamo.io; taxravens.com; myfreetaxamerica.com;
rapidr.io; edge-docs.stripe.com/atlas; island.is EHIC and transfer pages;
norden.org; lifeyrismal.is; eftasurv.int letter of formal notice;
gitlab.com handbook source; handbook.gitlab.com/handbook/communication;
workinvirtual.com.
Blocked: stripe.com, docs.stripe.com, deel.com, remote.com, oysterhr.com,
e-resident.gov.ee, learn.e-resident.gov.ee, mup.gov.hr, mofa.go.jp,
mdec.my, europa.eu, handbook.gitlab.com, paddle.com, lemonsqueezy.com,
mbopartners.com, taxsummaries.pwc.com, numbeo.com, weworkremotely.com,
buffer.com, island.is, efta.int, vistos.mne.gov.pt, wise.com, politsei.ee.
Gaps: visa durations for Spain, Portugal, Estonia; remote-worldwide share
on the boards; Stripe's own list; Lemon Squeezy and Payoneer Iceland
eligibility from their pages; Numbeo city indices; Deel contractor fee;
OECD text; Þjóðskrá deregistration mechanics; Japan's launch date.
