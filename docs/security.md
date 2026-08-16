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
   store (Windows Credential Manager / GitHub Desktop). No plaintext tokens
   outside the Signing folders.
