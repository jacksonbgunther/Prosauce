// Classify and normalize the single "email or phone" contact field.
// Keep in sync with contactType() in prosauce-landing.jsx.
const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;

function parseContact(raw) {
  const v = String(raw || "").trim();
  if (!v) return null;
  if (v.includes("@")) {
    return EMAIL_RE.test(v) && v.length <= 254 ? { type: "email", value: v.toLowerCase() } : null;
  }
  const digits = v.replace(/\D/g, "");
  if (!/^[\d\s()+.\-]+$/.test(v) || digits.length < 10 || digits.length > 15) return null;
  // Store phones in E.164. Bare 10-digit numbers are assumed to be US.
  if (digits.length === 10) return { type: "phone", value: `+1${digits}` };
  return { type: "phone", value: `+${digits}` };
}

module.exports = { parseContact };
