# Iceland: the money rules that shape every decision

Researched 2026-09-19 from a cloud sandbox whose egress proxy refused every
`.is` domain and every tax-summary site, so **nothing in this file was read
on the source page**. Labels: **[S]** snippet - the claim appeared in a
search result attributed to the URL given; **[I]** inference - reasoning
from those snippets or prior knowledge; **[G]** gap. There are no **[V]**
(verified) rows here yet. Before a number is acted on, open the primary
page from a machine that reaches `.is` (main-pc or the laptop) and upgrade
the label in `sources.md`. Tax, legal and immigration specifics go to a
licensed adviser before any filing or move; this file gets him to that
meeting prepared.

Contents: 1 legal form · 2 VAT · 3 personal tax and self-employed levies ·
4 ehf tax and dividends · 5 rates, indexation, inflation · 6 debt help and
limitation · 7 leaving Iceland · 8 cost of living · 9 payments from Iceland ·
10 questions for the accountant · 11 sources

## 1. Legal form: einstaklingsrekstur vs ehf

| Item | Value | Label | Source |
|---|---|---|---|
| ehf minimum share capital | ISK 500,000; one founder is enough | [V 2026-09-20] | skatturinn.is/fyrirtaekjaskra/stofnun-felaga/einkahlutafelog/ |
| ehf registration fee | ISK 140,500 (changes yearly - verify) | [V 2026-09-20] - "Stofnun einkahlutafélags (ehf.) kr. 140.500" on the fyrirtækjaskrá gjaldskrá, read on the page (the verklagsreglur page carries no fee) | skatturinn.is/fyrirtaekjaskra/gjaldskra/ |
| Sole trader | no share capital, no registration fee; registered by notifying Skatturinn (VAT and withholding registers); business result filed with the personal return (RSK 4.11) | [I] | skatturinn.is "Einstaklingsrekstur" (not opened) |
| ehf duties | separate corporate return and annual accounts (ársreikningur) filed with ársreikningaskrá; deadline, fee and penalties not found | [I]/[G] | - |

When an ehf is worth it [I]: limited liability, and profit above the owner's
reiknað endurgjald taxed at corporate rate plus 22 % dividend tax instead of
up to 46.29 % personal rates - but the fee, the annual accounts, an
accountant, and the 20/50 dividend rule (§4) eat the benefit at low
profits. With debt and thin profit, the sole-trader form is the default
until the numbers say otherwise; the accountant decides (§10).

## 2. VAT (virðisaukaskattur)

| Item | Value | Label | Source |
|---|---|---|---|
| Registration threshold | ISK 2,000,000 taxable turnover in any 12 months | [V 2026-09-20] | skatturinn.is/english/companies/value-added-tax/ (2,000,000 on the page) |
| Rates | 24 % standard, 11 % reduced | [V 2026-09-20] for 24 %; 11 % [S] | skatturinn.is/english/companies/value-added-tax/; avalara.com, quaderno.io |
| Services used abroad by foreign customers | zero-rated / exempt (export of services); "computer services, data processing and information provision" are on the list (Act 50/1988 Art. 12) | [S] | grantthornton.global Iceland indirect tax; skatturinn.is skattskylda-og-skattprosentur; althingi.is/lagas/nuna/1988050.html |
| Digital services to EU consumers | Iceland is outside the EU, so an Icelandic seller is a non-EU business and registers for EU VAT via the non-Union OSS from the first sale; the EUR 10,000 micro-threshold is for EU-established sellers only | [S] | getmyvat.com, support.taxually.com |
| Practical consequence | a merchant of record (Freemius, Paddle, Lemon Squeezy) becomes the seller and carries EU/US sales-tax duties; whether that also removes the Icelandic VAT-registration burden for foreign B2C software sales is an accountant question | [I]/[G] | - |

## 3. Personal income tax 2026 and the self-employed levies

