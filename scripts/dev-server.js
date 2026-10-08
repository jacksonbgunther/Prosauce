// Minimal local stand-in for Vercel: serves the static site (with clean URLs)
// and runs the functions in /api. Usage:
//   ADMIN_PASSWORD=test SIGNUPS_DEV_FILE=.signups.dev.json node scripts/dev-server.js
const http = require("http");
const fs = require("fs");
const path = require("path");

const ROOT = path.resolve(__dirname, "..");
const PORT = Number(process.env.PORT) || 3000;
const TYPES = {
  ".html": "text/html; charset=utf-8", ".js": "text/javascript", ".jsx": "text/babel",
  ".css": "text/css", ".png": "image/png", ".jpg": "image/jpeg", ".svg": "image/svg+xml", ".json": "application/json",
};

function decorate(res) {
  res.status = (code) => { res.statusCode = code; return res; };
  res.json = (obj) => { res.setHeader("Content-Type", "application/json"); res.end(JSON.stringify(obj)); return res; };
  res.send = (body) => { res.end(body); return res; };
  return res;
}

async function runApi(req, res, url) {
  const file = path.join(ROOT, url.pathname + ".js");
  const hidden = url.pathname.split("/").some((seg) => seg.startsWith("_"));
  if (!file.startsWith(path.join(ROOT, "api")) || hidden || !fs.existsSync(file)) {
    return decorate(res).status(404).json({ error: "Not found" });
  }
  let raw = "";
  for await (const chunk of req) raw += chunk;
  req.query = Object.fromEntries(url.searchParams);
  req.body = raw && /json/.test(req.headers["content-type"] || "") ? JSON.parse(raw) : raw;
  delete require.cache[require.resolve(file)];
  await require(file)(req, decorate(res));
}

function serveStatic(res, url) {
  let p = path.normalize(decodeURIComponent(url.pathname)).replace(/^(\.\.[/\\])+/, "");
  let file = path.join(ROOT, p);
  if (file.endsWith(path.sep)) file = path.join(file, "index.html");
  if (!fs.existsSync(file) && fs.existsSync(file + ".html")) file += ".html";
  if (!file.startsWith(ROOT) || !fs.existsSync(file) || fs.statSync(file).isDirectory()) {
    res.statusCode = 404;
    return res.end("Not found");
  }
  res.setHeader("Content-Type", TYPES[path.extname(file)] || "application/octet-stream");
  fs.createReadStream(file).pipe(res);
}

http.createServer((req, res) => {
  const url = new URL(req.url, `http://${req.headers.host}`);
  const handle = url.pathname.startsWith("/api/") ? runApi(req, res, url) : Promise.resolve(serveStatic(res, url));
  handle.catch((err) => {
    console.error(err);
    if (!res.headersSent) decorate(res).status(500).json({ error: "Dev server error" });
  });
}).listen(PORT, () => console.log(`ProSauce dev server on http://localhost:${PORT}`));
