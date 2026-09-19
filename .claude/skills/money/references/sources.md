# Sources and verification log

Built 2026-09-19 in a Claude Code cloud sandbox. **The sandbox's egress
proxy refused nearly every host** (403 on CONNECT: government sites,
regulators, founders' blogs, vendors, Wikipedia, even web.archive.org).
Only WebSearch worked, plus a handful of hosts: github.com and
raw.githubusercontent.com, platform.claude.com, developer.apple.com.
That sets the evidence quality of this whole skill on day one, and the
labels say so everywhere.

## Labels used in every reference file

| Label | Meaning | How to treat it |
|---|---|---|
| **[V]** Verified | the page was opened and the quote is on it | cite, with the date fetched |
| **[S]** Snippet | the claim appeared in a WebSearch result attributed to the URL; the page was not opened; the "quote" may be the search engine's paraphrase | "reported, not confirmed" - open the URL before quoting a number to anyone but Tenis, and before acting on it |
| **[SR]** Self-reported | a founder's own revenue or ramp claim, via snippet | marketing until audited; never audited |
| **[I]** Inference | reasoning or arithmetic from the above | say it is judgement |
| **[R]** Recalled | background knowledge not seen this session | a pointer only ("this regime exists, ask the adviser"), never a figure, rate or rule to act on |
| **[G]** Gap | looked for, not found | say "I could not verify this" |
| **[A]** Assumption | stated input to a calculation | list it in the footer |

## What was verified on the page this session

| Claim | Where | Fetched |
|---|---|---|
| HelmCNC pricing and positioning: "$129 founder price (first 30 days), $239 after — yours forever."; rent-to-own "$270 total"; "An optional $19/yr keeps updates coming."; "Free 14-day full-featured trial."; "Independent product · Not affiliated with Dynomotion." | raw.githubusercontent.com/PreissWorkshop/HelmCNC/main/index.html; github.com/PreissWorkshop/HelmCNC | 2026-09-19 |
| Anthropic API list prices, batch discount, cache pricing, tokenizer note, the support-ticket example | platform.claude.com/docs/en/about-claude/pricing | 2026-09-19 |
| Apple App Store Small Business Program: 15 % under $1M prior-year proceeds; EU alternative terms 10 % | developer.apple.com/app-store/small-business-program/ | 2026-09-19 |
| Microsoft Store fee: 0 % with own commerce for non-game apps, 15 % apps / 12 % games via Microsoft commerce | MicrosoftDocs windows-dev-docs repo (source of the learn.microsoft.com page) | 2026-09-19 |
| Cloudflare Workers Free and Paid limits and prices | cloudflare/cloudflare-docs repo pricing.mdx | 2026-09-19 |
| Fly.io pricing structure and support tiers | superfly/docs repo about/pricing | 2026-09-19 |
| Anthropic's official Claude Code plugin directory states no paid mechanism, revenue share or payouts | github.com/anthropics/claude-plugins-official README | 2026-09-19 |

Everything else in `references/` is [S], [SR], [I] or [G].

## The upgrade pass (do this from main-pc or the laptop, ~2 hours)

Open each URL below, confirm the quote, change the label to [V] with the
date in the reference file, and correct any number that differs. Order by
how load-bearing the claim is:

1. Stripe's supported-country list - stripe.com/global (`iceland.md` §9,
   `remote-and-relocation.md` §6). Decides the whole payments stack.
2. Skatturinn 2026: VAT threshold, rates and export-of-services rule;
   income-tax brackets and the personal credit; tryggingagjald; reiknað
   endurgjald class table; the 3-year tail; ehf capital and fee
   (`iceland.md` §1-3, §7).
3. Act 138/1994 Art. 42 and the 2017 amendment: ehf residency exemption
   for EEA residents (`iceland.md` §7).
4. Acts 100/2010 and 101/2010 (UMS, greiðsluaðlögun) and Act 150/2007
   (limitation) (`iceland.md` §6).
5. Sedlabanki.is MPC statements 2026 and Hagstofa CPI (`iceland.md` §5).
6. Freemius, Paddle, Lemon Squeezy fee pages and Iceland payout
   eligibility (`maker-leverage.md` §2).