| Item | Value | Label | Source |
|---|---|---|---|
| Bracket 1 | 31.49 % up to ISK 498,122 / month | [V 2026-09-20] | skatturinn.is/einstaklingar/stadgreidsla/skattthrep/2026/ |
| Bracket 2 | 37.99 % up to ISK 1,398,450 / month | [S] | same |
| Bracket 3 | 46.29 % above | [V 2026-09-20] | same |
| Personal tax credit (persónuafsláttur) | ISK 72,492 / month, ISK 869,898 / year | [V 2026-09-20] monthly figure; yearly [I] | skatturinn.is/einstaklingar/stadgreidsla/stadgreidsla/2026/ |
| Indexation of thresholds 2026 | +5.5 % (CPI 4.5 % + productivity add-on) | [S] | stjornarradid.is 2025-12-23 Skattabreytingar 2026 |
| Split of the combined rates | state 16.55 / 23.05 / 31.35 % plus average municipal tax (útsvar) about 14.9-15 % | [I] | skatturinn.is/einstaklingar/helstutolur/2026/ (not opened) |
| Capital income tax (dividends, interest, gains) | 22 % | [V 2026-09-20] - "er 22% frá og með 1. janúar 2018" on Skatturinn's dividends page for individuals, read on the page (the business fjármagnstekjuskattur page and the individuals' overview carry no rate) | skatturinn.is/einstaklingar/fjarmagnstekjur/ardur/; PwC |
| Tryggingagjald (social security contribution) | 6.35 % of wages / reiknað endurgjald | [V 2026-09-20] | skatturinn.is tryggingagjald; freelancepay.is |
| Mandatory pension | 15.5 % minimum (4 % employee + 11.5 % employer); a self-employed person pays all 15.5 % on the reiknað endurgjald; ages 16-70 | [S] | sa.is lífeyrissjóður; althingi.is 152/s/1033 |
| Reiknað endurgjald | the minimum monthly "salary" a self-employed person or working owner must report, by occupational class A-H; licensed-trade craftsmen are class D; specialists incl. IT consultants class A | [S] | skatturinn.is reiknad-endurgjald/2026/; island.is stjornartidindi |
| Class D guideline 2026 | ISK 589,000-969,000 / month by size of operation (single secondary source; a one-person shop is normally the lowest sub-class) | [V 2026-09-20] for 589,000 (on skatturinn.is reiknað endurgjald 2026); upper figure and sub-class mapping [S] | skatturinn.is/atvinnurekstur/stadgreidsla-og-reiknad-endurgjald/reiknad-endurgjald/2026/; new.freelancepay.is |
| Class A guideline 2026 | not found | [G] | - |

Worked illustration [I], not advice: a sole trader with ISK 600,000 of
monthly profit pays about 31.49 % income tax after the 72,492 credit
(~116,000), plus 6.35 % tryggingagjald (~38,000) and 15.5 % pension
(~93,000, which is savings, not tax) on the reiknað endurgjald. The
`rate` command's `--tax` input should carry the tax and contributions, not
the pension; the pension is a forced savings line in the burn.

## 4. ehf: corporate tax, dividends, the 20/50 rule

| Item | Value | Label | Source |
|---|---|---|---|
| Corporate income tax | "no change" for 2026; 20 % is prior knowledge (21 % applied to income year 2024 only) | [S] for "no change", [I] for 20 % | stjornarradid.is 2025-12-23; PwC (blocked) |
| Dividend withholding | 22 % on domestic dividends to individuals; 20 % to foreign legal entities | [S] - same page, "22" not in its text 2026-09-20 | skatturinn.is fjarmagnstekjuskattur |
| 20/50 rule | a working shareholder on reiknað endurgjald who takes dividends above 20 % of the company's taxable equity at year-end has half of the excess taxed as wages (with tryggingagjald) and half as dividends | [S] | skatturinn.is/einstaklingar/fjarmagnstekjur/ardur/; Deloitte Legal 2026 booklet |
| Combined burden on profit paid out | 20 % + 22 % of the remaining 80 % = 37.6 %, versus 31.49-46.29 % on salary: the ehf wins only for profit that would land in the upper brackets, and only up to the dividend ceiling | [I] | - |

## 5. Interest rates, indexation, inflation (why the debt order matters)

