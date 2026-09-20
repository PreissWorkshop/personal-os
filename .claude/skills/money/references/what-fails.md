# What fails: base rates, regulator cases, and the red flags

Researched 2026-09-19. Only developer.apple.com could be opened; ESMA,
SSRN, BIS, FTC, BLS, CFPB, CB Insights, Jungle Scout, Sensor Tower, Gumroad,
TechCrunch and Google were all refused by the sandbox proxy. Labels:
**[V]** verified (page opened) · **[S]** snippet (search-result text
attributed to the URL; page not opened) · **[I]** inference · **[G]** gap.
Every [S] number is "probably right, re-verify before the skill states it
as fact"; the direction of every finding is consistent across sources,
which is what the skill relies on when it says no.

Contents: 1 base-rate table · 2 speculation · 3 business-opportunity and
guru schemes · 4 MLM · 5 dropshipping and Amazon · 6 startups · 7 creators,
courses, "passive income" · 8 app stores · 9 AI wrappers · 10 credit traps ·
11 the red-flag checklist · 12 how to answer "is this course worth it" ·
13 sources

## 1. Base-rate table

| Activity | Share that lose or fail | Population and caveat | Source, label |
|---|---|---|---|
| Retail CFD/forex trading (EU) | "74-89% of retail accounts typically lose money on their investments, with average losses per client ranging from €1,600 to €29,000." | regulator-collected broker data 2017-18; mandated warning "Between 74-89% of retail investor accounts lose money when trading CFDs" | ESMA 2018 [V 2026-09-20] (esma.europa.eu node/84933 fetched, "74-89%" on it) |
| Day trading for a living (Brazil futures) | "97% of all individuals who persisted for more than 300 days lost money."; "only 1.1% earned more than the Brazilian minimum wage" | all new day traders 2013-15, administrative data; the strongest study here | Chague, De-Losso, Giovannetti 2020, SSRN 3423101 [S] (ssrn.com answers 403 to scripts, 2026-09-20; open in a browser) |
| Active individual stock trading (US) | "those that traded most earned an annual return of 11.4 percent, while the market returned 17.9 percent."; "trading is hazardous to your wealth." | 66,465 households 1991-96 | Barber & Odean 2000, Journal of Finance [S] |
| Retail bitcoin buyers 2015-22 | est. "73-81% of retail investors have likely lost money on their initial investment" | model-based on app downloads, 95 countries; "estimated", not observed P&L | BIS Bulletin 69 (2023) [S] (not on the HTML abstract page, fetched 2026-09-20; check the PDF) |
| MLM distributors (AdvoCare 2016) | "72.3 percent of distributors did not earn any compensation from AdvoCare; another 18 percent earned between one cent and $250" | company data cited by the regulator | FTC 2019 [S] (ftc.gov 403 to scripts, 2026-09-20) |
| MLM (Herbalife) | "A large majority of distributors made little or no money and a substantial percentage lost money" | $200M settlement | FTC 2016 [S] |
| MLM generally | "99.6-99.9% of MLM participants lose money, assuming at least somewhat realistic estimates of attrition ..." | one author's assumptions, not audited; low weight | Taylor, FTC public comment [S] |
| "Done for you" e-commerce and coaching | income claims unsubstantiated; buyers paid $2k-$125k; refunds only via the regulator, years later | four FTC cases 2018-2025 | FTC [S] |
| Business and job-opportunity fraud (US, reported) | "business and job opportunities reported losses totaled $750.6 million—up nearly $250 million from 2023." | reported cases only | FTC Consumer Sentinel 2024 [S] |
| Amazon sellers (surveyed) | "13% said their businesses are not yet profitable."; "just one-third have margins over 20%" | vendor survey of active sellers; quitters absent - an upper bound | Jungle Scout 2025 [S] |
| New US employer establishments | "77.9% of new establishments survive year one, 51.4% survive five years, and 34.7% survive a decade." | payroll establishments only; solo online businesses not counted, almost certainly worse | BLS BED to Mar 2025 via third party [S] (bls.gov 403 to scripts, 2026-09-20) |
| VC-backed startups (post-mortems) | "43% failing due to poor product-market fit, with 29% citing bad timing and 19% citing unsustainable unit economics" (2024 version; earlier versions differ) | self-selected, funded, non-exclusive tags | CB Insights 2024 [S] |
| Full-time creators | "Only 12% of full-time creators make over $50k a year"; "about 4% ... more than $100,000" | vendor survey 2022 | Linktree via TechCrunch [S] |
| App-store publishers | "the top 1 percent of U.S. App Store publishers ... generated approximately 94 percent of all revenue" (2016); ~79 % of new installs (1H 2022) | vendor estimates | Sensor Tower [S] |
| Apple commission | "a reduced commission rate of 15% on paid apps and Apple In-App Purchases" under $1M prior-year proceeds; standard rate above (the page did not state the number) | platform page | Apple Small Business Program [V] |
| Buy-now-pay-later (US 2022) | "Approximately 63 percent of borrowers in 2022 originated multiple simultaneous loans"; 61 % of originations subprime or deep-subprime | regulator data, 145M applications | CFPB Jan 2025 [S] |
| AI-wrapper startups | no credible rate found; "65% churn within 90 days" is a blog claim with no dataset | opinion, not data | [I] |

