# Maker leverage: what Tenis already owns, and what the market says it is worth

Researched 2026-09-19. Only the public HelmCNC site (the
`PreissWorkshop/HelmCNC` GitHub Pages repo) could be opened; every vendor
domain was refused by the sandbox proxy. Labels: **[V]** verified (page
opened) · **[S]** snippet (search-result text; URL not opened) · **[SR]**
self-reported (a founder's own statement, via snippet) · **[I]** inference ·
**[G]** gap. Re-open every [S] price before it goes into a plan or a
customer conversation.

Contents: 1 HelmCNC and the CNC-control market · 2 licensing and checkout
platforms · 3 digital files for makers · 4 vertical software for small
shops · 5 makers who built online income · 6 ScanPen's competitive set ·
7 Iceland context · 8 the opportunity map · 9 sources

## 1. HelmCNC and the CNC-control software market

What HelmCNC says about itself [V] (raw.githubusercontent.com/PreissWorkshop/HelmCNC/main/index.html, github.com/PreissWorkshop/HelmCNC, fetched 2026-09-19):
- "A paid standalone Windows control frontend for Dynomotion KFLOP / Kogna CNC controllers."
- "$129 founder price (first 30 days), $239 after — yours forever."
- "Six monthly payments ($270 total) and the license is yours — the same perpetual license." · "An optional $19/yr keeps updates coming." · "Free 14-day full-featured trial."
- "© 2026 HelmCNC · Independent product · Not affiliated with Dynomotion."
The public repo holds only the marketing site: no release list, customer
count or Freemius mention. Customer count and revenue come from Tenis's own
records (Freemius dashboard), never from this file.

The price landscape (all [S] unless marked):

| Product | Price | Company | Source |
|---|---|---|---|
| HelmCNC | $239 perpetual ($129 founder); $45×6 rent-to-own; $19/yr updates [V] | one person (Tenis) | HelmCNC site |
| Mach4 Hobby / Industrial | $200 (up to 5 machines) / $1,400 ($1,295 at a retailer) | Newfangled Solutions, US | machsupport.com/licensing, /shop/mach4-industrial |
| UCCNC licence key | ~€66 (€55-60 ex VAT); one key per motion controller | CNCdrive, Hungary (size unknown) | shop.cncdrive.com productID=494 |
| Centroid Acorn kit / CNC12 Pro upgrade | kits "start at $369" / $79 on v4.16+ ($399 on ≤v4.14) | Centroid, US (not one person) | shopcentroidcnc.com |
| MASSO G3 Touch | US $2,577 list, $2,397 on site (hardware controller with built-in software) | MASSO, Australia | masso.com.au |
| PlanetCNC controller licence | €69 + VAT per controller | PlanetCNC, Slovenia (size unknown) | shop.planet-cnc.com |
| EdingCNC | full licence included with the CNC720; CNC310 add-on ~€50-72 via reseller | EdingCNC, NL (size unknown) | edingcnc.com; hardware-cnc.nl |
| Dynomotion KFLOP | $299; KMotionCNC (stock GUI) free; third-party .NET front-ends explicitly supported | Dynomotion, US (small) | store.dynomotion.com |
| LinuxCNC / Carbide Motion / Duet RepRapFirmware | free | community / Carbide 3D / Duet3D | wikipedia; carbide3d.com; docs.duet3d.com |

What this means [I]:
- $239 sits above the PC-software peers that bundle hardware (UCCNC ~€66,
  PlanetCNC €69, Mach4 Hobby $200, CNC12 Pro $79) and far below hardware
  controllers (MASSO $2,397). The incumbent GUI for the same hardware is
  free, so the price is defended only by UX and reliability, never by
  necessity.
- No other **paid** KFLOP/Kogna front-end was found (forum front-ends such
  as "Chip CNC" are hobby VB.NET projects) [S: industryarena.com, cnczone.com].
  Zero direct competition, but also no proven market beyond his own
  customers; Dynomotion publishes no installed-base figure [G].
- Every forum thread about custom .NET GUIs for KFLOP is a lead list. The
  ceiling is hundreds of licences, not thousands, until sales data says
  otherwise; that still matters, because a licence needs no capital and no
  presence.
- No verified example of a pure-software one-person CNC front-end business
  was found; the small European vendors (PlanetCNC, CNCdrive, EdingCNC) all
  sell hardware too [G].

## 2. Licensing and checkout platforms (fees per the vendors' own pages, via search)

| Platform | Fee | Notes | Label | Source |
|---|---|---|---|---|
| Freemius | 4.7 % per transaction, "shrinking to 0.5 % as you grow"; on the product price only (not on VAT); no setup or monthly fee | merchant of record (global VAT/sales tax, licensing, subscriptions, disputes, portal, affiliates); payouts by wire, Wise, Payoneer, PayPal, $100 minimum; Iceland payout not confirmed in research, but HelmCNC already sells through it | [V 2026-09-20] for 4.7 % (freemius.com/pricing); rest [S] | freemius.com/pricing; freemius.com/blog/new-freemius-pricing-2025; freemius.com/help/.../our-pricing |
| Paddle | 5 % + 50¢ all-in, no monthly fee; a third party claims 2-3 % FX on top | merchant of record | [V 2026-09-20] for 5 % + 50¢; FX claim [S] | paddle.com/pricing |
| Lemon Squeezy | 5 % + 50¢ | merchant of record; Iceland listed for bank payouts | [S] fee; Iceland payout [V 2026-09-20] | lemonsqueezy.com; docs.lemonsqueezy.com |
| Gumroad | 10 % + $0.50 per direct sale | gumroad.com help article 66 fetched 2026-09-20, "10%" on it | [V 2026-09-20] for 10 %; the $0.50 [S] | gumroad.com/help/article/66-gumroads-fees; veloxthemes.com, pocketsflow.com |
| Etsy | $0.20 listing + 6.5 % transaction + 3 % + $0.25 processing (about 11-14 % of a digital sale) | third-party summaries; etsy.com blocked | [S] | blog.marmalead.com; stowelabs.dev |
| Creative Fabrica | designer keeps 75 % on self-referred sales, 50 % on marketplace-referred; subscription pool split 50/50 | | [S] | creativefabrica.com/open-store |

For a $239 licence, Freemius's percentage-only fee on the net price is the
cheapest of the merchant-of-record options; for a $10-30 subscription the
50¢ fixed part of Paddle/Lemon Squeezy bites [I].

## 3. Digital files for makers

- Vectric's Design & Make is a curated catalogue (2,000+ files; "a typical
  CNC Mini-project typically retails for only $25 and includes 5 individual
  models"), not an open marketplace with a seller programme [S:
  designandmake.com; archive.vectric.com 2014].