7. MicroConf State of Independent SaaS (latest) and Acquire.com
   multiples report Jan 2026 (`case-studies.md` §3-4).
8. ESMA CFD decision; Chague et al. 2020; BIS Bulletin 69; the four FTC
   cases; BLS BED survival (`what-fails.md`).
9. Upwork fee page, rate pages and In-Demand Skills 2026
   (`playbooks.md` §1).
10. Bengen 1994, Trinity 1998, Morningstar 2026, ERN, Pfau 2010, MMM 2012
    (`fi-and-debt.md` §1-2).
11. Visa thresholds on the official pages: exteriores.gob.es (Spain),
    vistos.mne.gov.pt (Portugal), politsei.ee (Estonia), mup.gov.hr
    (Croatia) (`remote-and-relocation.md` §3).
12. Founders' own posts: bannerbear.com journey-to-10k-mrr; nathanbarry.com
    /5k; plausible.io blog; tylertringas.com; theygotacquired.com
    (`case-studies.md`).
13. Vendor prices in `maker-leverage.md` §1 and §4.
14. OpenAI pricing page (`software-and-ai.md`).

A claim that fails verification is corrected in the file and noted in the
next session report; a number that cannot be verified keeps its [S] and
the answer says so.

## Research streams behind the reference files

| File | Stream | Findings | Verified |
|---|---|---|---|
| `fi-and-debt.md` | 01 FI math and debt | ~22 | 0 |
| `iceland.md` | 02 Iceland money, tax, legal | ~35 | 0 |
| `case-studies.md` | 03 indie software cases | 14 cases, base rates | 0 |
| `playbooks.md` | 04 services to product | 32 | 0 |
| `remote-and-relocation.md` | 05 remote and relocation | 56 | 0 |
| `what-fails.md` | 06 what fails | 21 | 1 (Apple) |
| `maker-leverage.md` | 07 maker leverage | 38 | 3 (HelmCNC pages) |
| `software-and-ai.md` | 08 software and AI money | 62 | 6 |

The raw stream files (with every snippet, URL and gap) were kept in the
session scratchpad, not in the repo; the reference files carry what
survived a second reading.

## Hosts that were blocked (for the record)

Government and regulators: skatturinn.is, rsk.is, island.is,
government.is, sedlabanki.is, ums.is, althingi.is, hagstofa.is, utl.is,
esma.europa.eu, eur-lex.europa.eu, ftc.gov, consumerfinance.gov, bls.gov,
federalreserve.gov, fca.org.uk, bis.org, oecd.org, europa.eu, efta.int,
mup.gov.hr, mofa.go.jp, mdec.my, politsei.ee, e-resident.gov.ee,
vistos.mne.gov.pt.
Vendors and platforms: stripe.com, docs.stripe.com, paddle.com,
lemonsqueezy.com, gumroad.com, freemius.com, etsy.com, upwork.com,
support.upwork.com, investors.upwork.com, help.fiverr.com, deel.com,
remote.com, oysterhr.com, wise.com, numbeo.com, openai.com,
developers.openai.com, vercel.com, fly.io, developers.cloudflare.com,
learn.microsoft.com, shopify.dev, developer.atlassian.com,
developer.chrome.com, levels.fyi, machsupport.com, cncdrive.com,
centroidcnc.com, masso.com.au, planet-cnc.com, edingcnc.com,
dynomotion.com, cutlistoptimizer.com, helmcnc.com, junglescout.com,
sensortower.com, cbinsights.com, chartmogul.com.
Founders and media: levels.io, nomadlist.com, tylertringas.com,
robwalling.com, microconf.com, asmartbear.com, nathanbarry.com, kit.com,
buffer.com, joel.is, bannerbear.com, thebootstrappedfounder.com,
theygotacquired.com, adamwathan.me, marclou.com, news.tonydinh.com,
dvassallo.com, plausible.io, blog.acquire.com, indiehackers.com,
mrmoneymustache.com, earlyretirementnow.com, morningstar.com,
kalzumeus.com, jonathanstark.com, momtestbook.com, stackingthebricks.com,
37signals.com, mckinsey.com, medium.com, x.com, wikipedia.org,
techcrunch.com, cnbc.com, news.ycombinator.com, handbook.gitlab.com,
web.archive.org.
