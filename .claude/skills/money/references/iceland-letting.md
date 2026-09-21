# Letting property in Iceland: the rules, the rents and whether it pays

Built 2026-09-21 from main-pc, from the statutes on Althingi's site, Skatturinn,
Reykjavik's own pages, Mosfellsbaer's planning documents, the Housing and
Construction Authority (HMS), Statistics Iceland and the firms' own price lists.
Every quotation was seen in the page or PDF text; the `let-*` claims in
`claims.json` re-check the ones a script can reach.

The short version, because it decides everything below: letting flats in Iceland
at 2026 prices returns less than a savings account, the favourable tax treatment
stops at two flats, and short-term letting of an ordinary town flat is closed by
planning rather than merely restricted. None of that is a matter of finding the
right property.

## 1. The rule that caps a portfolio at two

| Item | Value | Label | Source |
|---|---|---|---|
| Letting is business activity by default | "Tekjur manna af útleigu íbúðarhúsnæðis, frístundahúsnæðis eða annars húsnæðis, m.a. þar sem gisting er boðin gegn endurgjaldi, skulu teljast stafa af atvinnurekstri eða sjálfstæðri starfsemi nema:" | [V 2026-09-21] | Act 90/2003, althingi.is/lagas/nuna/2003090.html |
| The exception, and the ceiling | the lease must fall under the Tenancy Act, be registered, and "enda séu hinar útleigðu sérgreindu íbúðir ekki fleiri en tvær." A third separately let flat moves the whole activity to personal income rates, which reach 46.29 % | [V 2026-09-21]; the consequence [I] | same |
| Rate while inside the exception | 22 % capital income; "Til fjármagnstekna teljast í þessu sambandi tekjur skv. 1.–8. tölul. C-liðar 7. gr., þ.e. vextir, arður, leigutekjur, söluhagnaður og aðrar eignatekjur." | [V 2026-09-21] | same |
| Charged on the gross | "Ekki er heimilt að draga kostnað frá – skatturinn er lagður á heildartekjur (brúttó)." | [V 2026-09-21] | skatturinn.is, leigutekjur |
| The exemption was halved | "Í stað „50%“ í 4. málsl. 3. mgr. kemur: 25%." in force 1 January 2026; Skatturinn confirms "Þetta gildir frá og með árinu 2026. Frítekjumarkið var áður 50%" | [V 2026-09-21] | Act 103/2025; skatturinn.is |

## 2. Short-term letting: the home route

| Item | Value | Label | Source |
|---|---|---|---|
| What it is | "Heimagisting er gisting gegn endurgjaldi á lögheimili einstaklings eða í einni annarri fasteign"; the second property must now be outside an urban area | [V 2026-09-21] | Act 85/2007 as amended by Act 25/2026 |
| The caps | "Fjöldi útleigðra daga í báðum eignum samanlagt skal ekki fara yfir 90 daga á hverju almanaksári"; income capped at the VAT threshold of 2,000,000 krónur, and the 2026 amendment made the two limits cumulative rather than alternative | [V 2026-09-21] | same |
| Individuals only | "Aðeins einstaklingar geta skráð heimagistingu. Fyrirtæki og lögaðilar verða að sækja um rekstrarleyfi til sölu gistingar." | [V 2026-09-21] | island.is/heimagisting |
| The clock follows the flat | "Fjöldi gistinátta miðast við fastanúmer og skráð heiti viðkomandi eignar, ekki kennitölu þess sem skráir heimagistingu." so registrants cannot be rotated to reset it | [V 2026-09-21] | same |
| Going over is retrospective | exceed the ceiling or lose the registration and "falla allar leigutekjurnar á tekjuárinu undir atvinnurekstur eða sjálfstæða starfsemi" | [V 2026-09-21] | Act 90/2003 |
| Penalties | fines from 10,000 to 1,000,000 krónur, and "Litið er á hverja selda gistinótt umfram það sem heimilt er samkvæmt lögum þessum sem sjálfstætt brot" | [V 2026-09-21] | Act 85/2007 |
| One thing in its favour | registered home letting "telst ekki fara fram í atvinnuhúsnæði í skilningi laga um tekjustofna", so it does not move the property to the commercial tax rate | [V 2026-09-21] | same; confirmed by Reykjavík |
| Registration | 9,200 krónur, renewed annually, with a return of nights and income each year end; the number must appear "í allri markaðssetningu og kynningu, þ.m.t. á vefsíðum, bókunarsíðum" | [V 2026-09-21] | island.is; Act 85/2007 |

## 3. Short-term letting: the licensed route, and why it is shut in town

