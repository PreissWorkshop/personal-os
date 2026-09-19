# Playbooks: what to do first, rung by rung

Built 2026-09-19 from research stream 04 (freelance market, productized
services, consulting-to-product, validation, pricing, retainers, first
customers, AI work) and the case studies in `case-studies.md`. The sandbox
could open no external page, so every claim here is **[S]** snippet
(search-result text attributed to the URL), **[SR]** self-reported (a
founder's own claim, via snippet), or **[I]** inference. Open the URL before
quoting a number to anyone but Tenis.

Contents: 0 the first 30 days · 1 sold hours · 2 productized service ·
3 product · 4 recurring · 5 pricing · 6 validation · 7 first ten customers ·
8 AI work that sells · 9 saying no · 10 timelines · 11 sources

## 0. The first 30 days (phase 0-1), in order

1. Run `plan`; write the phase and the gap on paper. Nothing else until
   this exists.
2. Collect every króna owed: receivables, deposits not yet invoiced, work
   done and not billed. The website's CRM has the list.
3. Call the most expensive creditor before a payment is missed
   (`iceland.md` §6).
4. Pick **one** sellable offer from §1 or §2 that a known customer can buy
   this week. Write the one-page offer. Send it to ten people who already
   trust him (clients, suppliers, the KFLOP forum, former colleagues).
5. Put HelmCNC's existing price page in front of the installed base it was
   built for: forum threads, Dynomotion's channels, a founder-price mail
   to trial users (`maker-leverage.md` §1).
6. Fix the weekly rhythm: cash actions Monday, delivery Tuesday-Thursday,
   one fixed product block only if phase ≥ 2.
7. Re-run `plan` on day 30; the phase decides the next 30.

## 1. Rung one: sold hours (fastest cash, remote-capable)

Platform facts (2026, all [S]):

| Platform | Freelancer fee | Notes | Source |
|---|---|---|---|
| Upwork | variable 0-15 % per contract since 1 May 2025, "typically around 10 %"; locked when the proposal is sent | client-side fees too; blended marketplace take 19.6 % of GSV in Q2 2026; GSV per active client a record $5,230 | upwork.com/resources/is-upwork-free; nasdaq.com Upwork Q2 2026 release |
| Fiverr | flat 20 % from sellers; buyers pay 5.5 % + a small-order surcharge | | freelancecompare.com (help.fiverr.com blocked) |
| Toptal | 0 % freelancer-side, but the client pays a blended $60-150+/h and "Toptal typically keeps 30-40% of what the client pays"; rates reviewed by Toptal | acceptance-rate marketing | thefrontendcompany.com; freelancemvp.com |
| Contra | "does not charge freelancers any commission"; one snippet mentions a tiered per-payment fee on the free plan - verify | | contra.com/commission-free; memvers.com |

Upwork's own "cost to hire" medians, USD/hour (2026, [S] from Upwork's pages):

| Skill | Median | Typical range |
|---|---|---|
| C# developer | $50 | $35-100 |
| .NET developer (same skill, different label) | $25 | $17-35 |
| Python developer | $30 | $20-40 |
| Machine-learning engineer (incl. CV) | $100 | $50-200 |
| AI engineer | $50 | $35-60 |
| SolidWorks / CAD | - | $25-50 |
| "Highly specialized roles in development, AI, and consulting" | - | "$75-$150+ per hour" |
| OpenCV / CNC programming / CAD-CAM | no median surfaced | [G] |

Demand [S]: Upwork's In-Demand Skills 2026 (4 Feb 2026) reports "AI
integration (+178%)" and skills "explicitly tied to applying AI within
existing roles grew 109% year over year"; Q2 2026 "GSV from AI Strategy &
Consulting ... grew over 50% year-over-year". Growth rates, not volumes;
small bases inflate percentages. A secondary title claims "Half of AI
Automation Jobs Pay Under $500" [S: marathon.limited] - treat as a
hypothesis to check against live job feeds.

What the numbers say to do [I]:
- Label the skill by its highest-paid name: "C# machine-control /
  desktop engineer" ($50 median) not ".NET developer" ($25); "computer
  vision engineer" not "Python developer". Same person, double the median.
- Platforms are for the first proof and reviews; the rate that pays
  (`rate` command) is usually only reachable through direct clients and
  referrals, so every platform job is also a lead for a direct retainer.
- Net of a ~10 % fee and Icelandic tax and contributions, a $50/h platform
  rate is a survival rate, not a target. Run `rate` with the real burn.
- A remote part-time contract (2-3 days a week) is the cleanest bridge: it
  fixes the cash, keeps the product block, and survives a move if the
  contract is with a company that already hires abroad
  (`remote-and-relocation.md`).

## 2. Rung two: the productized service

