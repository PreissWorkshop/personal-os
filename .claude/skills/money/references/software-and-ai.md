# Software and AI: where the money is for one developer in 2026, and the honest limits

Researched 2026-09-19. Reachable this session: platform.claude.com,
developer.apple.com, github.com and raw.githubusercontent.com (which is
how the Cloudflare, Fly.io and Microsoft docs were read from their public
source repos). Everything else - OpenAI, Gumroad, Paddle, Lemon Squeezy,
Vercel, Stack Overflow, Upwork, Shopify, Atlassian, Levels.fyi, founders'
blogs - was refused. Labels: **[V]** verified (page opened) · **[S]**
snippet (search-result text attributed to the URL) · **[SR]**
self-reported · **[O]** opinion piece · **[I]** inference · **[G]** gap.

Contents: 1 demand · 2 what solo developers sell, with the fees ·
3 AI products with public numbers · 4 SMBs and AI · 5 what an AI product
costs to run · 6 developers vs businesses as buyers · 7 distribution
without an audience · 8 remote AI work as the bridge · 9 the limits ·
10 sources

## 1. Demand signals (measured, not hyped)

- Upwork In-Demand Skills 2026 (2026-02-04): "Demand for top AI-enabled
  skills more than doubled year-over-year, while hiring for human
  expertise remains strong across work categories."; "AI video generation
  and editing (+329%) and AI integration (+178%), to AI data annotation and
  labeling (+154%) and AI chatbot development (+71%)"; but "full stack
  development, general virtual assistance, data analytics, and graphic
  design have remained consistently strong year over year" [S:
  globenewswire.com mirror; upwork.com/research blocked]. Growth rates on
  one marketplace with no base counts; the largest categories are still
  conventional.
- Stack Overflow Developer Survey 2025 (49,009 responses, 166 countries):
  "84% of developers say they use or plan to use AI tools in their
  development process, up from 76% in 2024."; "46% of developers said they
  don't trust the accuracy of the output from AI tools, a significant
  increase from 31% last year." [S: stackoverflow.co press].
- Read [I]: the durable, paid demand is for people who integrate AI into
  existing systems and can verify its output - Upwork's "AI integration"
  line and Stack Overflow's distrust line are the same fact from two sides.
  That is exactly what a C#/.NET and Python engineer with agent-system
  experience sells.

## 2. What solo developers sell, and what the platforms take

| Channel | Fee | Label | Source |
|---|---|---|---|
| Apple App Store, Small Business Program | "a reduced commission rate of 15% on paid apps and Apple In-App Purchases" for "developers who made up to 1 million USD in proceeds in the prior calendar year"; standard rate above (the page does not print it); EU alternative terms "a further reduced commission of 10%" | [V] | developer.apple.com small-business-program |
| Microsoft Store | "keep 100% of the revenue for non-gaming apps" with your own commerce; "a competitive fee of 15% for apps and 12% for games" via Microsoft commerce; registration free for individuals since Sept 2025 | [V] (docs source repo); registration [S] | MicrosoftDocs windows-dev-docs; blogs.windows.com 2025-09-10 |
| Gumroad | "Gumroad charges a 10% + $0.50 fee per transaction."; merchant of record since 2025-01-01; PayPal payout with 2 % fee where bank payout is unavailable; Iceland not confirmed | [S] third party - verify | gumroad.com help 66 (blocked); dodopayments.com; latuos.com |
| Lemon Squeezy, Paddle | "identical headline rates of 5% + 50¢ with no monthly fee. Both platforms operate as merchants of record."; Lemon Squeezy adds international, PayPal and subscription surcharges | [S] | dodopayments.com comparison |
| Shopify App Store | "Developers keep 100% of their first $1,000,000 USD in gross app revenue earned from January 1, 2025, and 85% of earnings above that." (lifetime, not annual, since 2025); $19 one-time | [S] | shopify.dev (blocked) via betakit.com |
| Atlassian Marketplace | revenue share only when "Paid via Atlassian"; direct sales "no revenue sharing with Atlassian"; share % not captured | [S]/[G] | developer.atlassian.com (blocked) |
| GitHub Sponsors | "More than $100 million has been invested in open source maintainers and projects through GitHub Sponsors." since 2019 across >70,000 recipients | [S] | github.blog (blocked) via helpnetsecurity.com 2026-07-21 |
| Anthropic's Claude Code plugin directory | "Third-party partners can submit plugins for inclusion in the marketplace. External plugins must meet quality and security standards for approval."; "Anthropic does not control what MCP servers, files, or other software are included in plugins"; **no mention of paid plugins, revenue share or payouts** | [V] | github.com/anthropics/claude-plugins-official README |
| Chrome Web Store, Figma Community, Notion Marketplace | fees not obtained | [G] | - |