| Item | Value | Label | Source |
|---|---|---|---|
| Central Bank key rate | 8.00 % after +0.25 on 19 Aug 2026 (vote 4-1); path 7.25 % (Feb) → 7.50 % (18 Mar) → 7.75 % (May, inferred) → 8.00 % (Aug) | [V 2026-09-20] for 8.00 %, the +0.25 and the 4-1 vote - "hækka vexti bankans um 0,25 prósentur. Meginvextir bankans, vextir á sjö daga bundnum innlánum, verða því 8,00%. Fjórir nefndarmenn studdu þessa ákvörðun en einn vildi halda vöxtum óbreyttum." in the yfirlýsing of 19 Aug 2026, read on the page; the earlier path stays [S], May step [I] | sedlabanki.is/frettir-og-utgefid-efni/grein/yfirlysing-peningastefnunefndar-19-agust-2026; sedlabanki.is yfirlýsing 2026-02-04, 2026-03-18; dv.is 2026-08-19 |
| Inflation | 12-month CPI 5.3 % in July 2026 (5.2 % June); target 2.5 %; above 5 % all year; August figure not found | [V 2026-09-20] for July 5.3 %; rest [S] | hagstofa.is vísitala neysluverðs í júlí 2026; mbl.is 2026-07-23 |
| Overdraft and credit-card revolving rate | Arion 15.25 % after the March 2026 hike; Íslandsbanki +0.25 pp the same month; after August likely ~15.5 % | [V 2026-09-20] for Arion 15.25 % (visir.is); August level [I] | visir.is 2026 "bankarnir byrjaðir að hækka vexti"; bank price lists (not opened) |
| Indexed (verðtryggð) loans | the principal follows the CPI: each month's inflation is added to the balance (verðbætur) rather than paid, so payments start low, the balance grows with inflation and equity builds slowly; non-indexed loans carry a higher nominal rate on a fixed principal | [S] | arionbanki.is verðtryggð lán; landsbankinn.is; support.aurbjorg.is |

Debtor implication [I]: at 5 %+ inflation an indexed balance drifts up about
5 % a year before any repayment. The `debt` command compares debts on
interest **plus** `index_rate`, so a "cheap" 3.5 % indexed loan at 5 %
indexation ranks like an 8.5 % loan. Overpaying an indexed loan, or
refinancing to non-indexed once the rate environment allows, removes the
drift; a 15 % overdraft still comes first.

## 6. Debt help, limitation periods, collection

| Item | Value | Label | Source |
|---|---|---|---|
| Greiðsluaðlögun (debt mitigation, Act 101/2010) | for an individual who shows they are, or foreseeably will be, unable to meet obligations; application to Umboðsmaður skuldara (UMS), which gathers debts, assets, income and conduct before authorising | [S] | althingi.is/lagas/nuna/2010101.html; island.is/greidsluadloegun |
| Cost of UMS help | free (Act 100/2010); UMS tel. 512 6600 per island.is | [V 2026-09-20] for "free" (Act text); phone [S] | althingi.is/lagas/nuna/2010100.html |
| Business owners | Act 101/2010 restricts mitigation for persons in business - broadly only where business debts are a small part of the total or the business has ceased; ehf debts are the company's unless personally guaranteed, and guarantees count in the individual's mitigation | [I] | Act 101/2010 Art. 2 (not opened) - verify with UMS |
| Limitation (Act 150/2007) | general claims 4 years; money loans, bonds and securities-depository claims 10 years; judgment claims 10 years; interrupted by acknowledgement or legal action | [V 2026-09-20] for the 10-year rule (Act text); 4-year rule [S]; judgment/interruption [I] | althingi.is/lagas/nuna/2007150.html; skemman.is/handle/1946/20217 |
| Collection law (Innheimtulög 95/2008), maximum collection costs, wage attachment | not found | [G] | - |

Practical order [I]: talk to the creditor **before** a payment is missed (a
rescheduled minimum costs less than default interest and collection fees);
UMS is a free second opinion long before it is a last resort; a personal
guarantee on a business debt is personal debt for the plan.