| Item | Value | Label | Source |
|---|---|---|---|
| Commercial premises required | since the March 2026 amendment, "gististarfsemi innan þéttbýlis skal vera í samþykktu atvinnuhúsnæði." | [V 2026-09-21] | Act 85/2007 as amended by Act 25/2026 |
| A five-year clock | licences for letting in housing inside a town are now "tímabundið til fimm ára í senn", and those valid on 1 April 2026 "skulu gilda til 1. janúar 2032" | [V 2026-09-21] | Act 25/2026 |
| Reykjavík simply forbids it | the master plan's land-use table permits only category I in residential development: "Íbúðarbyggð (ÍB) Já Nei Nei Nei Nei" | [V 2026-09-21] | reykjavik.is, aðalskipulag land use table |
| The tax jump | residential 0.18 % against "C-skattflokkur 1,60% af fasteignamati", and a property holding an operating licence is moved to class C | [V 2026-09-21] | reykjavik.is/fasteignagjold and the correction page |
| A one-way door | "Vegna lagabreytinga verður ekki hægt að fá rekstrarleyfið aftur eftir að því er skilað, án þess að sækja um byggingarleyfi og breyta húsnæðinu í atvinnuhúsnæði." | [V 2026-09-21] | same |
| Use it or lose it | the authority may cancel a licence where the holder "hafi leyfishafi ekki stundað þá starfsemi sem kveðið er á um í leyfinu í samfellt 12 mánuði." | [V 2026-09-21] | Regulation 1277/2016 |
| VAT | accommodation is VAT-able where the letting is "til skemmri tíma en eins mánaðar", at the reduced rate, with registration required at 2,000,000 krónur of taxable sales | [V 2026-09-21] | Act 50/1988 |
| Accommodation tax | 800 krónur per unit sold, payable only by licensed categories II to IV, so not by home letting | [V 2026-09-21] | Act 87/2011 |

## 4. The neighbours

| Item | Value | Label | Source |
|---|---|---|---|
| The whole external envelope is shared | "Þótt fjöleignarhús samanstandi af einingum eða hlutum (stigahúsum) sem eru sjálfstæðar eða aðgreindar að einhverju leyti og hvort sem þau standa á einni lóð eða fleirum er allt ytra byrði hússins alls staðar, þak, útveggir og gaflar, í sameign allra eigenda þess." | [V 2026-09-21] | Act 26/1994, althingi.is/lagas/nuna/1994026.html |
| A substantial change of use needs everyone | changes bringing "verulega meira ónæði, röskun eða óþægindi fyrir aðra eigendur ... eru háðar samþykki allra eigenda hússins."; a lesser change needs a simple majority | [V 2026-09-21] | same |
| One affected owner can block | where the change causes special and substantial inconvenience to some owners, those affected "eiga þeir sem sýnt geta fram á það sjálfstæðan rétt til að krefjast þess að af breytingunni verði ekki." | [V 2026-09-21] | same |
| Registering with the authorities does not help | "Skráningin sem slík hefur þó ekki sjálfstæða þýðingu við mat á því hvort gagnaðila sé þörf á samþykki" | [V 2026-09-21] | Kærunefnd húsamála 86/2022 |
| Scale decides | letting in one flat fell outside the consent requirement (51/2012), but selling accommodation in four of eight flats did not: "Breytingin hafi í för með sér verulega meira ónæði og röskun en vænta má í sambærilegu húsi og því þurfi samþykki allra eigenda hússins til að heimila starfsemina." | [V 2026-09-21] | Kærunefnd húsamála 38/2009 and 51/2012 |
| Repairs when others will not act | "Eiganda er rétt að láta framkvæma nauðsynlegar viðgerðir á sameign á kostnað allra ef hún eða séreignarhlutar liggja undir skemmdum vegna vanrækslu á viðhaldi og húsfélagið eða aðrir eigendur hafa ekki, þrátt fyrir tilmæli og áskoranir, fengist til samvinnu" | [V 2026-09-21] | Act 26/1994 |

## 5. Long-term tenancy

