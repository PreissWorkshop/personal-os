# Icelandic language skill — built 2026-09-19

Cloud session on branch `claude/icelandic-language-skill-77oinn`. Tenis's
ask: build a skill that makes any Claude session write Icelandic to
clients the way a real person in this trade writes it, learned from every
text available, and use it whenever Icelandic is involved.

## What exists now

`.claude/skills/icelandic/`

| File | What it is |
|---|---|
| `SKILL.md` | Trigger description (pushy on purpose), language decision, five-step workflow, the voice in six rules, formatting table, review list |
| `references/style-guide.md` | Register (þú only), greetings and closings by relationship stage, signature proposal, mail shape, sentence style, numbers/dates/units/vsk, Icelandic quote structure, both brand voices, how to review others' Icelandic |
| `references/corpus-notes.md` | How Tenis actually writes in Icelandic (his own phrases), what to keep and what to smooth, how clients and suppliers write to him, a phrase bank by intent |
| `references/templates.md` | 17 ready drafts: first reply, rough price, fixed offer, price challenge, booking, confirmation, delay, done+invoice, reminder, polite no, follow-up, testimonial, SMS; Studio Esja product text, custom order, course, Instagram; plus the website mail-template review |
| `references/glossary.md` | Interiors, film, signage, CNC/steel, business and ceramics vocabulary with gender and plural, each row labelled by evidence |
| `references/pitfalls.md` | Wrong → right pairs that expose a translation |
| `references/sources.md` | Verification log: what was verified, how, and what is professional judgement |
| `scripts/check_icelandic.py` | Advisory checker (stdlib only): þéringar, "Sæl/l", English number formats, ISO dates, capitalised months, English leftovers, exclamation marks, amounts without vsk, straight quotes |
| `evals/evals.json` | Three test prompts |

Wired in: `CLAUDE.md` (new "Icelandic" section), `docs/employee.md`
(E-mail: Icelandic drafts go through the skill, signed as the workshop in
Icelandic), `docs/agent-system.md`, `docs/bootstrap-new-machine.md` (a
junction exposes the skill from `~\.claude\skills` so it loads in every
project root — unverified on Windows from here).

## What was read

- Gmail (connector, `tenis@preissworkshop.com`): five result pages of sent
  mail matching Icelandic keywords — about 250 threads from 2023-07 to
  2026-09; older pages exist (2021–2023, mostly English replies) and were
  not read. About 30 threads opened in full; 24 Icelandic messages of
  Tenis's own extracted verbatim into a scratchpad corpus (not committed).
  Inbound Icelandic from roughly 60 clients, designers, suppliers, banks
  and agencies.
- The website's generated quote and acceptance mails of 2026-09-18.
- Google Drive: the 2019 "Scripts" doc (early Icelandic and English reply
  templates). Nothing else Icelandic of value was found in Drive.
- The workshop-ops repo (`PREISS_WORKSHOP_CLAUDE_SYSTEM-`, cloned read-only):
  brand guide, premium-offer-writing and client-pdf-offer skills, quoting
  rules — the English voice rules the Icelandic guide maps onto. It holds
  no Icelandic text.
- Studio Esja: the public brand statement via search excerpts (the site
  itself was blocked). The studio's own mailbox is a different account and
  was not reachable.

## What the corpus says (short)

Tenis's Icelandic is short, direct and friendly: substance first, prices
split into labour and material with "með vsk", ranges with their reason,
a rough estimate labelled rough and closed with a site visit, value
framing instead of discounts when challenged, one line of warmth. Clients
write "Góðan dag / Sæll / Hæ", ask "Væri hægt að fá verðtilboð í ...",
"Takið þið að ykkur ...", "Er þetta örugglega rétt verð?", and close with
"Bestu kveðjur / Kær kveðja / Kv". Two habits worth smoothing in drafted
mail: mixing English into Icelandic replies, and workshop shorthand
("750þ", "+vsk") in client text. Detail in `references/corpus-notes.md`.

## Website mail templates — review

The site's Icelandic is good. Four things a client notices, ranked, with
a proposed rewrite, are in `references/templates.md` → "Website and CRM
templates": the `Sæl/l Fullt Nafn,` greeting (needs a salutation field or
a -son/-dóttir rule), the ISO date in the acceptance mail, `vsk` without
its period, and the bare `Afsláttur` label. 🔒 Tenis: apply in the website
repo; this session could not attach it.

## Test results

<!-- TEST-RESULTS -->

## Blocked or not done

- Attaching the website repo was denied by the auto-mode classifier, so
  the template review is from the generated mails, not the source.
- Every Icelandic reference site was blocked by the egress proxy; rules
  rest on search-result excerpts plus the corpus and are labelled as such.
- The first draft of `templates.md` carried a real client name and real
  quote figures from the mailbox; the classifier refused it. All names and
  figures in the skill are now invented, and the corpus file with real
  wording stays in the session scratchpad only.
- The skill-creator's description-optimisation loop needs the `claude` CLI
  and was skipped; the trigger description was written by hand.
- The Windows junction step in the bootstrap doc is unverified.

## Sources checked

- Gmail corpus as above (primary); Drive "Scripts" doc; website mails.
- Search-result excerpts of: Vísindavefurinn svör 31816, 1837, 75151;
  Íslensk réttritun / Ritreglur (rettritun.arnastofnun.is ch. 3, 6, 7);
  DV "Kveðjur í tölvupóstum" (2011); gerumbetur.ritmal.is "8 lyklar";
  Eiríkur Rögnvaldsson's column on "Hæ"; is.wikipedia "Ávarpsfall" and
  "Glerungur"; Skatturinn VAT guidance; Hönnunarsafn "Deiglumór";
  listavefurinn.is "Leirlist"; studioesja.com about page.

## Supporting evidence

- 24 Icelandic messages written by Tenis and the inbound Icelandic of
  about 60 counterparties, quoted (anonymised) in the corpus notes.
- Excerpt-verified rules: decimal comma and period thousands separator;
  "kr." with a period; lowercase months and weekdays; þéringar gone from
  everyday speech since the late 20th century; recommended closings;
  "Sæl(l)" as the standard greeting and "Hæ" as the institutional neutral
  one; "Verð með vsk." as the tax authority's wording.

## Assumptions

- The recipient's language decides the language of the reply; Tenis is
  addressed in English unless he asks otherwise (his preference).
- The employee signs as the workshop in Icelandic ("Bestu kveðjur, Preiss
  Workshop"); the Icelandic signature block for Tenis is a proposal.
- Standard VAT 24% is only an example; real figures come from the quote.

## Unverified points

- Everything labelled [K] in the skill (gender agreement forms, "Sæl
  bæði/öll", compound and hyphen rules, unit spacing, „quotes“, ceramics
  process words like hrábrennsla/handrenndur): standard Icelandic to my
  knowledge, not checked against a source this session.
- The time format "kl. 10:00" is corpus practice; the Ritreglur form was
  not confirmed.
- Whether "24%" without a space is the Ritreglur rule (excerpt only).

Confidence: **High** that the skill captures Tenis's register and the
clients' expectations (it is built from their own mail). **Medium** on
individual orthographic rules marked [K]; a native proofreader would
settle them in minutes and the sources log says where.