## 7. Leaving Iceland

| Item | Value | Label | Source |
|---|---|---|---|
| Tax residence | follows domicile/registration; more than 183 days in any 12 months creates residence; a former resident stays **fully tax-liable for 3 years after leaving unless they prove they became taxable in another country** (a general rule, not a low-tax-country rule) | [V 2026-09-20] for the 3-year rule (both pages); 183-day part [I] | taxsummaries.pwc.com/iceland/individual/residence; skatturinn.is/english/individuals/tax-liability/ |
| Exit tax on individuals | none found; Iceland is not on IFC Review's list of EU states with individual exit taxes (and is not in the EU); corporate exit rules on asset transfers exist and were not checked | [I] | ifcreview.com 2026-05 |
| ehf when the owner moves | the managing director and at least half the board must be resident in Iceland, **but the requirement does not apply to EEA/EFTA nationals or persons resident in the EEA** (Act 138/1994 Art. 42, amended 2017); the minister may grant exemptions | [V 2026-09-20] (Act text names the EEA) | althingi.is/lagas/nuna/1994138.html; althingi.is/altext/stjt/2017.025.html |
| Implication | Spain or Portugal keeps a one-person ehf compliant on residency; Thailand would need an exemption or a resident director; separately, if management sits abroad the company may become tax-resident there under that country's rules | [I] | - |
| Double tax treaties | about 44 treaties, including Spain, Portugal and the USA (US treaty signed 2007, in force 2009); none found with Thailand | [S], Thailand [I] | government.is double-taxation-treaties; skatturinn.is/english/companies/double-taxation-conventions/ |
| Iceland's own remote-worker visa (context, for non-EEA nationals coming in) | income ≥ ISK 1,000,000 / month (1,300,000 with partner), up to 180 days, not renewable, health insurance ≥ ISK 2,000,000 | [S] secondary | settlednomad.com, movingtoiceland.com (utl.is not reachable) |

The "leave properly" checklist [I]: deregister with Þjóðskrá, prove tax
residence in the new country from day one (registration, lease, local tax
number), keep the ehf's management facts consistent with where he lives,
and get the 3-year rule interpreted by the adviser before the move, not
after. `references/remote-and-relocation.md` covers the receiving side.

## 8. Cost of living (crowd-sourced - Numbeo, treat as rough)

| Comparison | Value | Label | Source |
|---|---|---|---|
| Reykjavík → Lisbon | ISK 1,100,000 / month in Reykjavík ≈ ISK 681,368 (EUR 4,696) in Lisbon for the same standard, i.e. Lisbon ~38 % cheaper including rent | [S] | numbeo.com compare Reykjavik/Lisbon (Aug-Sep 2026) |
| Lisbon → Bangkok | Bangkok 27.7 % cheaper excluding rent, 37.8 % including rent (so very roughly 60 % cheaper than Reykjavík including rent, by chaining) | [S], chaining [I] | numbeo.com compare Lisbon/Bangkok |
| Valencia, Chiang Mai | not found | [G] | - |

Cost of living is the second lever on the FI number after income: the same
`fi` run with Lisbon-level spending shortens the horizon by years. Model it
with real rent quotes, not Numbeo, before deciding.

## 9. Payments and checkout from an Icelandic business

