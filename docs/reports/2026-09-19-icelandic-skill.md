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
  2026-09; older pages exist (2021–2023) and were not read. About 30
  threads opened in full. Extracted to a scratchpad corpus (not
  committed): about 350 of Tenis's English messages, and 24 Icelandic
  messages sent from his address. Inbound Icelandic from roughly 60
  clients, designers, suppliers, banks and agencies.
- **Correction from Tenis, same day:** the Icelandic mails in his sent
  folder were ChatGPT-written; he is not fluent in Icelandic. The skill
  was rebuilt on that basis — his voice comes from his English, the
  Icelandic wording from native clients and suppliers plus the reference
  rules, and the old sent Icelandic is kept only as a record of terms
  clients have already seen.
- The website's generated quote and acceptance mails of 2026-09-18 — read
  for review only. Tenis's note: Claude wrote that Icelandic before any
  skill existed, so it is a target for the skill, not a source of it.
  Nothing in the skill rests on it.
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

Tenis's English is short, direct and friendly: "Here is ..." first, prices
split into work and material with VAT, ranges with their reason, a fixed
price as a principle defended with quality ("that is my best price for the
highest quality work I deliver"), scope changed rather than the rate when
a budget is short, exact site instructions with the reason, problems
reported fast and without drama, one concrete question at a time, light
emoji with people he knows. Icelandic clients write "Góðan dag / Sæll /
Hæ", ask "Væri hægt að fá verðtilboð í ...", "Takið þið að ykkur ...",
"Er þetta örugglega rétt verð?", and close with "Bestu kveðjur / Kær
kveðja / Kv". The skill renders the first into the second: an
English-to-Icelandic mapping table, worked examples and 21 templates.
Not carried over: typos, ".." pauses, "850þ"-style shorthand and
mixed-language lines - speed, not voice. Detail in
`references/corpus-notes.md`.

## Website mail templates — review

The site's Icelandic is good. Four things a client notices, ranked, with
a proposed rewrite, are in `references/templates.md` → "Website and CRM
templates": the `Sæl/l Fullt Nafn,` greeting (needs a salutation field or
a -son/-dóttir rule), the ISO date in the acceptance mail, `vsk` without
its period, and the bare `Afsláttur` label. 🔒 Tenis: apply in the website
repo; this session could not attach it.

## Test results

Three prompts from `evals/evals.json`, each run by a fresh subagent with
the skill and by another without it (baseline = the model's own Icelandic).
All six drafts passed the checker with no findings, so the checker did not
discriminate here; the differences are in voice and discipline.

| Prompt | Without skill | With skill | Read |
|---|---|---|---|
| 1 Kitchen film quote reply | 106 words, correct, a little wordy ("Þetta er áætlun en ekki fast verð") | 107 words, Tenis's own lines ("Takk fyrir fyrirspurnina og myndirnar", "upphæð sem breytist ekki í lokin"), prices on their own lines, asks for address and phone, Icelandic signature block | Both sendable; the skill version is the one Tenis would have written |
| 2 Delay notice | 86 words, formal ("Ég biðst velvirðingar"), invented the compound "spónarkirnar", added a subject line | 66 words, "Spónninn kom skemmdur", correct cases in "frá þriðjudeginum ... til föstudagsins", owns it in one line, offers another day | Skill version clearly better: shorter, natural, no odd words |
| 3 Studio Esja yunomi | 70 words, good, name "Melur" (a fine idea), one small marketing flourish ("fær að eldast með þér") | 46 words, template pattern followed exactly, facts only, name "Yunomi – grábrúnn" (safe but flat) | Skill version tighter and brand-true; the baseline's naming idea was better and is now a rule in the skill |

Conclusion: the model's unaided Icelandic is competent; the skill adds
Tenis's voice, brevity, house formatting and the discipline not to invent,
and it keeps the register even under a formal-sounding task (the delay).
One improvement was folded back from the test (nature-word naming for
Studio Esja pieces). Outputs live in the session scratchpad, not the repo.
The skill-creator's browser review loop was not run (no display, Tenis
not present); the comparison above is my own read.

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

- Gmail corpus as above (primary); Drive "Scripts" doc. Website mails
  reviewed only.
- Search-result excerpts of: Vísindavefurinn svör 31816, 1837, 75151;
  Íslensk réttritun / Ritreglur (rettritun.arnastofnun.is ch. 3, 6, 7);
  DV "Kveðjur í tölvupóstum" (2011); gerumbetur.ritmal.is "8 lyklar";
  Eiríkur Rögnvaldsson's column on "Hæ"; is.wikipedia "Ávarpsfall" and
  "Glerungur"; Skatturinn VAT guidance; Hönnunarsafn "Deiglumór";
  listavefurinn.is "Leirlist"; studioesja.com about page.

## Supporting evidence

- About 350 English messages by Tenis (the voice) and the inbound
  Icelandic of about 60 native counterparties (the language), quoted
  anonymised in the corpus notes; the 24 machine-written Icelandic mails
  sent from his address are recorded, not used.
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

Confidence: **High** that the skill captures Tenis's register (his own
English) and the clients' expectations (their own Icelandic). **Medium** on
individual orthographic rules marked [K]; a native proofreader would
settle them in minutes and the sources log says where.