| Item | Value | Label | Source |
|---|---|---|---|
| Registration is compulsory | "Leigusali skal skrá leigusamning um íbúðarhúsnæði eða annað húsnæði sem leigt er til íbúðar í leiguskrá húsnæðisgrunns", within thirty days, with fines of 10,000 to 1,000,000 krónur | [V 2026-09-21] | Act 36/1994 |
| An unregistered increase is unenforceable | "Breytingu á leigufjárhæð skal skrá innan 30 daga frá gildistöku hennar og er slík skráning forsenda þess að hækkun leigufjárhæðar taki gildi gagnvart leigjanda." | [V 2026-09-21] | same |
| Notice | six months on an indefinite lease, but twelve where the tenant has been there over twelve months and the landlord is "lögaðila sem í atvinnuskyni leigir út viðkomandi íbúðarhúsnæði" | [V 2026-09-21] | same |
| Deposit capped | "mega eigi nema hærri fjárhæð en svarar þriggja mánaða húsaleigu" | [V 2026-09-21] | same |
| No increase in the first year of a fixed lease | "Í tímabundnum leigusamningi er þó óheimilt að semja um að leigufjárhæð breytist á fyrstu 12 mánuðum leigutímans." | [V 2026-09-21] | same |
| Tourist accommodation sits outside it | the Tenancy Act does not apply to use of housing under the accommodation Act | [V 2026-09-21] | same, art. 2 |

## 6. Managing lettings for somebody else needs a licence

| Item | Value | Label | Source |
|---|---|---|---|
| The licence | only a licence holder may "reka miðlun með leiguhúsnæði, sem lög þessi taka til, í því skyni að koma á leigusamningi eða annast framleigu eða skipti á leiguhúsnæði."; the title is leigumiðlari, the licence runs five years and requires an examination and security | [V 2026-09-21] | Act 36/1994 ch. XV |
| Without it | "er með öllu óheimilt að stunda leigumiðlun án leyfis þar að lútandi." | [V 2026-09-21] | Regulation 675/1994 |
| Not the estate agent act | Act 70/2015 reserves only "kaup, sölu eða skipti á fasteignum", so letting is not covered there | [V 2026-09-21] | Act 70/2015 |
| Whether it catches short-term management | unresolved. Chapter XV applies to housing the Tenancy Act covers, and that Act excludes accommodation under Act 85/2007 | [G] | reading of both acts |

## 7. What rents actually are

| Item | Value | Label | Source |
|---|---|---|---|
| The register closed | HMS stopped recording registered tenancy agreements: "Skráningu þinglýstra leigusamninga á íbúðarhúsnæði hefur verið hætt og því verða þessi gögn ekki uppfærð eftir 31.12.2023." The historic file is still downloadable and is Latin-1 encoded | [V 2026-09-21] | hms.is, grunngögn til niðurhals |
| The field that misleads | HEILDARVERD is documented as "Heildarverð leigusamnings. Mánaðarverð." - a monthly figure despite its name | [V 2026-09-21] | same |
| Capital region, agreements of 2023 | median 230,000 krónur a month and 3,244 per square metre, from 2,689 agreements | [V 2026-09-21] derived from the register | HMS rental register |
| The index since | 130.2 points in August 2026, up 4.24 % over twelve months, the smallest annual rise since December 2021; with inflation at 5.6 % rent "lækkað um 1,31 prósent að raunvirði á síðustu tólf mánuðum" | [V 2026-09-21] | hms.is |
| What the index covers | "vegnu meðaltali leiguverðs á fermetra hjá hefðbundnum íbúðum í eigu einstaklinga og hagnaðardrifinna leigufélaga á höfuðborgarsvæðinu." - market rent only, capital region only | [V 2026-09-21] | same |
| By landlord type | three to four room flats averaged about 300,000 from for-profit companies and about 276,000 from individuals, against 238,000 from non-profits and 196,000 from municipalities | [V 2026-09-21] | hms.is |
| Coverage | HMS believes "um 50 þúsund heimili séu á leigumarkaði í dag, en leiguskrá HMS hefur aðeins að geyma um 30 þúsund gilda leigusamninga" | [V 2026-09-21] | hms.is |

## 8. What it yields, and against what

Computed from the two public registers, for a standard 85 square metre flat bought
for cash, with running costs from the published tariffs. Method and the full table
are in `scripts/iceland_comps.py` and the working in the session's scratchpad.

| Item | Value | Label |
|---|---|---|
| Best in the capital region, 111 Breiðholt | 6.74 % gross, 3.70 % after costs and tax | [I] computed |
| Weakest, 110 Árbær and 221 Hafnarfjörður | about 4.87 % gross, 2.57 % after costs and tax | [I] computed |
| Best anywhere in the data, 262 near Keflavík | 8.51 % gross, 4.78 % after costs and tax | [I] computed |
| Postcodes where letting beat a savings account | none of 27 | [I] computed |
| The alternative | an instant-access savings account at "Vöxtur óbundinn 5,55% 5,65% 5,75% 5,85%" | [V 2026-09-21] Arion rate table of 3 September 2026 |

## 9. Short-let demand, for the same comparison