- CutRocket (Carbide 3D) is a free project-sharing site, not a paid
  marketplace [S: carbide3d.com/blog/cutrocket].
- Etsy and Creative Fabrica are the open marketplaces; fees in §2.
- Read [I]: files are a low-price volume and SEO game, a byproduct of real
  signage and CNC jobs (every job leaves a reusable file), never a primary
  income. Studio Esja's and the workshop's brand rules still apply to what
  goes up under their names.

## 4. Vertical software for small workshops

| Product | Price | Label | Source |
|---|---|---|---|
| CutList Optimizer | free web tier; premium price not found | [S]/[G] | finewoodworking.com 2021 review |
| Cutlistor Pro | $12 / month or $99 / year | [S] | cutlistor.com/pricing |
| OptiCutter | €9 or €19 / month (July 2026); API ~€99 / month | [S] third party | cutlistevo.com |
| MaxCut Pro | ~$100 once; free Community Edition | [S] third party | cutlistcalc.com |
| CutList Plus fx | $89 / $249 / $499 (another source: ~$100-150 / yr) - conflicting | [S] third party | defusco.com |
| shopVOX (sign/print shop management) | Express $99 / month, PRO $199 / month | [S] | shopvox.com/pricing; itqlick.com |
| SignTracker, EstiMate, GraphixCalc | current prices not surfaced (historical $1,950 for SignTracker) | [G] | sign-tracker.com; estimatesoftware.com; graphixcalc.com |

