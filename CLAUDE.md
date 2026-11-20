# Toon Sauce website (toonsauce.com)

Read docs/brand.md for the full brand guide; it overrides the brand notes here if they conflict.

Pre-launch landing page for **Toon Sauce**, a chicken sauce brand. First flavor: **Gold Rush** (sweet, smoky, made with real honey). Mascot: **Gary**, a very strong cowboy chicken who can't say no to anything. Next flavor teased: Cool Ranch (the cat mascot).

The brand was formerly "ProSauce" (theprosauce.com — a separate old site, leave it untouched). "ProToon" was a short-lived name; never use it.

## How the site is built and deployed

- Fully static site + one Cloudflare Pages Function. No framework, no npm.
- **Source of truth:** `tools/gen_site.py` (page content, CSS, copy) and `tools/build_html.py` (wraps pages with `<head>`: GA4, Meta Pixel, meta tags; injects the form/tracking script and cookie notice; maps image IDs to `/assets/...`).
- **Never hand-edit `index.html` or `privacy.html`** — they are generated. Edit `tools/gen_site.py`, then run:
  ```
  bash tools/build.sh
  ```
- `tools/gen_site.py` writes intermediate `*.dc.html` files (a format from the Claude design canvas used earlier). Images are referenced as `/_blob/<id>`; `tools/build_html.py` has a `BLOBS` map from those IDs to files in `assets/`. **To add a new image:** put the file in `assets/` and reference it directly as `/assets/name.ext` in `gen_site.py` (the `/_blob/` indirection is only needed for the old canvas).
- **Browsers cache `/assets/*` for 4 hours**, so when you change an image, save it under a new filename and update the reference; overwriting a file in place won't show up for returning visitors.
- Swappable image slots: `assets/hero-cream.jpg` (hero photo; black background replaced with cream #F6EEDF, food untouched; the dark original is `assets/hero-pour2.jpg`), `assets/bottle.png` (transparent bottle cutout), `assets/gary-wing.png` (placeholder art — replace with real art), `assets/other-sauce.png` (generic "regular sauce" bottle in the comparison), `assets/blandville.webp` (poster in the Blandville video slot). To swap one, add the new file under a new name and update the reference (see the cache note above).
- **Hosting:** Cloudflare Pages project **"toonsauce"**, auto-deploys on push. Custom domains toonsauce.com + www. DNS is on Cloudflare (registrar GoDaddy).
- **Production branch is `claude/adoring-edison-q8icsx`.** Pushing to any other branch does NOT update the live site. Either push to that branch, or (recommended) change the Cloudflare Pages production branch to `main` and merge there.
- Deploys take ~1 minute. Verify with `curl -s https://toonsauce.com/ | grep "<something you changed>"`.
- `_redirects`: old pages (/gold-rush, /cartoons, /cool-ranch, /blandville) redirect to `/`; `/functions/*` is hidden.
- Local preview: `python3 -m http.server 8123` from repo root (the `/api/lead` function does not run locally; mock it in Playwright tests).

## Tracking (do not break)

- **Meta Pixel ID `1495416545782879`** is in `tools/build_html.py` head. Only `PageView` fires on load. Never add a second pixel.
- Facebook domain verification meta tag and GA4 `G-BTGXZ5LCFG` are also in the head.
- Email forms (hero + footer, class `ef`, wrapper `.signup[data-source]`): validate → `POST /api/lead` → only on success fire `fbq('track','Lead',…,{eventID})` with the same `event_id` the server sends to the Conversions API (deduplication).
- After signup: follow-up question "How do you usually get your protein?" → `fbq('trackCustom','QualifiedLead',{protein_source},{eventID})` + server event with same id.
- Server: `functions/api/lead.js` (Cloudflare Pages Function). Hashes email (SHA-256, trimmed/lowercased), sends CAPI with fbp, fbc, IP (`CF-Connecting-IP`), user agent. Upserts Klaviyo profile (props `signup_source`, `protein_source`) and subscribes to list. Optional KV backup binding `SIGNUPS`. All background via `waitUntil` so the user never waits.
- Cloudflare env vars (Pages → Settings → Variables and Secrets): `META_CAPI_TOKEN` (secret), optional `META_TEST_EVENT_CODE`, `KLAVIYO_API_KEY` (secret), `KLAVIYO_LIST_ID`. **Until these are set, signups are not stored anywhere** and only the browser pixel fires.

## Brand guardrails

- Colors: matte black `#141414` (main bg), warm cream `#F6EEDF` (text, light sections), golden amber `#F2A93B` (accents, buttons). No pure white backgrounds.
- Fonts: **Lilita One** (headlines), **Fredoka** (everything else), **Shrikhand** only on the round 7g/70g badge. Flavor names use the logo images, not text.
- Tone: premium, appetizing, confident, dry deadpan humor. Not a gym/supplement brand: never "fuel", "gains", "beast". No gym/shaker/weights imagery, no stock photos of people.
- Never name another restaurant or sauce brand (e.g. no Chick-fil-A). "Drive-thru" phrasing is fine.
- Pre-launch: nothing may imply it can be bought today. No shop/cart/price links.
- Protein: **7g per serving, 70g per bottle** — use only these numbers. Never write "high-protein"; never mention Non-GMO.
- No reviews/testimonials, star ratings, "as seen in" logos, or certification badges.
- Gold Rush calories: 120 per serving (from the current label).

## Current page structure (index.html)

Announcement bar → sticky nav (Gold Rush → `#gold-rush`, Coming soon → `#coming-soon`, "Get first dibs" → focuses hero email) → hero (cream bg; food photo on the right ~74% with a left fade on desktop; dark ink text, headline "Your favorite sauce. / Now with 70g of protein." with amber highlight, subhead, spec line, email form; bottle + 70g badge right) → dark scrolling strip → `#compare` "Sauce just had a glow-up." comparison (cream; Toon Sauce card left with our bottle beside it, regular sauce card right with generic bottle `assets/other-sauce.png`) → `#gold-rush` product showcase (dark; CSS-only photo gallery with captions: bottle, meal prep, bowls, homemade meal prep, tenders, pour (`hero-pour2.jpg`, dark original); Gold Rush logo, specs 70g/7g/real honey, "Gold Rush drops first" → hero form) → `#blandville` teaser (cream; "Something's coming out of Blandville.", Plain intro, 16:9 video placeholder using `assets/blandville.webp` — swap for the "Welcome to Blandville" embed) → `#coming-soon` Cool Ranch teaser (dark shadow photo `assets/ranch-shadow.jpg`, dimmed Cool Ranch logo) → `#new-flavors` cream card "Be the first to try our new flavors." with Gary + email form (source `flavors`) → FAQ (cream) → footer (email form, source `footer`). Cookie notice bottom-left. `/privacy` page.

## Open items / known issues

1. **Protein claim check:** the existing Gold Rush nutrition label (`assets/label-gold.jpg`) says 45g serving, "about 2 servings per container" (~14g protein per bottle). The site says 70g per bottle. Confirm the real bottle has ~10 servings before running ads.
2. Placeholders in `tools/gen_site.py`: `LAUNCH = 'soon'` (launch month), `CONTACT = ''` (privacy contact email; currently points to Instagram).
3. `assets/bottle.png` was hand-edited (80G→70G, Non-GMO mark painted out). The render still has garbled small text ("reld Rusly"). A clean bottle render would be better.
4. `assets/gary-wing.png` is placeholder art.
5. Gary's original art was generated as "Family Guy chicken" style — resemblance risk; consider making him more distinct.
6. Cloudflare env vars above must be added for CAPI + Klaviyo.

## Working style the owner prefers

- Make the change, rebuild, check it in Playwright at 1440×900 and 390×844, push, verify live, then report briefly with a screenshot.
- Keep it premium and minimal; the owner dislikes "AI-looking" templates and clutter.
- Commit messages end with the session's attribution lines if the harness provides them.

Last handoff: 2026-11-20