The pattern, from two self-reported cases [SR]:
- **DesignJoy (Brett Williams)**: "a graphic design business doing over
  $2M/year with no employees or contractors, working about six hours a
  day"; "started with extreme underpricing—$449/month for unlimited
  requests—primarily to get a customer fast, build momentum, and rack up
  'reps'"; "all requests must be submitted asynchronously via Trello, no
  calls or meetings, and only one active request at a time"; prices raised
  with demand; "removed sales calls and let clients buy directly from a
  simple landing page" [SR: dealroom.co note; starterstory.com; designjoy.co;
  getzendo.io]. Revenue figures vary by date ($1.5M-$3.1M); none audited.
- **Draft.dev (Karl Hughes)**: "a productized service that provides
  technical content to software engineering blogs on a subscription basis";
  ~$8k/month at the start, ~$60k/month at 10 months, "within two years, the
  company reached $2.5 million in annual revenue" [SR: nichepursuits.com;
  starterstory.com; karllhughes.com].

The rules that fall out [I]: one deliverable, fixed scope, fixed monthly or
per-unit price, async intake, no sales calls, a landing page that takes
the order, price raised as the queue fills. Candidate offers from his
assets (judgement, to be tested with a real buyer): KFLOP/Kogna machine
commissioning and HelmCNC setup as a package; a "quote-ready cutlist and
CNC program" service for small shops; a one-workflow automation for a
trade business (quotes, bookings, follow-ups) built on the agent system he
already runs; a signage or wrap job's files packaged for another shop.

## 3. Rung three: the product, funded by the service

Consulting-to-product transitions with the mechanics visible [SR]:
- **37signals → Basecamp**: a web-design firm (1999) that "needed a better
  way to manage their projects, looked around for software to help them
  but couldn't find anything" and built Basecamp (2004); "Since mid-2004,
  the company's focus has shifted from web design to web application
  development." [SR: medium.com/@jasonfried Basecamp origin story]
- **Mailchimp**: side project of a web agency (2001); "In 2005, we noticed
  it was a better business than our web-dev agency (it was growing faster
  than us humans, and its recurring revenue was basically keeping us
  afloat)"; "We officially hit the 'reset button' in 2007 and became a
  product company." - a full year of deliberate wind-down [SR attributed to
  Ben Chestnut: justgogrind.com; tinyseed.com; stacksync.com].
- **Tailwind / Adam Wathan**: "went solo in 2016 after writing his first
  book, which made $61,392 in the first week"; a TDD course "made over $1
  million"; "went full-time on it in January 2019 while living on sales
  from his educational products"; Tailwind UI "generated over $4 million
  in revenue in under 2 years" [SR: indiehackers.com AMA; adamwathan.me
  blocked].
- **Bannerbear / Jon Yongfook**, the cautionary one: "spent almost a year
  burning through his savings attempting the '12 startups in 12 months'
  challenge, launching 7 startups but earning no direct revenue"; then
  "took 1 year to reach $10k MRR"; "a two-week cycle: one week for coding
  and the next for marketing" [SR: bannerbear.com/journey-to-10k-mrr;
  starterstory.com; indiehackers.com podcast 208].

The rule [I]: the service reveals the product (Basecamp, Mailchimp), the
service or the info-product pays the founder while the product is small
(Mailchimp until 2005, Wathan until 2019), and the switch happens only when
product revenue is real and recurring. Twelve launches on savings is the
anti-pattern for someone with debt.

## 4. Rung four: recurring revenue

- Retainers are the bridge from project cash to recurring cash: "Promethean
  Research's 2025 Digital Agency Industry Report found 91% offer
  retainers"; "Agency monthly retainers average about $3,209, but the
  single most common price band is $501 to $1,000 per month, which 20.4% of
  providers charge"; 2026 benchmarks put small clients at $1,000-5,000 a
  month [S: shno.co; gigradar.io; agencykit.tech]. (A snippet giving
  "revenue shares" for pricing models sums to over 100 %, so it is really
  "share of agencies using each model".)
- HelmCNC already has the shape: a perpetual licence plus "$19/yr keeps
  updates coming" [V]. A maintenance, support or update line on every
  product is how one-off sales become the compounding rung [I].
- Unit economics before scale: `unit` with real churn; LTV/CAC under 3 or
  payback over 12 months is a stop sign for a cash-poor business [I,
  standard SaaS heuristics - see `case-studies.md` for survey figures].

## 5. Pricing

- Jonathan Stark, *Hourly Billing Is Nuts*: "Billing by the hour rewards
  inefficiency at every level and encourages potentially wasteful,
  premature and unrelated work"; hourly "rewards slowness, punishes
  efficiency, shifts the conversation away from outcomes, and positions
  expertise as labour instead of judgment" [S: club255.com; cfobookshelf.com;
  jonathanstark.com/hbin blocked].