The founder pattern that repeats - "built it for my own shop, then sold it
to my trade" - is the strongest evidence in this stream:
- **EstiMate / Mark Smith**: a sign-shop owner "struggled with pricing his
  work and wrote EstiMate Sign Pricing Software as a way of getting himself
  to profitability"; launched 15 April 1999; claims 15,000+ registered
  users [SR: estimatesoftware.com/about/vision].
- **ProShop ERP**: "During the first 10 years, they focused and built
  ProShop just for their own company with no plans to commercialize it"
  (Pro CNC machine shop) [SR via press: interestingengineering.com].
- **ProCabinet.App / Adam Denney**: a cabinet maker with 10+ years in his
  own workshop who "built ProCabinet.App to connect the cut list to the
  quote the customer signed off"; no revenue numbers [SR:
  procabinet.app/blog/best-cut-list-software].

Read [I]: cut-list tools cluster at €9-19 a month and are crowded; sign-shop
management sits at $99-199 a month and is thinner. Preiss Workshop's own
CRM and quote flow (signage, wrap, carpentry in one tool) is the natural
candidate, English-first: the Icelandic trade is ~1,700 SI member firms
across all of industry [S: si.is], too small to carry a subscription
product. The shop is the test bench; the first ten customers are shops
like it abroad.

## 5. Makers who built online income (own accounts only)

| Maker | Model | What they say | Label | Source |
|---|---|---|---|---|
| Marc Spagnuolo, The Wood Whisperer Guild | paid courses and a subscription on top of a free YouTube audience | courses "starting at $49"; "Guild Stream ... two full Guild courses each month"; $84 / year back in 2012 | [S] | thewoodwhispererguild.com; popularwoodworking.com 2012 |
| Matt Cremona | online teaching + plans | "Teaching expert-level woodworking online is the core of his business."; sold DIY sawmill plans | [SR] interview | madeforprofit.com/episode57; startribune.com |
| Cam Anderson, Blacktail Studio | YouTube ads/sponsors/affiliates, high-ticket furniture, own product line (N3 Nano finishes), Makerbook directory | "$15K/month" exists only as an interview title | [S] | wikipedia Cam_Anderson; UpFlip video |
| Florian Gadsby (ceramics) | content-first, then 3-4 sell-out drops a year of ~250-450 pots, plus YouTube and a book | "I wish I could make enough to satisfy demand but I don't want to scale my business up, I like working by myself"; restocks sell out in minutes ("3 Minutes 53 Seconds: My Fastest Shop Sell-Out Yet") | [SR] | floriangadsby.com/shop/how-my-shop-works; ceramicartsnetwork.org |
| Bourbon Moth | Patreon exists (graphtreon listing); no own-account numbers | - | [G] | - |

Read for Studio Esja [I]: the drop model sells out in minutes only because
the audience is large and the maker's hands cap supply; it is a brand and
sales tactic, not a scalable income, and it is time-heavy. Keep it as the
premium channel it is; do not count on it in phases 0-3. Third-party
"net worth" and AdSense estimates for any of these makers are not evidence.

## 6. ScanPen's competitive set (why hardware waits)

| Competitor | Price | Label | Source |
|---|---|---|---|
| Leica DISTO D2 | ≈ $255 | [S] | transcat.com |
| Bosch GLM 50 C | ≈ $110-150 | [S] | amazon.com |
| Moasure ONE (motion-measure tool + app) | $349 MSRP; launched on £76,521 from 649 Kickstarter backers plus a claimed $102,343 on Indiegogo | [S] | lawnandlandscape.com; kickstarter.com; launchboom.com |
| Polycam Pro (software scanning) | $26.99 / month or $199.99 / year (App Store), ~$150 / year web; venture-backed | [S] | poly.cam/pricing; techcrunch.com 2024-02-07 |
| Canvas / Twindo | free for two projects a month; outputs from $0.18 / sq ft (2D) and $0.26 / sq ft (3D) | [S] | support.canvas.io |

