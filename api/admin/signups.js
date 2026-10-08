// GET /api/admin/signups            -> JSON list of signups
// GET /api/admin/signups?format=csv -> CSV download
// Requires header "Authorization: Bearer <ADMIN_PASSWORD>".
const crypto = require("crypto");
const { listSignups } = require("../_lib/store");

function authorized(req) {
  const expected = process.env.ADMIN_PASSWORD;
  if (!expected) return false;
  const header = req.headers.authorization || "";
  const given = header.startsWith("Bearer ") ? header.slice(7) : "";
  const a = crypto.createHash("sha256").update(given).digest();
  const b = crypto.createHash("sha256").update(expected).digest();
  return crypto.timingSafeEqual(a, b);
}

function csvCell(value) {
  let s = value == null ? "" : String(value);
  // Neutralize spreadsheet formulas, but leave E.164 phone numbers alone.
  if (/^[=+\-@\t\r]/.test(s) && !/^\+\d+$/.test(s)) s = `'${s}`;
  return /[",\n\r]/.test(s) ? `"${s.replace(/"/g, '""')}"` : s;
}

function toCsv(rows) {
  const cols = ["name", "contact", "contact_type", "created_at", "source", "sms_consent"];
  const lines = [cols.join(",")];
  for (const r of rows) lines.push(cols.map((c) => csvCell(r[c])).join(","));
  return lines.join("\r\n") + "\r\n";
}

module.exports = async (req, res) => {
  res.setHeader("Cache-Control", "no-store");
  res.setHeader("X-Robots-Tag", "noindex");
  if (req.method !== "GET") {
    res.setHeader("Allow", "GET");
    return res.status(405).json({ error: "Method not allowed" });
  }
  if (!process.env.ADMIN_PASSWORD) {
    return res.status(500).json({ error: "ADMIN_PASSWORD is not set on the server." });
  }
  if (!authorized(req)) return res.status(401).json({ error: "Wrong password." });

  let rows;
  try {
    rows = await listSignups();
  } catch (err) {
    console.error("signup list failed", err);
    return res.status(500).json({ error: "Could not load signups." });
  }

  if ((req.query && req.query.format) === "csv") {
    const date = new Date().toISOString().slice(0, 10);
    res.setHeader("Content-Type", "text/csv; charset=utf-8");
    res.setHeader("Content-Disposition", `attachment; filename="prosauce-signups-${date}.csv"`);
    return res.status(200).send(toCsv(rows));
  }
  return res.status(200).json({ signups: rows });
};