| Item | Value | Label | Source |
|---|---|---|---|
| Capital hotel occupancy | 75.2 % of rooms in 2024 and 74.6 % in 2025; beds far lower at 62.6 % and 61.1 % | [V 2026-09-21] | Statistics Iceland SAM01104 |
| Seasonality, and widening | 92.1 % in August 2025 against 57.7 % in December, a ratio of 1.60; the same ratio was 1.39 in 2023 and 1.51 in 2024 | [V 2026-09-21] | same |
| Demand is flat | foreign departures 2,211,666 in 2023, 2,261,391 in 2024, 2,267,638 in 2025, and the first eight months of 2026 down 1.0 % on 2025 | [V 2026-09-21] | Ferðamálastofa |
| Capital guest nights below their peak | 3,661,440 in 2025 against 3,733,856 in 2018 | [V 2026-09-21] | Statistics Iceland SAM01601 |
| Supply still rising | capital hotel rooms 3,937 in July 2015 against 5,670 in July 2026 | [V 2026-09-21] | Statistics Iceland SAM01202 |
| Rates flat | a bank review states "meðalverð á hótelherbergi nánast haldist óbreytt frá miðju ári 2023" and revenue per available room likewise | [S] a bank report, not official statistics | Arion tourism review, 1 April 2025 |
| Most of the market is unregistered | the government's own bill estimates "tæplega 4.200 einstaklingar bjóði fasteignir til skammtímaleigu án skráningar eða tilskilinna leyfa, sem nemur um 56% af gististarfsemi á landsvísu." | [V 2026-09-21] | Althingi, bill 157/0114 |
| What the legal route earns | of 2,280 who filed a return for 2024, "nýttu um 1.500 þeirra innan við 90 daga yfir almanaksárið 2024 og þénuðu innan við 1,5 millj. kr." | [V 2026-09-21] | same |
| It is not a spare-room market | "Á Íslandi eru 67 prósent allra íbúða á Airbnb með leigusala sem sjá um tvær eða fleiri eignir á markaðnum" | [V 2026-09-21] | HMS |

## 10. What it costs to run one

| Item | Value | Label | Source |
|---|---|---|---|
| Finding a tenant | one month's rent plus VAT is the Icelandic norm, confirmed at six agencies; one charges three months where the lease exceeds twenty months | [V 2026-09-21] | Lind, Eignamiðlun, Fastborg, Ás, HM, Húseign; Heimili |
| Short-let management | the one firm publishing a full rate card charges "20% af veltu að frádregnum kostnaði við ræstingar og þóknun sölurása" plus a monthly system fee and an onboarding fee | [V 2026-09-21] | greenkey.is |
| Turnaround cleaning | from about 10,000 krónur for a studio to 15,000 for a two-bedroom per booking, excluding VAT, with weekend and holiday surcharges | [V 2026-09-21] | same |
| Move-out cleaning | "0-99fm 46.000 m. vsk" and 460 krónur per square metre above that | [V 2026-09-21] | flekklaus.com |
| Utilities | electricity 9.82 to 12.97 krónur per kWh including VAT for the energy plus about 12.05 for distribution; hot water about 227.56 per cubic metre; cold water and drainage are property charges per square metre and are VAT exempt | [V 2026-09-21] | Orkusalan; Veitur tariffs |
| Caretaking, as a benchmark for a one-person operator | "Tímagjald húsumsjónarmanna á vegum rekstrarfélagsins er 9.990 kr. auk virðisaukaskatts." | [V 2026-09-21] | eik.is |
| Insurance for short letting is different | one insurer states its home-letting cover applies "í útleigu í 90 daga á ári eða skemur" and warns claims through short-term platforms are difficult | [V 2026-09-21] | tm.is |
| Building fund | nobody publishes a tariff; an agency article suggests 10,000 to 15,000 a month extra into a works fund | [S] an agency opinion piece of 2023 | husaskjol.is |

## 11. What the facts allow [I]

- A portfolio of let flats is not available on the favourable tax treatment. Two
  is the ceiling, and the third flat re-rates the first two.
- On 2026 prices a cash-bought flat returns less than the bank pays on instant
  access, everywhere in the capital region. Borrowed at the going mortgage rate
  it loses money every month.
- Short-term letting of an ordinary Reykjavik flat is not restricted, it is
  prohibited: the planning permits only the home route, and that route requires
  the owner to live there and caps the year at ninety nights.
- The routes that remain open are approved commercial premises, and property
  outside an urban area where the second-property home-letting rule still works.
- Anyone managing lettings for an owner should establish whether they need the
  letting intermediary licence before taking a fee. Maintaining and renovating
  the same property needs nothing beyond the trades involved.