- Patrick McKenzie (patio11): "most famous piece of advice is 'Charge
  more,'" [S: kalzumeus.com/greatest-hits via secondary]. His 2014 piece
  *Don't End The Week With Nothing* exists (training.kalzumeus.com
  newsletter archive; HN item 26531297) but its text could not be
  retrieved - do not paraphrase it as a quote [G].
- DesignJoy raised prices with demand (§2). Upwork's own pages show the same
  skill at $25 or $50 depending on the label (§1).
- Practice [I]: price the outcome with a fixed number where the scope is
  fixed; keep hourly only for open-ended work and then at the `rate`
  figure; raise the price on the next customer whenever the queue is full;
  never discount to win the first customer - shorten the scope instead
  (Tenis's own habit in the workshop, per the Icelandic skill's corpus).

## 6. Validation: money, not applause

- **Buffer (Joel Gascoigne)**: landing page with a pricing page in week
  one; "seven weeks in total before he launched"; "They had their first
  paying customer within 3 days."; "Don't just build. Speak to customers.
  Cut down scope." [SR: mixergy.com; indiehackers.com podcast 058;
  buffer.com post blocked]
- **Storemapper (Tyler Tringas)**: "got paying customers within 24 hours at
  $5/month"; "manually emailing receipts in Gmail for the first two months
  until it became inefficient, then building the automated feature" [SR:
  saasclub.io; tylertringas.com].
- **The Mom Test (Rob Fitzpatrick)**, the three rules as every summary
  gives them: "Talk about their life instead of your idea"; "Ask about
  specifics in the past instead of generics or opinions about the future";
  "Talk less and listen more" - because "the moment you introduce your
  idea, you have contaminated the data." [S: mtlynch.io; theforgeventure.eu
  PDF; momtestbook.com blocked]
- **Sales Safari (Amy Hoy)**: find "the places online where your target
  audience is and interacts" and "take meticulous notes on how they
  communicate their pains, use insider jargon, and make recommendations to
  each other" [S: marcabraham.com; joelhooks.com; stackingthebricks.com
  blocked].
- Counter-evidence [S, opinion pieces, no controlled data]: "Misleadingly
  positive feedback is worse than no feedback at all"; when "it comes to
  actually pulling out the credit card, they back away"; "one founder
  reports building four apps based on ideas that AI tools validated as
  promising, only to have all four fail" [richinjose.medium.com;
  unbuiltlab.com; shubhq.com; failory.com].

The rule [I]: a sign-up list, a "great idea", and an AI's opinion are not
validation. A paid invoice, a deposit, or a pre-order with money is. Sell
the productized version by hand first (Storemapper's Gmail receipts);
automate when it hurts.

## 7. The first ten customers (founders' own accounts)

- **Nathan Barry / ConvertKit**: "But then I discovered the key: direct
  sales."; niche-by-niche outreach; "once a customer was set up and
  successful, he'd ask who else to talk to, and those warm introductions
  worked far better than cold outreach"; "in the beginning, he tracked
  everything in a Trello board" [SR: nathanbarry.com/sales; x.com
  1482374304704565251; indiehackers.com podcast 008].
- **Rob Walling / Drip**: "gave Drip away free to early beta users to build
  initial traction and later converted them to paying." **Jason Cohen / WP
  Engine**: "offered incentives like $50 Amazon gift cards or Starbucks
  cards for conversations" [SR via interviews: blog.salesflare.com;
  saasclub.io; conormccarthy.me].
- Channels across the cases [I]: Buffer - Twitter and Hacker News;
  Bannerbear - Twitter; ConvertKit - direct email and referrals; DesignJoy
  - landing page and Twitter; Draft.dev - niche positioning.
- For Tenis [I]: his first ten are already known - workshop clients and
  designers for the shop tool, KFLOP forum members and trial users for
  HelmCNC, Icelandic trade businesses for an automation offer. Direct
  message, one niche, ask for the next name after every success, track it
  in the CRM he already has.

## 8. AI work that sells (hype removed)

- McKinsey, State of AI: "88 percent of respondents report that their
  organizations are regularly using AI in at least one business function"
  (2025 survey); "About four in ten respondents (37 percent) report that AI
  has contributed positively to their organizations' EBIT" (2026); "80% of
  AI users report improved individual productivity, but ... those gains
  haven't translated into measurable organizational financial benefit"
  [S: mckinsey.com State of AI 2026 PDF; techtimes.com 2026-08-26].