| Platform | Iceland | Label | Source |
|---|---|---|---|
| Stripe | **not on stripe.com/global's list of supported merchant countries** (51 entries on 2026-09-20, five of them "Extended network" and two "Preview"; Denmark, Finland, Norway, Sweden, Estonia are on it); ISK appears only as a presentment currency, which is not merchant availability; stripe.com/global fetched 2026-09-20 from main-pc: no "Iceland" in the page text, nor anywhere in the raw HTML; the country list is in the served HTML, not script-rendered - Denmark, Estonia, Finland, Liechtenstein, Norway and Sweden are all on it (read 2026-09-20) | [V 2026-09-20] absence, read in the served HTML (the earlier "46 countries" was a secondary source's count; the page itself lists 51 entries, 44 without the extended-network and preview ones) | stripe.com/global; dodopayments.com stripe-supported-countries; rapyd.net blog |
| PayPal (receiving as a merchant) | reported unavailable to Icelandic businesses (forum, weak) | [S] weak | community.shopify.com thread 327112 |
| Rapyd (ex-Valitor), Teya (ex-SaltPay/Borgun) | local card acquiring for Icelandic merchants | [S] | rapyd.net/network/country/iceland; radgreidslur.borgun.is |
| Lemon Squeezy (merchant of record) | Iceland listed for bank payouts | [V 2026-09-20] | docs.lemonsqueezy.com supported-countries |
| Payoneer | Iceland listed as supported | [V 2026-09-20] | payoneer.custhelp.com a_id/45754 |
| Wise | personal accounts opened for Iceland residents; Wise Business for Icelandic companies not confirmed (wise.is is an unrelated Icelandic IT firm) | [S], business [G] | wise.com/is |
| Paddle, Freemius | market themselves as Stripe alternatives / merchant of record; Iceland seller eligibility not confirmed (HelmCNC already sells through Freemius, so Freemius payouts to Iceland are working in practice - Tenis's own record, not this research) | [G] | paddle.com/alternatives/stripe |

Consequence [I]: a standard Stripe account is not the default for an
Iceland-registered seller. The working pattern is a merchant of record
(Freemius for licensed software, Lemon Squeezy or Paddle for SaaS and
digital goods), which also carries EU VAT; a foreign entity only to get
Stripe is a tax-residency decision, not a payments decision.

## 10. Questions for the accountant (one meeting, prepared)

1. Sole trader or ehf at the profit level the snapshot shows, given the
   20/50 rule, the ISK 500,000 capital and the annual-accounts cost?
2. Which reiknað endurgjald class and sub-class apply to a one-person shop
   that also sells software, and what minimum does that fix for 2026?
3. VAT treatment of software licences and SaaS sold to foreign consumers
   through a merchant of record - is Icelandic VAT registration still
   needed for those sales, and how are Freemius payouts booked?
4. Are any business debts personally guaranteed, and how would
   greiðsluaðlögun treat them?
5. If he moves inside the EEA: the 3-year tail, where the ehf becomes
   tax-resident, and what to file in the year of leaving.

## 11. Sources (search-result URLs; none opened this session)

Primary: skatturinn.is (skattþrep 2026, staðgreiðsla 2026, helstu tölur
2026, reiknað endurgjald 2026, tryggingagjald, fjármagnstekjuskattur,
arður, VAT english, tax-liability english, double-taxation conventions,
fyrirtækjaskrá ehf pages, greiðsluaðlögun); stjornarradid.is
Skattabreytingar 2026 (2025-12-23); government.is double-taxation
treaties; sedlabanki.is MPC statements 2026-02-04, 2026-03-18, 2026-08-19;
hagstofa.is CPI June 2026; althingi.is Acts 100/2010, 101/2010, 150/2007,
138/1994, 50/1988 and amendment 25/2017; island.is greiðsluaðlögun and
stjórnartíðindi; numbeo.com city comparisons.
Secondary: taxsummaries.pwc.com Iceland; KPMG Iceland tax booklet Jan
2026; Deloitte Legal booklet 2026; new.freelancepay.is; sa.is; stripe.com
Iceland VAT guide; anrok.com; avalara.com; grantthornton.global;
getmyvat.com; taxually.com; dv.is; mbl.is; visir.is; arionbanki.is;
landsbankinn.is; aurbjorg.is; ifcreview.com; expatmodo.com;
settlednomad.com; movingtoiceland.com; dodopayments.com; rapyd.net;
docs.lemonsqueezy.com; payoneer.custhelp.com; wise.com; paddle.com;
community.shopify.com.

Blocked this session: skatturinn.is, rsk.is, island.is, government.is,
sedlabanki.is, ums.is, stripe.com, docs.stripe.com, taxsummaries.pwc.com,
kpmg.com, wikipedia.org, tradingeconomics.com, numbeo.com.
