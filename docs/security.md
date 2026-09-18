# Security & secrets

## Inventory (locations only — values never appear in this repo)

- `C:\HelmCNC-Signing\` on cnc-pc, mirrored to `D:\HelmCNC-Signing\` (USB
  stick — physically separate medium):
  - `helm_private_key.xml` — RSA private half. Whoever holds it can mint
    HelmCNC licenses **and** sign update manifests (i.e. push code to
    customers' machines). The crown jewel.
  - Cloudflare API token; customer-reports admin token, endpoint, IP salt.
- `C:\HelmCNC\Data\` — machine-local license/trial state. Never committed
  (helmcnc-app `.gitignore` backstops exist and stay).
- `~\.claude\channels\telegram\.env` on main-pc — the Telegram bot token.
- `~\.claude\frontdesk\.env` on main-pc — the same bot token, an Anthropic
  API key, and the webhook token. Written only by
  `scripts/frontdesk-set-key.ps1`, which locks the file to the one user.
  Outside the repo, and the repo's `.gitignore` backstops `.env` anyway.

## Rules

1. Secrets never enter any git repo, doc, chat report, or artifact — not even
   "temporarily".
2. The signing key lives only in the two Signing folders. **TODO: make a third
   offline copy** (second USB stick or paper/QR in a drawer) — today both
   copies sit in the same room.
3. Agents never read secret files' contents, never extract tokens from
   credential stores, never echo values into transcripts. File *names* and
   locations may be documented; contents may not.
4. Per-repo `.gitignore` backstops (pattern set from helmcnc-app; replicate
   where relevant): `*private_key*.xml`, `*_signing_key*.xml`, `freemius.cfg`,
   `.env*`, machine `Data/`.
5. Platform auth (GitHub, Cloudflare, Freemius) stays in the platform's own
   store (Windows Credential Manager / GitHub Desktop). The **only**
   plaintext tokens outside the Signing folders are the two agent-channel
   `.env` files above, because neither Telegram nor the Anthropic API can
   read from Credential Manager. They are machine-local, user-locked, and
   listed in the inventory — not an exception to be widened. Adding a third
   is a decision, not a convenience.
6. An agent never writes, reads back or echoes those files' contents. They
   are written by a masked dialog at the keyboard, and a token is never
   pasted into a chat — including into the front desk's own chat.