Ben Einstein (Bolt): "Building the first saleable hardware unit usually
takes more capital than shipping software." [S: blog.bolt.io/hardware-is-hard]

Read [I]: with debt and no capital, ScanPen stays software-only (phone app
plus printed markers, priced per output like Canvas) or parked until phase
4 or a paying pilot customer appears. A printed marker is not hardware; a
manufactured probe is.

## 7. Iceland context

- VAT: sale of services to buyers with no residence or place of business
  in Iceland is exempt if used entirely abroad; the list includes "computer
  services, data processing and information provision" (Act 50/1988 Art.
  12 para 1 item 10) [S: skatturinn.is; althingi.is]. B2C software through
  a merchant of record is an accountant question (`iceland.md` §10).
- Market size for interiors and signage: no Hagstofa or SI figures found
  [G]; SI has ~1,700 member companies across all industry [S: si.is].

## 8. The opportunity map (all [I])

| Asset | Nearest money | Online form | Capital | Rung |
|---|---|---|---|---|
| Skills for hire (C#/.NET machine control, Python/CV, agent systems) | weeks | remote contract, productized setup/automation service | none | 1-2 |
| HelmCNC | months (existing product) | sell into the KFLOP/Kogna base via forums and Dynomotion channels; keep the $19/yr updates line, add a maintenance or support tier | none | 3-4 |
| Workshop know-how | months | productized quoting/cut-list/CNC-setup services, then the shop tool as a product, English-first | none | 2-3 |
| Studio Esja | brand, not scale | content + drops + waiting list | none, but hours | - |
| ScanPen | slowest | software-only or parked | real money if hardware | 4 |

## 9. Sources

Opened [V]: github.com/PreissWorkshop/HelmCNC;
raw.githubusercontent.com/PreissWorkshop/HelmCNC/main/index.html.
Search-result sources [S] (not opened): machsupport.com; shop.cncdrive.com;
shopcentroidcnc.com; masso.com.au; shop.planet-cnc.com; edingcnc.com;
hardware-cnc.nl; store.dynomotion.com; industryarena.com; cnczone.com;
wikipedia LinuxCNC; carbide3d.com; docs.duet3d.com; freemius.com (pricing,
blog 2025, docs); paddle.com/pricing; lemonsqueezy.com;
docs.lemonsqueezy.com; veloxthemes.com; pocketsflow.com;
blog.marmalead.com; stowelabs.dev; creativefabrica.com/open-store;
designandmake.com; archive.vectric.com; carbide3d.com/blog/cutrocket;
finewoodworking.com 2021; cutlistor.com/pricing; cutlistevo.com;
cutlistcalc.com; defusco.com; shopvox.com/pricing; itqlick.com;
sign-tracker.com; signsofthetimes.com; estimatesoftware.com/about/vision;
interestingengineering.com ProShop origin; procabinet.app;
popularwoodworking.com 2012; thewoodwhispererguild.com;
madeforprofit.com/episode57; startribune.com; wikipedia Cam_Anderson;
floriangadsby.com; ceramicartsnetwork.org; transcat.com; amazon.com;
lawnandlandscape.com; poly.cam/pricing; support.canvas.io; kickstarter.com;
launchboom.com; techcrunch.com 2024-02-07; blog.bolt.io; skatturinn.is
VAT pages; althingi.is Act 50/1988; si.is; hagstofa.is.
Blocked: machsupport.com, cncdrive.com, centroidcnc.com, masso.com.au,
planet-cnc.com, edingcnc.com, dynomotion.com, freemius.com, paddle.com,
lemonsqueezy.com, gumroad.com, etsy.com, cutlistoptimizer.com, helmcnc.com,
preissworkshop.github.io, ceramicartsnetwork.org.
