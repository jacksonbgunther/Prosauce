// Cloudflare Pages Function: POST /api/lead
// Receives launch-list signups from the hero and footer forms, then (in the background):
//   1. sends a server-side event to the Meta Conversions API (same event_id as the browser pixel, so Meta deduplicates)
//   2. upserts the profile in Klaviyo (if configured)
//   3. keeps a backup copy in Workers KV (if a SIGNUPS binding exists)
//
// Environment variables (Cloudflare Pages > Settings > Variables and Secrets):
//   META_CAPI_TOKEN        required for Conversions API (secret, never sent to the browser)
//   META_TEST_EVENT_CODE   optional, for testing in Meta Events Manager
//   KLAVIYO_API_KEY        optional, Klaviyo private API key (secret)
//   KLAVIYO_LIST_ID        optional, Klaviyo list to subscribe new emails to
// Optional binding: SIGNUPS (Workers KV namespace)

const PIXEL_ID = '1495416545782879';
const GRAPH = 'https://graph.facebook.com/v21.0';
const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;
const ANSWERS = ['Protein shakes', 'Meat & eggs', 'Protein snacks', "I don't really track it"];

const json = (body, status = 200) =>
  new Response(JSON.stringify(body), { status, headers: { 'Content-Type': 'application/json', 'Cache-Control': 'no-store' } });

async function sha256(s) {
  const d = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(s));
  return [...new Uint8Array(d)].map((b) => b.toString(16).padStart(2, '0')).join('');
}

function clean(s, max = 300) {
  return typeof s === 'string' ? s.trim().slice(0, max) : '';
}

async function sendCapi(env, ev) {
  const body = { data: [ev], access_token: env.META_CAPI_TOKEN };
  if (env.META_TEST_EVENT_CODE) body.test_event_code = env.META_TEST_EVENT_CODE;
  const r = await fetch(`${GRAPH}/${PIXEL_ID}/events`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
  if (!r.ok) console.error('CAPI error', r.status, await r.text());
}

async function sendKlaviyo(env, email, props, subscribe, source) {
  const headers = {
    Authorization: `Klaviyo-API-Key ${env.KLAVIYO_API_KEY}`,
    revision: '2024-10-15',
    'Content-Type': 'application/vnd.api+json',
    Accept: 'application/vnd.api+json',
  };
  const r = await fetch('https://a.klaviyo.com/api/profile-import', {
    method: 'POST',
    headers,
    body: JSON.stringify({ data: { type: 'profile', attributes: { email, properties: props } } }),
  });
  if (!r.ok) console.error('Klaviyo profile error', r.status, await r.text());
  if (subscribe && env.KLAVIYO_LIST_ID) {
    const s = await fetch('https://a.klaviyo.com/api/profile-subscription-bulk-create-jobs', {
      method: 'POST',
      headers,
      body: JSON.stringify({
        data: {
          type: 'profile-subscription-bulk-create-job',
          attributes: {
            custom_source: `toonsauce.com ${source} form`,
            profiles: { data: [{ type: 'profile', attributes: { email, subscriptions: { email: { marketing: { consent: 'SUBSCRIBED' } } } } }] },
          },
          relationships: { list: { data: { type: 'list', id: env.KLAVIYO_LIST_ID } } },
        },
      }),
    });
    if (!s.ok) console.error('Klaviyo subscribe error', s.status, await s.text());
  }
}

export async function onRequestPost(context) {
  const { request, env } = context;
  let b;
  try {
    b = await request.json();
  } catch {
    return json({ ok: false, error: 'bad_request' }, 400);
  }

  const email = clean(b.email, 254).toLowerCase();
  if (!EMAIL_RE.test(email)) return json({ ok: false, error: 'invalid_email' }, 400);

  const eventName = b.event_name === 'QualifiedLead' ? 'QualifiedLead' : 'Lead';
  const eventId = clean(b.event_id, 100);
  if (!eventId) return json({ ok: false, error: 'missing_event_id' }, 400);

  const source = ['hero', 'footer', 'flavors'].includes(b.source) ? b.source : 'hero';
  const proteinSource = ANSWERS.includes(b.protein_source) ? b.protein_source : '';
  if (eventName === 'QualifiedLead' && !proteinSource) return json({ ok: false, error: 'invalid_answer' }, 400);

  const origin = new URL(request.url).origin;
  const pageUrl = clean(b.url, 1000);
  const eventSourceUrl = pageUrl.startsWith(origin) ? pageUrl : origin + '/';

  const userData = {
    em: [await sha256(email)],
    client_ip_address: request.headers.get('CF-Connecting-IP') || undefined,
    client_user_agent: request.headers.get('User-Agent') || undefined,
    fbp: clean(b.fbp) || undefined,
    fbc: clean(b.fbc) || undefined,
  };

  const ev = {
    event_name: eventName,
    event_time: Math.floor(Date.now() / 1000),
    event_id: eventId,
    action_source: 'website',
    event_source_url: eventSourceUrl,
    user_data: userData,
    custom_data: eventName === 'QualifiedLead' ? { protein_source: proteinSource } : { content_name: 'launch_list', signup_source: source },
  };

  const tasks = [];
  if (env.META_CAPI_TOKEN) tasks.push(sendCapi(env, ev));
  if (env.KLAVIYO_API_KEY) {
    const props = eventName === 'Lead' ? { signup_source: source } : { protein_source: proteinSource };
    tasks.push(sendKlaviyo(env, email, props, eventName === 'Lead', source));
  }
  if (env.SIGNUPS) {
    const key = `${email}`;
    tasks.push(
      env.SIGNUPS.get(key, 'json').then((prev) =>
        env.SIGNUPS.put(key, JSON.stringify({
          ...(prev || { created_at: new Date().toISOString(), signup_source: source }),
          ...(proteinSource ? { protein_source: proteinSource } : {}),
          updated_at: new Date().toISOString(),
        }))
      )
    );
  }

  // Don't make the visitor wait on Meta or Klaviyo.
  context.waitUntil(Promise.allSettled(tasks));
  return json({ ok: true });
}

export async function onRequest() {
  return json({ ok: false, error: 'method_not_allowed' }, 405);
}
