# ProSauce landing page

Static React page (`index.html` + `prosauce-landing.jsx`, compiled in the browser) deployed on Vercel,
plus two Vercel serverless functions for the pre-launch "notify me for the next drop" list.

## Pieces

| Path | What it is |
| --- | --- |
| `index.html`, `prosauce-landing.jsx` | Homepage |
| `images/` | Self-hosted food photos (Pexels free license: 8463470, 11519282, 29653190, 31300944) |
| `api/signup.js` | `POST /api/signup`: stores `{ name, contact, source, smsConsent }` |
| `api/admin/signups.js` | `GET /api/admin/signups` (JSON) and `?format=csv` (CSV), password-protected |
| `admin/signups.html` | Admin page at `/admin/signups` |
| `supabase/migrations/…_create_signups.sql` | Creates the `signups` table |

Signup `source` values: `hero`, `drop-section`, `product-card-sweet-smoke`, `product-card-ranch`.

## Environment variables (Vercel → Project → Settings → Environment Variables)

| Variable | Purpose |
| --- | --- |
| `SUPABASE_URL` | Supabase project URL, e.g. `https://abcd1234.supabase.co` |
| `SUPABASE_SERVICE_ROLE_KEY` | Supabase **service_role** key (server-only; never put it in client code) |
| `ADMIN_PASSWORD` | Password for `/admin/signups` |

## Setup

1. Create a free Supabase project (or use an existing one) and run
   `supabase/migrations/20261008000000_create_signups.sql` in the SQL editor.
2. Add the three env vars above in Vercel and redeploy.
3. Visit `/admin/signups`, enter `ADMIN_PASSWORD`.

## Local development

```sh
ADMIN_PASSWORD=test SIGNUPS_DEV_FILE=.signups.dev.json node scripts/dev-server.js
# http://localhost:3000 and http://localhost:3000/admin/signups
```

`SIGNUPS_DEV_FILE` stores signups in a local JSON file instead of Supabase (dev only).