What that means [I]:
- A C#/.NET desktop tool (HelmCNC's shape) is best sold through a merchant
  of record at 5 % or Freemius's 4.7 % (`maker-leverage.md` §2), listed in
  the Microsoft Store at 0 % for discovery. Consumer app stores are a
  15-30 % lottery (`what-fails.md` §8).
- Sponsorship is a tip jar: $100M over seven years across 70,000+
  recipients is roughly $1,400 each, cumulative [I from the snippet]. Open
  source pays when a company buys the closed add-on: Sidekiq - "Sidekiq is
  open source but Sidekiq Pro and Sidekiq Enterprise are closed source,
  commercial add-ons"; revenue reported "closer to $10m than $1m" [SR:
  saas.group podcast; indiehackers.com 016]. Plausible: "$1M ARR ... team
  of four"; "It took 324 days to reach the first $400 monthly recurring
  revenue (MRR)"; "Content marketing and Hacker News are essential to their
  growth." [SR: plausible.io blog via snippet].
- MCP servers and Claude Code plugins or skills have **no stated revenue
  path** as of 2026-09-19 [V]. They are distribution and credibility - a
  listed plugin is a portfolio piece and a lead source; the money is
  off-platform (a paid product or API the plugin talks to, licences,
  consulting). Do not plan a business on selling plugins until Anthropic
  publishes a paid mechanism.

## 3. AI products with public numbers (what they sell instead of "AI")

| Product | Reported numbers | What is actually sold | Label |
|---|---|---|---|
| HeadshotPro (Danny Postma, solo) | "By 2025, HeadshotPro was generating $300,000 per month, or roughly $3.6 million in annual recurring revenue, with 40,000 paying users"; affiliates ">$50,000/month" | an outcome: a usable headshot | [SR] starterstory; aituts.com |
| TypingMind (Tony Dinh, small team) | "$148k revenue last month. All-time high for TypingMind." (Apr 2025); "$130K to $160K a month ... B2B Team plan now more than half of revenue" (Oct 2025); launched 2023-03-01, "$10K MRR in 7 days" (low confidence) | a workflow layer: multi-model client, team admin, bring-your-own-key, shared prompts | [SR] news.tonydinh.com; x.com/tdinh_me |
| Photo AI (Pieter Levels) | not retrieved | - | [G] |

Opinion pieces on the "wrapper" question, labelled as such [O]: "If OpenAI
or Anthropic releases a model tomorrow that is 10x smarter and has
infinite memory, will your business die? If yes, you are a thin wrapper."
[startupfortune.com]; the moat is "data flywheels, workflow lock-in and
distribution" [hatchworks.com]; "each update quietly kills a category of
startup that existed only because the frontier model hadn't gotten around
to doing that specific thing yet" [medium.com, low credibility]. No
dataset supports a wrapper failure rate (`what-fails.md` §9).

Read [I]: the two solo AI apps with public numbers sell an outcome or a
workflow, and TypingMind's revenue moving past 50 % business plans is the
clearest public sign that durable wrapper revenue migrates to workflow
plus business buyers. For Tenis that points at automations inside a trade
workflow (quotes, bookings, follow-ups, shop-floor checks) sold to shops,
never a general chat product.

## 4. SMBs and AI: use is not spend

