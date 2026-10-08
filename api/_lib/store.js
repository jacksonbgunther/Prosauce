// Signup storage. Uses Supabase (Postgres) via its REST API in production.
// For local development only, set SIGNUPS_DEV_FILE to a JSON file path instead.
const fs = require("fs");

const TABLE = "signups";

function supabaseConfig() {
  const url = process.env.SUPABASE_URL;
  const key = process.env.SUPABASE_SERVICE_ROLE_KEY;
  if (url && key) return { url: url.replace(/\/$/, ""), key };
  return null;
}

function devFile() {
  return process.env.SIGNUPS_DEV_FILE || null;
}

function readDevFile(path) {
  try {
    return JSON.parse(fs.readFileSync(path, "utf8"));
  } catch {
    return [];
  }
}

async function supabaseRequest(cfg, path, init = {}) {
  const res = await fetch(`${cfg.url}/rest/v1/${path}`, {
    ...init,
    headers: {
      apikey: cfg.key,
      Authorization: `Bearer ${cfg.key}`,
      "Content-Type": "application/json",
      ...(init.headers || {}),
    },
  });
  if (!res.ok) {
    const text = await res.text().catch(() => "");
    throw new Error(`Supabase ${res.status}: ${text.slice(0, 300)}`);
  }
  return res;
}

async function insertSignup(row) {
  const cfg = supabaseConfig();
  if (cfg) {
    await supabaseRequest(cfg, TABLE, {
      method: "POST",
      headers: { Prefer: "return=minimal" },
      body: JSON.stringify(row),
    });
    return;
  }
  const file = devFile();
  if (file) {
    const rows = readDevFile(file);
    rows.push({ id: rows.length + 1, created_at: new Date().toISOString(), ...row });
    fs.writeFileSync(file, JSON.stringify(rows, null, 2));
    return;
  }
  throw new Error("Signup storage is not configured (set SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY).");
}

async function listSignups() {
  const cfg = supabaseConfig();
  if (cfg) {
    const res = await supabaseRequest(
      cfg,
      `${TABLE}?select=id,created_at,name,contact,contact_type,source,sms_consent&order=created_at.desc&limit=50000`
    );
    return res.json();
  }
  const file = devFile();
  if (file) {
    return readDevFile(file).sort((a, b) => (a.created_at < b.created_at ? 1 : -1));
  }
  throw new Error("Signup storage is not configured (set SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY).");
}

module.exports = { insertSignup, listSignups };
