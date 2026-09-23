# Website weekly audit (2026-09-23, cloud routine)

Clean run: nothing broken, nothing fixed. First moves done: `registry/projects.yaml`,
`docs/employee.md`, and in the website repo `AGENT_WORKFLOW.md`, `PROGRESS.md`,
`TODO-OWNER.md`. Source has had **no commits since `eca8035`** (the 2026-09-19
audit merge) other than a no-op `public/` regeneration — this is the same site
that audit already covered in depth, four days later.

## What was checked

- **Build**: `python src/site/build.py` — OK, 114 pages, 56 sitemap URL pairs.
  Regenerated `public/` and diffed against the committed tree: **zero diff**,
  build is reproducible.
- **SEO**: `python src/tools/audit_seo.py` — 112 indexable pages, 112 sitemap
  URLs, **0 warnings**.
- **Internal links and `srcset`** (custom script, all 114 HTML pages outside
  `/admin/` and `/crew/`): every `href`/`src`/`srcset` target resolved against
  the built tree — **0 broken links, 0 broken image paths**.
- **`<title>` and meta description** on all 114 pages — **0 missing**.
- **Empty/near-empty pages** (body text under 80 chars after stripping tags) —
  **0 found**.
- **Alt text**: 1,324 `<img>` tags — 0 missing the attribute entirely. 240 have
  `alt=""`; spot-checked one (the `stigi` project gallery): these are the
  thumbnail-strip images, each wrapped in a button carrying an `sr-only` label
  ("Summer house — complete interior — Photo 1/17") and the large image next to
  it has real alt text. Correct pattern, not a defect — matches the 2026-09-19
  audit's "every image has alt" finding.
- **Broken ASCII Icelandic in visible copy** (`thjonusta`, `ad `, `thess`,
  `rymi`, `hurdar`, `yfirbordsfilmur`, `fraesing`): only hits are URL slugs
  (`/thjonusta/`, `/hurdar/`), which `AGENT_WORKFLOW.md` explicitly allows —
  the visible Icelandic text itself reads correctly (Þjónusta, hurðir, etc.).
- **Asset sizes**: CSS 72 KB and JS 36+16+12 KB, already minified (single-line
  rules, no whitespace) — no unminified or oversized CSS/JS. Video assets
  under `public/media/` are 1.2–1.9 MB each, reasonable for hero video.
  Images: only 4 files over 1 MB (see below).
- **`robots.txt`, `sitemap.xml`, `_redirects`, `_headers`, `404.html`,
  `llms.txt`** — spot-checked, all present and consistent with what the
  2026-09-19 audit left in place (immutable caching on `/images/`, `/css/`,
  `/js/`, `/fonts/`; CSP with `object-src 'none'`; Icelandic `/is/*` 301s).

Not checked this week: the admin, crew and CRM/quote test suites
(`test_crm.html`, `test_quote.mjs`) and anything requiring a live database or
real mail — out of scope for a public-site audit and already exercised in the
2026-09-19 session. `[UNVERIFIED — needs check]` if a website session wants
those re-run.

## Fixed

Nothing. The site was already clean on every check above — there was no
unambiguous, low-risk defect to fix this week. No branch or PR opened in the
website repo; there is nothing to put on one.

## Found but deliberately not touched

- **Four images over 1 MB** (`preiss-projects-forstofa-console-drawer-015-1600w.webp`
  1318 KB, `preiss-process-sea-gold-electroplated-letters-538-1600w.webp` 985 KB,
  `preiss-process-gold-plated-letter-batch-606-1600w.webp` 985 KB,
  `preiss-homepage-hidden-push-drawer-open-151-1600w.webp` 1351 KB). Same class
  of issue as `AUDIT-2026-09-19.md` backlog #19: fixing it means re-encoding
  from the raw photos, which live only on main-pc
  (`C:\PREISS_WEBSITE\PHOTOS_RAW`, per `registry/projects.yaml`) and are not in
  this cloud session, and `/images/*` is cached immutable for a year so a
  same-name overwrite wouldn't reach returning visitors anyway (new filenames
  needed). Not a regression — same files, same sizes as last week's backlog
  item.
- **`llms.txt` says the Clipso service is "in Reykjavík"**, workshop address is
  Mosfellsbær. Same content decision the 2026-09-19 audit flagged for four
  Icelandic meta descriptions (`AUDIT-2026-09-19.md` "Needs Tenis" #7,
  `SEO.md` says it's deliberate for the search keyword) — a content/SEO
  tradeoff, not mine to change unilaterally.

## What needs Tenis

Unchanged from `AUDIT-2026-09-19.md` — nothing new surfaced this week. The
open items there are still open (kennitala/VSK number in the footer, Smart
Film spec figures, service area and lead times, About page has no person, the
Reykjavík-vs-Mosfellsbær SEO wording, the slat-wall length/height
discrepancy, privacy notice, the four oversized images). No new instance of
any of these; no new category of issue found.

## Honesty check

What could be wrong: my link/alt/meta checker is a same-session script, not a
long-standing tool in the repo — it's a reasonable implementation but hasn't
been cross-checked against `audit_seo.py`'s own internals, so a shared blind
spot between the two is possible. What was assumed: that "audit the website"
means the public site (`public/`), not admin/crew/CRM, which the in-tree docs
and last week's audit treat as a separate surface. What was verified and how:
build reproducibility by diffing git status after a clean rebuild; links/meta/alt
by parsing all 114 generated HTML files directly; SEO via the repo's own
`audit_seo.py`. Safest next step: none needed — re-run this same routine next
week; only act if source commits land between now and then.