- US Chamber of Commerce, 2025 (n = 3,870 firms under 250 employees,
  surveyed 6-26 June 2025): 58 % use generative AI (40 % in 2024, 23 % in
  2023); "82% of small businesses using AI increased their workforce over
  the past year."; adoption highest in tech (77 %) and finance (74 %),
  lowest in trades [S: ipwatchdog.com 2025-08-18; uschamber.com blocked].
- Why surveys disagree: "the different numbers do not agree, with the
  reason being methodology rather than error." - the Chamber asks about
  tools like ChatGPT for writing and scheduling; the US Census BTOS asks
  whether AI produces the goods or services and reports far lower shares
  [S: capsulecrm.com]. Salesforce's "91% of small businesses using AI
  report measurable revenue increases" is vendor-sponsored [S].
- What SMBs pay for (bookkeeping, scheduling, quoting, replies) with spend
  figures: not obtained - the single most important gap for a
  trades-vertical thesis [G]. `playbooks.md` §8 has the Intuit and McKinsey
  lines that exist.

## 5. What an AI product costs to run

Anthropic API list prices, USD per million tokens [V: platform.claude.com
/docs/en/about-claude/pricing, fetched 2026-09-19]:

| Model | Input | Output | Cache hit | Batch (−50 %) |
|---|---|---|---|---|
| Claude Fable 5.1 | $10 | $50 | $0.25 (0.025×) | $5 / $25 |
| Claude Opus 5 | $5 | $25 | $0.50 | $2.50 / $12.50 |
| Claude Sonnet 5 | $2 | $10 | $0.20 | $1 / $5 |
| Claude Sonnet 4.6 / 4.5 | $3 | $15 | $0.30 | $1.50 / $7.50 |
| Claude Haiku 4.5 | $1 | $5 | $0.10 | $0.50 / $2.50 |

Modifiers on the same page [V]: 5-minute cache write 1.25× input, 1-hour
2×, cache read 0.1× (0.025× on Fable 5.1); "The Batch API allows
asynchronous processing of large volumes of requests with a 50% discount
on both input and output tokens."; "This tokenizer produces approximately
30% more tokens for the same text." (Claude 4.7 and later); US-only
inference 1.1×; web search "$10 per 1,000 searches"; web fetch "no
additional charges" beyond tokens; Managed Agents session runtime "$0.08
per session-hour"; code execution 1,550 free container-hours a month then
$0.05 per hour; the Sonnet 5 $2/$10 introductory price "is now the standard
price". The page's own unit example: "~3,700 tokens per conversation",
"Using Claude Haiku 4.5 at $1/MTok input, $5/MTok output", "Total cost:
~$37.00 per 10,000 tickets". Its guidance: "Choose Haiku for simple tasks,
Sonnet for most production workloads, and Opus for the most complex
reasoning".

Other costs:

| Item | Price | Label | Source |
|---|---|---|---|
| OpenAI GPT-5 | "$1.25 per million input tokens and $10.00 per million output tokens"; gpt-5-nano $0.05 / $0.40; tracker-named "GPT-5.6" tiers unverified | [S] trackers; official page blocked | pricepertoken.com; morphllm.com |
| Cloudflare Workers | Free: "100,000 per day" requests, 10 ms CPU; Paid: $5/month with "10 million included per month", "+$0.30 per additional million" requests, +$0.02 per extra million CPU-ms | [V] docs source repo | cloudflare-docs pricing.mdx |
| Fly.io | no free tier; "about $5 per 30 days per GB of additional RAM"; support $29 / $199 / $2,500 a month; smallest machine ≈ $2.02/month (third party) | [V] structure; [S] price points | superfly/docs; withorb.com |
| Vercel | "Pro costs $20 per deploying seat per month and bundles $20 of credit"; Hobby free but non-commercial | [S] | schematichq.com |

Margin sketch [I] (from the verified prices and the 5 % + 50¢ fee): a
$10/month plan allowing 200 interactions of ~3,700 tokens costs about
$0.74 in tokens on Haiku 4.5 or $1.48 on Sonnet 5, $1.00 in payment fees,
and a share of a $5/month Workers plan; at 50 subscribers that is ~$500
revenue against ~$90-130 cost, a 75-82 % gross margin. It collapses if
users loop agents or the +30 % tokenizer is ignored - meter per-user
usage, cache the system prompt, batch what is not interactive. The `unit`
command takes the resulting margin.