## 2. Speculation

The four rows above say the same thing from four directions: leveraged
retail trading loses for three in four accounts (ESMA), persistence does
not fix it (Brazil: no evidence of learning), activity itself costs about
6.5 points a year (Barber & Odean), and retail crypto buyers mostly bought
high (BIS: "large and sophisticated investors selling and smaller retail
investors buying"). ESMA's measures were EU-wide; the Icelandic (FME /
Seðlabanki) transposition was not checked [G]. FCA UK crypto consumer
research not obtained [G].

Rule [I]: no trading, no leverage, no crypto as a path out of debt. A
person with a 15 % overdraft already holds the best risk-free investment
available (`fi-and-debt.md` §4).

## 3. Business-opportunity and guru schemes (US FTC cases)

| Case | What the FTC alleged | Label, source |
|---|---|---|
| Ecommerce Empire Builders (complaint Sept 2024, order May 2025) | "In social media ads, EEB claims that its clients can make $10,000 monthly, but the FTC's complaint alleges that the company has no evidence to back up those claims."; "'done for you' online storefronts that cost consumers as much as $35,000"; ~$2,000 training; owner banned from selling business opportunities | [S] ftc.gov 2025-05 (403 to scripts, 2026-09-20) |
| Automators AI (TRO Aug 2023, settlement Feb 2024) | "luring consumers to invest $22 million in online stores using unfounded claims about income and profits"; "initial investments of $10,000 to $125,000, and providing tens of thousands of dollars of additional funding for working capital"; "AI-powered" Amazon/Walmart stores | [S] ftc.gov 2024-02; cnbc.com 2025-03 |
| Digital Altitude (2018) and MOBE (2018) | "falsely claimed its program would enable people to earn 'six figures' in 'ninety days or less'"; "individualized coaching from successful marketers, who in fact were just salespeople selling higher membership levels"; a summary claims ~145,000 buyers and none reached the promise (advocacy-site figure, lower confidence) | [S] ftc.gov 2018; truthinadvertising.org |
| FTC Business Opportunity Rule (16 CFR 437) | disclosure document, waiting period, earnings-claim substantiation - text not obtained | [G] |

Pattern [I]: the seller's income comes from selling the opportunity;
tiers escalate (training → done-for-you → "working capital"); the
technology word of the year is the guarantee; the numbers are never
substantiated; recovery, when it comes, is years later via a regulator.

## 4. MLM

AdvoCare and Herbalife (table above) are the regulator-grade numbers;
Taylor's 99 % is one analyst's model and is cited only as such. The test
[I]: if the plan pays for recruiting or for the distributor's own
purchases rather than sales to outsiders, the distributor is the customer.

