// POST /api/signup — "notify me for the next drop" capture.
const { parseContact } = require("./_lib/contact");
const { insertSignup } = require("./_lib/store");

const SOURCE_RE = /^[a-z0-9-]{1,64}$/;

module.exports = async (req, res) => {
  if (req.method !== "POST") {
    res.setHeader("Allow", "POST");
    return res.status(405).json({ error: "Method not allowed" });
  }

  const body = typeof req.body === "string" ? safeJson(req.body) : req.body || {};

  // Honeypot: real visitors never fill the hidden "company" field. Pretend success for bots.
  if (body.company) return res.status(200).json({ ok: true });

  const name = String(body.name || "").trim().slice(0, 100);
  const contact = parseContact(body.contact);
  const source = SOURCE_RE.test(String(body.source || "")) ? body.source : "unknown";
  const smsConsent = body.smsConsent === true;

  if (!name) return res.status(400).json({ error: "Please enter your name." });
  if (!contact) return res.status(400).json({ error: "Enter a valid email or phone number." });
  if (contact.type === "phone" && !smsConsent) {
    return res.status(400).json({ error: "Please check the box to agree to text messages." });
  }

  try {
    await insertSignup({
      name,
      contact: contact.value,
      contact_type: contact.type,
      source,
      sms_consent: contact.type === "phone" ? smsConsent : false,
    });
  } catch (err) {
    console.error("signup insert failed", err);
    return res.status(500).json({ error: "Something went wrong. Please try again." });
  }
  return res.status(200).json({ ok: true });
};

function safeJson(s) {
  try {
    return JSON.parse(s);
  } catch {
    return {};
  }
}