- Agents: "Deloitte's 2026 technology trends research puts the
  pilot-to-production failure rate for AI agents at 89%"; "78% of
  enterprises have at least one agent pilot running, but only 14% have
  scaled one"; the Remote Labor Index paper: "Across the frameworks
  evaluated, the maximum automation rate is 2.5%"; "a lot of what's being
  sold as 'agentic AI' is just old automation, wrapped in new language and a
  nicer UI." [S: thisandthat.chat; fiddler.ai; arxiv 2510.26787;
  artificialintelligence-news.com]
- SMBs: "58% of small businesses now use generative AI — up from 40% in
  2024 and just 23% in 2023 (U.S. Chamber of Commerce, 2025)"; "the top
  three uses are marketing, customer service, and administrative work
  (Intuit QuickBooks, 2025)"; "small businesses typically spend $50 to $500
  per month on AI tools in 2026" [S: aggregators citing the named surveys;
  primaries not opened].
- Read [I]: the sellable thing is a narrow, reliable automation with a
  measured result for a business that already has the pain (quotes,
  bookings, follow-ups, reports), priced against the hours it saves - not
  "an agent". The website's outbox-first mail and the employee's own
  workflow are working demos. A direct critique of the "AI agency course"
  wave was not found in this stream; `what-fails.md` carries the regulator
  cases.

## 9. Saying no (judgement, [I])

- No work priced below the `rate` figure unless it buys a named strategic
  thing (a reference customer, a reusable asset) with an end date.
- No unpaid pilots without a written price for the paid version.
- No "equity instead of cash" from strangers while there is debt.
- No new product idea in phase 0-1 that cannot be sold as a service first.
- No brand-diluting work: discount blasts, generic goods under the
  brands, anything he would not show a premium client.

## 10. Timelines the evidence supports

| Path | Reported timeline | Label |
|---|---|---|
| First paying customer for a pre-sold web product (Buffer) | 7 weeks to launch, paying customer within 3 days | [SR] |
| First paying customers for a tiny SaaS (Storemapper) | within 24 hours at $5/month | [SR] |
| Productized service to $60k/month (Draft.dev) | ~10 months | [SR] |
| SaaS to $10k MRR (Bannerbear) | 12 months, after a year of failed launches | [SR] |
| Freelancers reaching their own income goal | "42 percent ... within 12 months"; "average ... within 23 months"; "Five out of six ... within two years"; "just 28% ... increased their fees within their first year" | [S] secondary 2018 survey, sponsor and sample unknown |
| Freelancer dropout rate | not found | [G] |

Plan cash for a 12-24 month ramp; the sold-hours rung is what makes that
survivable [I].

## 11. Sources (search-result URLs; none opened)

upwork.com/resources/is-upwork-free; support.upwork.com fee article
(blocked); gigradar.io; freelancecompare.com; nasdaq.com Upwork Q2 2026
press release (investors.upwork.com blocked); upwork.com/resources/
freelancing-stats; upwork.com/research/in-demand-skills-2026;
globenewswire.com 2026-02-04; upwork.com/hire/*/cost pages (c-sharp,
dot-net, asp-dot-net, python, machine-learning, artificial-intelligence,
solidworks); upwork.com/resources/upwork-hourly-rates;
thefrontendcompany.com; hireinsouth.com; freelancemvp.com;
contra.com/commission-free; memvers.com; ciela.ai; adsnipper.com;
marathon.limited; dealroom.co DesignJoy note; starterstory.com (DesignJoy,
Draft.dev, Bannerbear); designjoy.co; getzendo.io; nichepursuits.com;
how2exit.com; karllhughes.com; medium.com/@jasonfried; 37signals.com
(blocked); justgogrind.com; stacksync.com; tinyseed.com; getlatka.com;
indiehackers.com (Wathan AMA, podcasts 008/058/208); adamwathan.me
(blocked); bannerbear.com/journey-to-10k-mrr; buffer.com (blocked);
mixergy.com; saasclub.io; tylertringas.com; stackingthebricks.com
(blocked); marcabraham.com; joelhooks.com; momtestbook.com (blocked);
mtlynch.io; theforgeventure.eu; richinjose.medium.com; unbuiltlab.com;
shubhq.com; failory.com; mckinsey.com (blocked; 2026 PDF URL);
techtimes.com; thisandthat.chat; fiddler.ai; arxiv.org/pdf/2510.26787;
artificialintelligence-news.com; epiphanydynamics.ai; capsulecrm.com;
presenc.ai; usecarly.com; jonathanstark.com/hbin (blocked); club255.com;
cfobookshelf.com; training.kalzumeus.com (blocked); news.ycombinator.com
26531297; kalzumeus.com/greatest-hits; shno.co; gigradar.io/blog/
retainer-pricing; agencykit.tech; minora.ai; nathanbarry.com/sales; x.com
nathanbarry 1482374304704565251; blog.salesflare.com; conormccarthy.me;
entrepreneur.com 308524; ddiy.co; blog.freelancersunion.org 2026-01-27.
