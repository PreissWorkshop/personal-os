# Buying distressed property in Iceland: where it surfaces and how the sale works

Built 2026-09-21 from main-pc, from Act 90/1991 on forced sales, the official
Legal Gazette, the sheriffs' own guidance, the building act and Mosfellsbaer's
conservation papers. Every quotation was seen in the page or PDF text; the
`dist-*` claims in `claims.json` re-check the ones a script can reach.

The problem this answers: a derelict building is never advertised, because
nobody is selling it. It rots precisely because no transaction is happening. It
becomes visible only when a creditor or a court forces the issue, and that has
to be published. `scripts/iceland_distressed.py` reads those publications.

## 1. Where it surfaces

| Item | Value | Label | Source |
|---|---|---|---|
| The Legal Gazette | publication of forced sales there is compulsory; the notices cover "nauðungarsölur, þar á meðal á fasteignum búa sem eru til opinberra skipta" | [V 2026-09-21] | logbirtingablad.is, under Act 15/2005 |
| It is downloadable | every issue is a PDF at files.logbirtingablad.is with no login, "Gefið út samkvæmt lögum nr. 15 10. mars 2005"; there is no free text search, because "Lögformleg birting auglýsinga fer fram rafrænt á áskriftarvef Lögbirtingablaðsins" behind a paid subscription | [V 2026-09-21] | same |
| What a notice contains | the office and its address, the sitting date, then per property the name, municipality, property number, the debtor, the petitioning creditors and the total claim: "Eftirtaldar beiðnir um nauðungarsölur til fullnustu kröfum um peningagreiðslu verða teknar fyrir á skrifstofu" | [V 2026-09-21] | Gazette issues |
| Redistribution is restricted | the site states "Afritun eða dreifing þessa efnis er óheimil." because the notices carry personal data | [V 2026-09-21] | logbirtingablad.is |
| The sheriffs' live list | an open interface at island.is returns office, auction type, lot name, property number, date, time and petitioners, and is the only reliable place to see a continuation auction | [V 2026-09-21] | island.is/s/syslumenn/uppbod |
| Estates | the Gazette also carries bankruptcy, company-liquidation and deceased-estate notices, each naming the trustee, the office address and the creditors' meeting; a trustee may use the forced-sale machinery "til að koma eign þrotabús í verð ef þess er krafist af þeim sem fer með skipti á því" | [V 2026-09-21] | Gazette; Act 90/1991 art. 7 |
| Banks do not publish | Landsbankinn states plainly "Íbúðarhúsnæði er skráð beint hjá fasteignasölum og er því ekki birt sérstaklega á vef bankans." | [V 2026-09-21] | landsbankinn.is |

## 2. How the sale works

| Item | Value | Label | Source |
|---|---|---|---|
| The grounds | six of them, including a statutory lien for state or municipal charges where the amount is fixed in law or an approved tariff, which is why municipalities appear as petitioners over very small sums | [V 2026-09-21] | Act 90/1991 art. 6 |
| Warning first | on the lien grounds the creditor must serve a payment demand with at least fifteen days' notice | [V 2026-09-21] | same, art. 9 |
| The four-week notice | "Auglýsing um nauðungarsölu skal birt einu sinni í Lögbirtingablaði minnst fjórum vikum áður en beiðnin verður tekin fyrir" - this is the earliest public sighting | [V 2026-09-21] | same, art. 20 |
| An open-market alternative | either party may ask for sale on the general market instead of by auction, with consent and a security for costs; the sheriff controls that sale | [V 2026-09-21] | same, art. 23 |
| First auction | at the sheriff's office, advertised at least three days ahead: "Sýslumaður skal fá birta auglýsingu um byrjun uppboðs á eign með minnst þriggja daga fyrirvara í dagblaði" | [V 2026-09-21] | same, art. 26 |
| What must be disclosed | before bidding the sheriff states the property's location, size and age, the registered charges, the costs payable ahead of all claims, and expressly any burdens that survive the sale | [V 2026-09-21] | same, art. 31 |
| Proof of funds | "Sýslumaður getur krafist að sá sem gerir boð í eignina leiði þegar að því rök að hann geti staðið við það" and may require a security first | [V 2026-09-21] | same, art. 32 |
| Second auction, at the property | "verður því fram haldið eftir ákvörðun sýslumanns innan fjögurra vikna frá því lokið er að leita boða" and "skal fram haldið á eigninni sjálfri" | [V 2026-09-21] | same, arts. 35 and 36 |
| The right to inspect | the occupier must let bidders in before bidding opens; the sheriff may force entry with police assistance. "Öllum er heimilt að mæta við framhald uppboðs, jafnt í fasteign og á skrifstofu sýslumanns." | [V 2026-09-21] | same, art. 36; island.is |
| Sold as it stands | "að eignin sé seld svo farin sem hún er þegar uppboði lýkur," | [V 2026-09-21] | same, art. 28 |
| One-year longstop | if the auction has not begun within a year of the first sitting, every petition lapses | [V 2026-09-21] | same, art. 27 |
| Payment | "Algengast er að greiða þurfi 25% uppboðsandvirðis við samþykki boðs, 25%" a month later and the balance three months after acceptance | [V 2026-09-21] | island.is/naudungarsoelur |
| Paying without cash | "Oft ná bjóðendur samningum við veðhafa um að taka yfir áhvílandi veðskuldir." - the route for a buyer without capital, though the share covering the costs of the sale must always be cash | [V 2026-09-21] | same; Act 90/1991 art. 28 |
| Clean title, with a catch | on the deed issuing, "falla niður öll veðbönd, umráðaréttindi, kvaðir, höft og önnur réttindi yfir eigninni við útgáfu afsals" except where law, the terms or the buyer's own undertaking keeps them alive. Charges ranking above where the money runs out survive, which is what art. 31 makes the sheriff warn about | [V 2026-09-21] | same, arts. 56 and 31 |
| The seller may stay a year | where it was the debtor's own home, he may remain "allt að tólf mánuði frá samþykki boðs" paying the buyer a rent the sheriff fixes | [V 2026-09-21] | same, art. 28 |
| The state's fee | 56,000 krónur for real property, added to the creditor's claim | [V 2026-09-21] | island.is/naudungarsoelur |