## 5. Dropshipping and Amazon FBA

Jungle Scout 2025 (survey 10-27 Jan 2025): "A majority of sellers and SMBs
have profit margins above 10% on Amazon, though just one-third have
margins over 20%."; "13% said their businesses are not yet profitable."
[S: junglescout.com]. The respondents are customers of a paid seller tool;
people who quit are absent, so this is the best case. Quit rates and a
credible margin structure were not obtained [G]. The coaching cases in §3
are the dropshipping evidence that exists: the money was in selling the
stores.

Rule [I]: inventory, platform dependence and thin margins with debt and no
capital - out, and it cheapens the brands.

## 6. Startups

BLS survival (payroll establishments): 22 % gone in year one, 49 % by year
five, 65 % by year ten [S]. CB Insights' post-mortems: cash ran out in
~70 % as the final cause; product-market fit 43 %, timing 29 %, unit
economics 19 % (2024 version; older versions said "no market need 42%" -
say which version) [S]. Read together with `case-studies.md` §3: the
survivors' median is small, the failures are the majority, and the cause
is almost always "no one paid" or "cash ran out first" - both of which the
phase model and the money-not-applause rule in `playbooks.md` §6 address.

## 7. Creators, courses, "passive income"

- Linktree 2022 via TechCrunch: "Only 12% of full-time creators make over
  $50k a year"; "about 4% of global creators are deemed professionals,
  meaning they pull in more than $100,000 a year"; "53% earn under $100
  per brand collaboration" [S].
