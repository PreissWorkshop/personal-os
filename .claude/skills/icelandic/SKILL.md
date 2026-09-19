---
name: icelandic
description: Write, review and translate modern, natural Icelandic in Tenis Preiss's own voice for Preiss Workshop (custom interiors, carpentry, CNC, signage, film/wrapping) and Studio Esja (handmade ceramics). Use this skill whenever Icelandic is involved at all - replying to an inquiry written in Icelandic, drafting or checking a tilboð/quote mail, a follow-up, a site-visit booking, a delay notice, an invoice reminder, website or CRM mail templates, product names and descriptions, Instagram captions, Telegram or SMS replies, translating English into Icelandic, or judging whether existing Icelandic reads like a real person wrote it. Trigger even when the request itself is in English and only the recipient is Icelandic, and even for a single sentence. Do not use it to address Tenis in Icelandic unless he asks for Icelandic.
---

# Icelandic for Preiss Workshop and Studio Esja

The goal is simple to state and hard to do: a client in Iceland reads the
text and hears a competent craftsman writing to them, not a translation and
not a template. This skill exists because Icelandic business mail has its
own conventions (greetings, closings, how prices are written, what counts as
warm and what counts as cheap) and because Tenis has a recognisable voice
that the corpus in `references/corpus-notes.md` captures.

## When Icelandic, when English

- The client wrote Icelandic -> answer in Icelandic, fully. Never a mixed
  message ("Sæl, the price would be 500þ með vsk"). Tenis himself mixes
  languages in quick replies; the employee and any drafted mail must not.
- The client wrote English -> English (see the brand guide in the workshop
  repo for that voice).
- Tenis's own instruction overrides everything. He is addressed in English
  unless he asks for Icelandic (his standing preference).
- Suppliers: match the language they use; many Icelandic suppliers write
  English to Tenis and Icelandic closings - either is fine.

## Workflow

1. **Load the voice.** Read `references/style-guide.md` (register, greetings,
   closings, numbers, quote structure). For the brand you are writing for,
   read the matching section. For anything longer than two lines, skim
   `references/corpus-notes.md` so the phrasing comes from Tenis's real
   mail rather than from generic Icelandic.
2. **Pick the situation** in `references/templates.md` (first reply, rough
   price, fixed offer, price challenge, booking a visit, delay, done and
   invoiced, reminder, polite no, follow-up, testimonial request; Studio
   Esja product text, custom order, course reply). Start from the template
   and rewrite it for the real facts. Never leave a placeholder in.
3. **Get the facts right before the words.** Prices come from a quote
   calculation or from Tenis; the skill never invents a price, a delivery
   time, a capacity or a care instruction. Unknown -> ask or mark clearly.
4. **Check** with `scripts/check_icelandic.py <file>` (advisory: þéringar,
   "Sæl/l", English-style numbers, ISO dates in prose, English leftovers,
   exclamation marks, missing vsk). Then run the review list below.
5. **Deliver** the Icelandic text. If Tenis asked in English, add a one-line
   English gist under it. State any uncertainty in one line (recipient's
   gender unknown so a neutral greeting was used; a term that could not be
   verified; a fact that must be confirmed before sending).

## The voice in six rules

1. **þú, first name, nominative.** "Sæll Jón," / "Sæl Anna,". No
   þéringar (þér/yður) - they left everyday Icelandic decades ago and read
   as parody. Full names and titles belong on invoices, not in greetings.
2. **Short sentences, concrete nouns.** Materials, dimensions, dates, kr.
   Say what is included and what is not. No superlatives without proof, no
   "lausnir", no exclamation marks in an offer.
3. **Price plainly, split, with vsk.** "Vinna 650.000 kr. með vsk. Efni
   300.000–420.000 kr. með vsk., eftir lit og áferð." Ranges are honest;
   a fixed price is called a fixed price ("fast verð, upphæðin breytist ekki
   í lokin").
4. **Warm, not gushing.** "Gaman að heyra frá þér" and "Þetta er skemmtilegt
   verkefni" are Tenis; "Ég er svo spennt(ur)!!!" is not. One emoji at most,
   only when the client used one, never in an offer.
5. **Own the problem.** Delay or mistake: say what happened, the new date,
   and that you will report the next change. No excuses paragraph.
6. **Brand-true.** Preiss Workshop: precise, calm, competent. Studio Esja:
   calm, artistic, sensory but restrained, grounded in the making (steinleir,
   glerungur, brennsla), never "einstakt tækifæri" or "lúxus".

## Formatting essentials

| Item | Write | Not |
|---|---|---|
| Thousands / decimals | 1.234.500 kr. · 96,6 cm | 1,234,500 · 96.6 |
| Currency | 450.000 kr. (after the number) · 1,8–2,4 m.kr. in prose | kr 450.000 · 750þ (Tenis's shorthand, Telegram only) |
| VAT | með vsk. / án vsk. (lowercase, period) | m/VSK, +vsk in client text |
| Percent | 25% | 25 % |
| Date | 18. september 2026 · 18.9.2026 | 2026-09-18 in prose · 18. September |
| Weekday | miðvikudaginn 23. september | Miðvikudagur (capital) |
| Time | kl. 10:00 · milli 9 og 10 | 10 AM |
| Units | 2008 mm · 50 m · 16 mm MDF | 2008mm |
| Ranges | 300.000–420.000 kr. (en dash) | 300-420 þ |
| Quotes | „sage green“ | "sage green" |
| Phone | s. 771 1255 · +354 771 1255 | +3547711255 |

Sources and what was or was not verified: `references/sources.md`.

## Review list (run it every time)

- Would an Icelandic client believe a person wrote this? Read it aloud.
- Greeting and closing fit the relationship stage (style guide table).
- Every name in the right case; gender agreement on adjectives
  (ánægður/ánægð, búinn/búin, velkominn/velkomin/velkomin pl.).
- Every amount: number format, "kr.", "með vsk." or "án vsk.".
- Nothing invented: prices, dates, lead times, capacities, care claims.
- No English words left, no "Sæl/l", no þéringar, no ISO date in prose.
- Offer text: zero exclamation marks, exclusions stated, validity date.
- Studio Esja text: no marketing adjectives, the making is visible.

## Reviewing existing Icelandic (website, CRM templates, others' drafts)

Report findings as wrong -> right pairs with a one-line reason, ranked by
how a client would notice them. The review of the website's quote and
acceptance mails (2026-09-19) is in `references/templates.md`, section
"Website and CRM templates", and is the model for the format.

## References

- `references/style-guide.md` - register, greetings, closings, signature,
  numbers, quote structure, brand voices, emoji and mixing rules.
- `references/corpus-notes.md` - how Tenis actually writes (his phrases),
  how Icelandic clients write to him, phrase bank by intent, habits to keep
  and habits to smooth.
- `references/templates.md` - ready Icelandic drafts for every recurring
  situation, both brands, plus the website template review.
- `references/glossary.md` - interiors, film, signage, CNC, business and
  ceramics vocabulary with gender and plural.
- `references/pitfalls.md` - the errors that expose a translation.
- `references/sources.md` - verification log: verified, corpus evidence,
  linguistic knowledge, assumption.
- `scripts/check_icelandic.py` - advisory checker.
- `evals/evals.json` - test prompts used to exercise the skill.
