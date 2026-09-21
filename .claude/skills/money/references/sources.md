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

## Verification pass 2026-09-20 (main-pc, `scripts/verify_claims.py`)

Run by the employee session on main-pc with open internet, as part of the
first Windows run of `scripts/money-setup.ps1 -Verify`. Result: 30 of 44
claims VERIFIED (the quote is in the page text; the three controls among
them), 5 NOT FOUND (the page answered, the quote is not in its text),
9 BLOCKED (7 × HTTP 403 to a script, 2 × HTTP 404 dead links). The report
sits in `~\.preiss\finance\verify-2026-09-20.md` on main-pc (private folder).
The reference lines were relabelled `[V 2026-09-20]` for exactly the figure the
script found, nothing wider; a substring match is not a reading.

| Result | Claims | What to do |
|---|---|---|
| VERIFIED (30) | Skatturinn: ehf capital, VAT threshold and 24 %, brackets 1 and 3, personal credit, tryggingagjald, reiknað endurgjald 589,000, the 3-year tail (also on PwC); Althingi: the EEA exemption in Act 138/1994, UMS free (Act 100/2010), the 10-year limitation (Act 150/2007); Hagstofa CPI July 5.3 %; Vísir Arion 15.25 %; stripe.com/global without "Iceland"; Lemon Squeezy and Payoneer list Iceland; Freemius 4.7 %; Paddle 5 % + 50¢; Gumroad 10 %; Upwork up to 15 %; ESMA 74-89 %; Morningstar 3.9 %; MMM names the Trinity study; Croatia EUR 3,622.50 on mup.gov.hr; the three controls | cite with the date; the Stripe absence needs a browser look (a script-rendered list would also read as absent) |
| NOT FOUND (5) | is-ehf-fee (140,500 not on the verklagsreglur page), is-capital-tax (22 % not on the fjármagnstekjuskattur page), is-policy-rate (no rate on the 19 Aug webcast page), microconf-28 (28 % not on the report landing page), bis-crypto (81 % not on the abstract page) | settled in round 2 below, except microconf-28 (report behind an e-mail form) |
| BLOCKED 403 (7) | upwork-csharp-median, acquire-multiples, chague-97 (SSRN), ftc-eeb, ftc-advocare, bls-survival, eea-free-movement (efta.int) | settled in round 2 below, except upwork-csharp-median (bot challenge to every route) and eea-free-movement (a summarising tool\'s quotation only, kept [S]) |
| BLOCKED 404 (2) | estonia-threshold (the politsei.ee page is gone; the programme's official page is e-resident.gov.ee/nomadvisa), gitlab-async (the asynchronous page is no longer in the all-remote section of the handbook) | both repointed; two of the three GitLab sentences found on the all-remote guide (round 2 below); the Estonia programme page still unopened |

Everything not in the two tables above is [S], [SR], [I] or [G].

### Round 2, by eye, 2026-09-20 (employee session on main-pc)

The twelve claims the script could not settle were opened by hand: a
browser-style fetch read as raw page text, a headless browser where that was
refused, and the session's fetch tool last. Labels changed only for wording
seen word for word.

| Outcome | Claims |
|---|---|
| Found on a neighbouring page, `claims.json` re-pointed, script now VERIFIED | is-ehf-fee (the gjaldskrá), is-capital-tax (individuals' dividends page), is-policy-rate (the yfirlýsing itself), chague-97 (RePEc record of the working paper; SSRN still 403), bis-crypto (**BIS Working Paper 1049, not Bulletin 69**) |
| Read on the claim's own page, [V]; the script still gets 403 because these sites refuse its honest bot user agent | ftc-eeb, ftc-advocare, bls-survival (read in a headless browser), acquire-multiples |
| Quoted back by a summarising fetch tool only; raw page not readable - kept [S] on review (a tool's quotation is not the page text) | eea-free-movement |
| Not openable, stays [S] | upwork-csharp-median (bot challenge to every route), microconf-28 (2024 report behind an e-mail form) |

Corrections this round: the Acquire.com figures (median profit multiple 3.9x;
the 17x to 5.5x series is public SaaS *revenue* multiples, not net income); the
BIS 73-81 % source; the Chague wording; the FTC Ecommerce Empire Builders
quote; two GitLab sentences that had been quoted with words GitLab did not
write; Stripe's list is in the served HTML (51 entries, Iceland absent,
Denmark and Norway present). The script's user agent was left as it is: the
four 403 claims above stay BLOCKED for the script by design, not by error.

### Round 3, 2026-09-20: the destination's own taxes (`remote-and-relocation.md` §9b)

Spain and Portugal, from the authorities' own pages only: boe.es,
sede.agenciatributaria.gob.es, seg-social.es and portal.seg-social.gob.es;
info.portaldasfinancas.gov.pt, diariodarepublica.pt, sisscontent.seg-social.pt.
Two research agents fetched raw page text (no summarising fetch tool was used
for any fact); the employee session then checked all 78 quotations of the new
section against the saved page texts and read the load-bearing passages itself.
56 claims added to `claims.json`: `es-*` 26 of 26 VERIFIED by the script;
`pt-*` 23 of 30 VERIFIED, the other 7 NOT FOUND because they live in PDFs
(the ISS guide, two AT documents) or in a script-rendered Diário da República
page, which the script cannot read - they were read in the extracted text.
Still [G] after this round: whether an ordinary autónomo, or the owner of a
one-person foreign company, fits either regime; Spain's 80-euro quota for 2026;
Portugal's 2026 social-security edition; a euro table of Spanish quotas.

### Round 4, 2026-09-20: company debt in Iceland (`iceland-company-debt.md`)

A new reference, built from althingi.is (consolidated acts of 1 September
2026), skatturinn.is, sedlabanki.is, island.is and, for the visa side,
immigration.govt.nz and legislation.govt.nz. Three research agents read raw
page text only; the employee session checked all 94 quotations of the file
against the saved texts and read the load-bearing passages itself (the two
penalty articles, the Landsréttur judgment, Act 150/2019 arts. 7, 12 and 15,
Bankruptcy Act arts. 64, 112-113, 134 and 180-182, Penal Code arts. 53-54).
36 claims added (`is-debt-*`, `nz-char-*`). Not settled by any authority
page: which taxes a payment plan excludes, the maximum length of an ordinary
plan (the procedural rules are not public), and whether a newer restructuring
statute replaces Act 57/2020.

### Round 5, 2026-09-20: interior film training (`interior-film-training.md`)

Providers' own pages only (24 training providers, two vehicle-wrap
platforms), read as raw page text by a research agent; the employee session
checked the 25 quotations of the file against the saved texts. 11 `film-*`
claims added. YouTube counts were read in the pages' embedded data and cannot
be re-checked by the script; Udemy refused every fetch, so the absence of an
independent English online course is a search result, not proof.

### Round 6, 2026-09-20: seven references for the course-and-installs strategy

Seven research agents fetched raw page text (curl, headless Edge, PDF text)
and returned URL-plus-quotation blocks; the employee session checked every
quotation of each new file mechanically against the saved texts before
writing it, then ran the script on the new claims.

| File | Claims | Script result |
|---|---|---|
| `video-production-and-dubbing.md` | 13 `dub-*` | 13 verified |
| `trade-qualification.md` | 15 `trade-*` | 15 verified |
| `nz-pathways.md` | 22 `nzp-*` | 22 verified |
| `course-platforms.md` | 17 `plat-*` | 17 verified (two are absence checks: Stripe and Thinkific list no Iceland) |
| `iceland-b2b-market.md` | 19 `isb-*` | 19 verified |
| `tax-residency-and-exit.md` | 19 `exit-*` | 19 verified (two absence checks on Skatturinn's treaty list, with Latvia's presence as the control) |
| `selling-rules-and-ads.md` | 20 `ads-*` | 15 verified; the five ftc.gov pages refuse the script (HTTP 403) and were confirmed the same day by curl, quotation found on each |

Not re-checkable by the script: Statistics Iceland's hotel tables (the API
needs a POST query), the UAE decisions and the FTC notice (PDF), eCFR's
versioner API (needs a compressed request), Meta's policy and help pages
(rendered by script; read with headless Edge). Their quotations were checked
against the saved texts only. Known gaps are marked [G] in the files: an
Icelandic exit tax on an individual's shares was not found and Act 71/2026
was not examined; UAE Cabinet Decision 85/2022 could not be opened; the
regulation under Iceland's Marketing Act 44/2026 was not located.

### Round 7, 2026-09-21: is being a landlord worth it, and where cheap property hides

Five research agents, then the employee session checked every quotation against
the saved page text before writing, as in round 6.

| File | Claims | Script result |
|---|---|---|
| `iceland-letting.md` | 18 `let-*` | 16 verified, 2 blocked by HMS rate-limiting |
| `iceland-distressed-property.md` | 18 `dist-*` | 18 verified |

Two things were computed rather than quoted, from the two public registers put
side by side for the first time. Rental yield by postcode for a standard flat,
which came out at 2.56% to 4.78% after costs and tax and beat an instant-access
savings account in none of 27 postcodes. And repeat sales: of 6,252 capital-region
flats resold within two years since 2006, the median beat the market by 1.0% and
44% fell behind it, which is the base rate for flipping.

Three tools came out of this round and live in `scripts/`: `portfolio` in
money_model.py, `iceland_comps.py` for recorded sale prices, and
`iceland_distressed.py` for forced sales and estates.

Sources that decayed during the work, worth knowing before trusting an old note:
HMS stopped recording registered tenancy agreements at the end of 2023, so the
rental register is a closed historical file and 2023 rents have to be carried
forward on the published index; Skatturinn's rental income page is now
script-rendered, so those claims are repointed at the statute; and the property
listing endpoint used in round 6 is dead, replaced by a different portal's
public interface. The sale register, by contrast, is still refreshed daily.

## The upgrade pass (do this from main-pc or the laptop, ~2 hours)

Status 2026-09-20: the mechanical part ran on main-pc (30 / 5 / 9 above) and
the labels were updated the same day. The hand part below stays open
except where a reference line now reads `[V 2026-09-20]`.

Mechanical first: `python scripts/verify_claims.py --report verify.md`
fetches every claim in `references/claims.json` (44 load-bearing claims
with their URLs and quotes, three of them controls that were verified on
the page when the skill was built) and prints VERIFIED / NOT FOUND /
BLOCKED per claim. NOT FOUND means the page answered but the quote is not
on it - open the page, correct the reference, note the date. BLOCKED means
try from another machine. Then, by hand, the items below that the script
cannot settle (PDFs, wording, judgement), changing each label to [V] with
the date. Order by how load-bearing the claim is:

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
8. ESMA CFD decision; Chague et al. 2020; BIS Working Paper 1049 (was
   cited as Bulletin 69, which does not carry the figure); the four FTC
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

| File | Stream | Findings | Verified (09-19 + 09-20 passes) |
|---|---|---|---|
| `fi-and-debt.md` | 01 FI math and debt | ~22 | 2 |
| `iceland.md` | 02 Iceland money, tax, legal | ~35 | 21 |
| `case-studies.md` | 03 indie software cases | 14 cases, base rates | 1 |
| `playbooks.md` | 04 services to product | 32 | 1 |
| `remote-and-relocation.md` | 05 remote and relocation | 56 | 3 |
| `what-fails.md` | 06 what fails | 21 | 7 |
| `maker-leverage.md` | 07 maker leverage | 38 | 5 |
| `software-and-ai.md` | 08 software and AI money | 62 | 7 |

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

From main-pc on 2026-09-20 (open internet) only these refused a scripted fetch:
upwork.com/hire/*/cost, blog.acquire.com, papers.ssrn.com, ftc.gov,
bls.gov, efta.int (HTTP 403 - bot protection, open in a browser);
politsei.ee digital-nomad-visa and handbook.gitlab.com
all-remote/asynchronous (HTTP 404 - pages moved or removed).