- Gumroad distribution figures in circulation ("99.5% of all platform
  revenue accrues to the top 1% of creators. The median creator earns $72
  per month.") are third-party and unverifiable - direction only, never a
  statistic [S low reliability: insightraider.com].
- YouTube: RPM is net of YouTube's share; CPM is what advertisers pay per
  1,000 impressions [S third-party]; the 55 % creator share was not
  verified on a Google page [G].
- Read [I]: content is a distribution channel for a product or a service
  (Gadsby, Wood Whisperer, Plausible in the other files), not the income.
  "Passive" income in every verified case was active work with a lag.

## 8. App stores

Apple: 15 % under $1M prior-year proceeds, standard rate above; EU
alternative terms "a further reduced commission of 10%" [V:
developer.apple.com small-business-program]. Sensor Tower: the top 1 % of
publishers take ~79-95 % of revenue and installs [S]. Google Play's fee
page not verified [G]. Read [I]: a consumer app store is a lottery with a
15-30 % ticket price; a desktop tool sold through a merchant of record and
listed in the Microsoft Store at 0 % (`software-and-ai.md`) keeps the
customer relationship.

## 9. AI wrappers

Blogs claim "AI wrapper startups have an average 65% churn rate within 90
days" and that each frontier-lab release kills a category; none has a
traceable dataset, and attributions to "CB Insights and Gartner" could not
be verified [S opinion: machinebrief.com, dev.to]. The mechanism (the
model vendor ships your feature) is real by example; the rate is not.
`software-and-ai.md` §3 has the two solo AI apps with public numbers and
what they sell instead of "AI".

## 10. Credit traps

CFPB, January 2025 (145 million BNPL applications 2017-2022): 63 % of
borrowers stacked simultaneous loans, 33 % across firms; deep-subprime
45 % and subprime 16 % of originations; lenders approved 78 % of subprime
applicants [S: files.consumerfinance.gov cfpb_BNPL_Report_2025_01]. A
regulator source on revolving-credit and payday costs, and the Icelandic
equivalents (Neytendastofa), were not reached [G]. Icelandic overdraft
and card rates are in `iceland.md` §5.

## 11. The red-flag checklist (all [I], synthesised from §3-§4)

1. A specific income number with no substantiation - "$10,000/month",
   "six figures in 90 days". Ask for the typical result and the share of
   buyers who reached it; refusal ends it.
2. Pay before you see data; tiers that escalate (training → done-for-you →
   working capital). The tiers are the product.
3. "Coaching" whose income depends on your next purchase.
4. A technology word used as a guarantee: "AI-powered", "automation",
   "passive".
5. Lifestyle imagery instead of an income disclosure.
6. Earnings that depend on recruiting or on your own purchases.
7. The seller's business is selling the opportunity; ask for their own
   store's audited P&L.
8. Money that is unrecoverable without a regulator - assume 0 % recovery.
9. Platform dependence sold as an asset (a storefront on someone else's
   marketplace, a wrapper on someone else's model).
10. Base-rate blindness in the pitch: a legitimate opportunity survives
    the ESMA / BLS / creator-income conversation; a scheme cannot.
11. Jurisdiction: these are US cases; Iceland's consumer regulator is
    Neytendastofa and EEA unfair-commercial-practice rules apply; nothing
    Icelandic verified [G].

## 12. How to answer "is this course / agency / opportunity worth it"

1. Name the closest regulator case from §3 and the base rate from §1, with
   labels.
2. Run the checklist in §11 against the pitch; count the flags.
3. Price it against the phase: in phases 0-3 no paid course precedes a
   paying customer, full stop.
4. Give the zero-cost version of the same thing this week (for an "AI
   agency" course: sell one narrow automation to one real business he
   already knows - `playbooks.md` §8).
5. No moralising; one sentence on the risk, one on the alternative, the
   numbers in a table.

## 13. Sources

Opened [V]: developer.apple.com/app-store/small-business-program/;
esma.europa.eu/node/84933 (2026-09-20, from main-pc).
Search-result only [S]: esma.europa.eu node/84933 and notice PDF
esma35-43-1135; papers.ssrn.com 3423101; ideas.repec.org 2019wpecon47;
onlinelibrary.wiley.com 10.1111/0022-1082.00226; bis.org bisbull69 and
work1049; ftc.gov press releases 2025-05 (EEB), 2024-09 (AI crackdown),
2024-02 (Automators AI), 2018-07 (Digital Altitude), 2018-06 blog (MOBE),
2019-10 (AdvoCare), 2022-05 (AdvoCare refunds), 2016-07 (Herbalife);
cnbc.com 2025-03-18; truthinadvertising.org; consumer.ftc.gov Data Book
2024; ftc.gov Taylor public comment 00008-57281.pdf; junglescout.com
amazon-seller-report-2025; bls.gov/bdm and TED 2024;
startbusinessbystate.com; cbinsights.com startup-failure-reasons-top;
techcrunch.com 2022-04-20 Linktree; linktr.ee/creator-report;
insightraider.com; gumroad.gumroad.com last-year-in-the-creator-economy;
support.google.com 9314357; creator-hero.com; sensortower.com
app-store-one-percent and 1H-2022; techcrunch.com 2019-11-21;
machinebrief.com; dev.to jamilxt; valueaddvc.com; hatchworks.com;
files.consumerfinance.gov cfpb_BNPL_Report_2025_01;
consumerfinance.gov BNPL newsroom archive.
Blocked: esma.europa.eu, eur-lex.europa.eu, papers.ssrn.com,
ideas.repec.org, bis.org, ftc.gov, ecfr.gov, courtlistener.com, bls.gov,
advocacy.sba.gov, consumerfinance.gov, fca.org.uk, cbinsights.com,
faculty.haas.berkeley.edu, junglescout.com, marketplacepulse.com,
chartmogul.com, sensortower.com, gumroad.gumroad.com, techcrunch.com,
cnbc.com, support.google.com, android-developers.googleblog.com.
Gaps: ESMA decision text and the Icelandic transposition; FCA crypto
research; Business Opportunity Rule text; FTC MLM guidance; Sentinel
median loss; FBA quit rates; SaaS churn benchmarks; Google Play fees;
YouTube 55 % share; a real creator-income distribution; any AI-wrapper
data; revolving-credit and payday costs; Barber & Odean quote on the
journal page.