## 6. Developers vs businesses as buyers

- [O] "developers rarely control the tools budget; their managers do."
  [markepear.dev]; "Developers expect software to be free and open source,
  subscribe to a handful of services that provide value for very little
  cost, and build everything else themselves." [infoworld.com; HN 33687639].
- Quantitative willingness-to-pay data for dev tools: none found [G].
- Read [I]: every small dev-tool business with public revenue in this file
  bills organisations (Sidekiq Pro, Plausible to site owners, TypingMind's
  Team plan). Build for the developer, invoice the company; for Tenis, build
  for the machine operator, invoice the shop.

## 7. Distribution without an audience

| Channel | Evidence | Label |
|---|---|---|
| Product Hunt | "top 3 of the day pulling 5,000 to 15,000 visitors and 100 to 400 signups"; outside the top 10 under 500 visitors; ~10 % of launches featured; 4.5-8.3M monthly visitors, about half the 2018-19 peak | [S] third party: shno.co; causo.ai |
| Hacker News front page | "Reaching the Hacker News front page can deliver 10,000 to 30,000 visitors in 24 hours, though results vary significantly."; ~90 % of submissions never reach it; 58-68 % of HN visitors block analytics | [S]/[SR] marcotm.com; blog.abdellatif.io |
| Content and SEO | Plausible: content and HN "essential" to $1M ARR; 324 days to the first $400 MRR | [SR] |
| Affiliates | HeadshotPro ">$50,000/month" from affiliates - works when the buyer gets a clear cash outcome | [SR] |
| Audience-first | Vassallo: "Before you start thinking about building an audience, you need to build some credibility."; $210,822 in 9 months from a PDF and a course - sold to other aspiring founders, a different market from tradespeople | [SR]/[O] dvassallo.medium.com |
| Embedded in a community | Kahl: "Embedded Entrepreneurs find customers and build a solution for and with them." | [O] thebootstrappedfounder.com |
| Plugin and MCP directories | distribution and credibility only; no revenue mechanism | [V] |
| Cold outreach studies, Reddit/Discord, programmatic SEO | not obtained | [G] |

Read [I]: launches are a spike, content compounds slowly, and the
embedded position is the one Tenis already holds - CNC operators, KFLOP
users and small workshops are his community without a social audience.
Direct outreach into that community (`playbooks.md` §7) beats any launch.

## 8. Remote AI and software work as the bridge

- Levels.fyi aggregate (US-weighted, self-reported): AI Engineer median
  total comp ~$154,000 across all companies; "median US AI engineer total
  pay peaked at $295K in March 2024, fell 22% to $228,500 by January 2025,
  then rebounded to $277K by March 2025" [S: pin.com; levels.fyi blocked].
  Not remote-from-Iceland rates.
- Braintrust: "charges a 15% flat fee of the total amount the client pays
  for the project, while freelancers keep 100% of their earnings"; a
  10-minute video screening [S: terminal.io; sidehusl.com]. Toptal: "The
  screening process includes algorithmic interviews, live coding, and test
  projects."; client deposit $500 [S: fastlancer.org]. Mercor: "uses an AI
  interviewer to screen candidates." [S low credibility: money-forge.org].
  "$50-200/hour" claims for AI platforms come from listicles - not
  evidence.
- Read [I]: rates and fees for the platforms are in `playbooks.md` §1; the
  vetted platforms (Braintrust, Toptal) are worth one application each
  because they carry the client-side fee, not his.

## 9. The limits (opinion, labelled)

- BCG 2025 [O]: "Customers perceive greater value in expertise (such as
  domain-specific insights or proprietary data) and in the complete
  execution of tasks" - generic software gets cheaper to make and sell.
- Candriam [O]: "Software tools serving highly regulated industries such
  as healthcare, financial services or government maintain resilience,
  where data security and compliance are paramount."