## 3. The pipeline from neglect to auction

This is the part worth understanding, because it is the only route to a building
nobody is yet selling.

| Item | Value | Label | Source |
|---|---|---|---|
| The building official's power | where a building's "ásigkomulagi, frágangi, umhverfi eða viðhaldi húss, annars mannvirkis eða lóðar ábótavant" is defective, dangerous or unhealthy, the official orders the owner to put it right, may levy daily fines up to 500,000 krónur, and may have the work done at the owner's cost | [V 2026-09-21] | Act 160/2010 art. 56 |
| Those costs become a lien | and a municipal statutory lien is itself a ground for forced sale without any prior judgment: "ákvæðum laga sem veita lögveðrétt í eigninni fyrir kröfu ríkisins, sveitarfélaga" | [V 2026-09-21] | Act 90/1991 art. 6 |
| It is used in practice | in the window examined, a capital-region municipality was itself the petitioning creditor on a property in its own area | [V 2026-09-21] | Gazette, August 2026 |

So a neglected building has a statutory path: complaint, order, fines, works at
the owner's cost, lien, forced sale, Gazette notice, and four weeks later it can
be bought. Nothing about that path is unusual or adversarial; it exists because
neglected buildings damage their neighbours. [I]

## 4. Reading the notices without being misled

| Item | Value | Label |
|---|---|---|
| A claim is not a condition report | a municipality chasing an unpaid charge of 92,995 krónur on a 2019 flat says nothing about the building. The interesting ones are old and carry a claim that is large against the assessment | [I] |
| Cross-reference the property number | the Gazette gives a fastanúmer and the sale register carries the same number for anything sold since 2006, with size, build year, type and last price. Roughly two in five forced-sale properties are not in the register at all, which means they have not changed hands in twenty years | [I] from the session's own matching |
| Percentage shares | many entries are for a part share, shown as "50% ehl." in the property name. That is a share of a property, not a property | [V 2026-09-21] Gazette |
| Continuation auctions are mostly absent from the Gazette | they are notified by registered letter plus a three-day newspaper or website notice, so the sheriffs' live list is the only reliable place to see them | [V 2026-09-21] Act 90/1991 art. 35 |
| The Gazette's own text is restricted | it names private debtors. Read it for yourself, and do not republish it | [V 2026-09-21] |

## 5. Heritage, which can make a cheap building unusable

Checked for the Álafoss mill district in Mosfellsbær, as a worked example of what
to check anywhere.

| Item | Value | Label | Source |
|---|---|---|---|
| A conservation proposal is live | the council put a proposal to the minister to make the area a protected district, out for public comment "til og með 11. janúar 2026"; no ministerial confirmation was found since | [V 2026-09-21] | mos.is |
| It already has neighbourhood protection | "Hverfisvernd í Álafosskvos er hluti af hverfisvernd" under the current master plan | [V 2026-09-21] | Mosfellsbær conservation report |
| Some buildings are protected automatically | four in the area because they predate 1924, and five more need the heritage agency's opinion because they predate 1940. "Óheimilt er að gera breytingar á friðuðu húsi án" that opinion and permission | [V 2026-09-21] | same, under Act 80/2012 |
| Conversion is physically awkward | the report warns the old machine halls were built to let heat out rather than keep it in, so sound and thermal insulation are the problem | [V 2026-09-21] | same |
| The general rule elsewhere | buildings that are protected, predate 1918 or carry streetscape protection cannot be altered on the minor-works route at all | [V 2026-09-20] | Building Regulation 112/2012 |

## 6. What the facts allow [I]

- The Gazette notice is the buying opportunity, not the auction. Four weeks is
  enough to inspect, price the work and decide, and almost nobody else is reading
  it.
- The continuation auction is held at the property and the occupier must let
  bidders in. For a builder that is a free survey of a distressed building, and
  it is the single most useful feature of the whole process.
- A buyer without capital should be looking at taking over the charges rather
  than paying the price in cash, which the sheriffs' own guidance describes as
  common.
- The surviving-charges rule is where money is lost. What ranks above the money
  running out stays on the property, and the sheriff must say so at the first
  auction. Attend that, or read what was said there, before bidding at the second.
- For a building that nobody is selling, the route is the building official, not
  the market. It is slow, it is public, and it ends in the Gazette.
- Check heritage protection before price. A protected building cannot be altered
  without permission, and that decides whether a cheap wreck is an opportunity or
  a liability.