- Guru Startups [O]: "combine domain expertise, data advantage, and
  regulatory alignment with API access".
- Read [I]: all three point at the same premium bucket - deep domain
  knowledge, data the model lab does not have, a complete outcome, and
  hardware or safety constraints. CNC control, machine-vision QA and
  shop-floor automation sit there; no retrieved source names CNC, so this
  is a mapping, not their claim. Counter-evidence to keep in view:
  developers distrust AI output (§1) and so will buyers of safety-critical
  software; open source pays badly (§2); plugins have no revenue path (§2);
  SMB "AI use" is mostly ChatGPT, not paid vertical software yet (§4).

## 10. Sources

Opened [V]: platform.claude.com/docs/en/about-claude/pricing;
developer.apple.com/app-store/small-business-program/;
github.com/anthropics/claude-plugins-official;
raw.githubusercontent.com cloudflare/cloudflare-docs workers pricing.mdx;
raw.githubusercontent.com superfly/docs about/pricing;
raw.githubusercontent.com MicrosoftDocs windows-dev-docs
why-distribute-through-store.md.
Search-result only [S]: upwork.com/research/in-demand-skills-2026;
globenewswire.com 2026-02-04; stackoverflow.co 2025 survey press;
blogs.windows.com 2025-09-10; gumroad.com help 66; dodopayments.com
(Gumroad fees; Paddle vs Lemon Squeezy); latuos.com; shopify.dev
revenue-share; betakit.com; developer.atlassian.com; atlassian.com
partner agreement; github.blog Sponsors $100M; helpnetsecurity.com
2026-07-21; plausible.io/blog/open-source-saas; founderventures.io;
saas.group Sidekiq podcast; indiehackers.com podcast 016;
startupsfortherestofus.com 661; code.claude.com discover-plugins;
claude.com/plugins; systemprompt.io; starterstory.com
headshotpro-breakdown; aituts.com; news.tonydinh.com oct-2025;
x.com/tdinh_me 1908345028327727335; startupfortune.com; hatchworks.com;
medium.com activated-thinker; uschamber.com C_TEC 2025; ipwatchdog.com
2025-08-18; capsulecrm.com; quickbooks.intuit.com April 2025 survey;
developers.openai.com pricing; pricepertoken.com; morphllm.com;
vercel.com/pricing; schematichq.com; withorb.com; markepear.dev;
infoworld.com 4058058; news.ycombinator.com 33687639; endler.dev;
shno.co product-hunt statistics; hub.causo.ai; awesome-directories.com;
marcotm.com; blog.abdellatif.io; dvassallo.medium.com; x.com/dvassallo
1250224237396148225; thebootstrappedfounder.com; levels.fyi ai-engineer;
pin.com ai-compensation; terminal.io; sidehusl.com; fastlancer.org;
money-forge.org; bcg.com 2025 B2B software pricing; candriam.com
SaaSpocalypse; gurustartups.com.
Blocked: platform.openai.com, openai.com, developers.openai.com,
gumroad.com, help.gumroad.com, lemonsqueezy.com, paddle.com,
developers.cloudflare.com, cloudflare.com, vercel.com, fly.io,
survey.stackoverflow.co, stackoverflow.blog, news.ycombinator.com,
upwork.com, learn.microsoft.com, shopify.dev, claude.com,
quickbooks.intuit.com, levels.fyi, developer.atlassian.com,
developer.chrome.com, plausible.io, mikeperham.com, news.tonydinh.com,
github.blog, uschamber.com.
Gaps: OpenAI official prices; Gumroad's exact fee and Iceland payout;
typical (non-outlier) earnings for desktop and utility apps; Chrome, Figma
and Notion fees; Atlassian's share; GitHub Sponsors per-maintainer
median; Photo AI revenue; credible operator essays on wrappers; SMB AI
spend by category; Stack Overflow salaries by country; willingness-to-pay
data for dev tools; Show HN text and Product Hunt's own numbers; cold
outreach and programmatic-SEO data; remote-from-Iceland AI pay; a source
on the premium for hardware or safety-critical software.
