const { useState, useEffect, useRef } = React;

// ---------- Data ----------
const PRODUCTS = [
  {
    id: "sweet-smoke",
    name: "Sweet Smoke",
    fullName: "Sweet Smoke Protein Sauce",
    accent: "#E78431",
    cap: "#E78431",
    sauce: "#F1A455",
    deep: "#A85618",
    image: "bottle-sweet-smoke.png",
    descriptor: "Sweet, smoky, tangy. The dipping sauce you already crave.",
    use: "Tenders · Fries · Wraps",
    tagline: "The dipper.",
  },
  {
    id: "ranch",
    name: "Ranch",
    fullName: "Protein Ranch Sauce",
    accent: "#3F6238",
    cap: "#2F4A2A",
    sauce: "#B5C19E",
    deep: "#1F3019",
    image: "bottle-ranch.png",
    descriptor: "Herb-forward, buttermilk-thick, dill + chive.",
    use: "Bowls · Veggies · Sandwiches",
    tagline: "The everyday.",
  },
];

const NOTIFY_LABEL = "Notify me for the next drop";
const SMS_CONSENT_TEXT =
  "By providing your phone number you agree to receive recurring marketing text messages from ProSauce. Message & data rates may apply. Reply STOP to opt out.";

const scrollToDrop = () => {
  const el = document.getElementById("drop");
  if (el) el.scrollIntoView({ behavior: "smooth", block: "start" });
};

// Returns "email", "phone", "invalid", or null (empty). Mirrors api/_lib/contact.js.
function contactType(raw) {
  const v = raw.trim();
  if (!v) return null;
  if (v.includes("@")) return /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v) ? "email" : "invalid";
  const digits = v.replace(/\D/g, "");
  if (/^[\d\s()+.\-]+$/.test(v) && digits.length >= 10 && digits.length <= 15) return "phone";
  return "invalid";
}

// ---------- Notify capture form ----------
function NotifyForm({ source, variant = "light", compact = false, collapsible = false }) {
  const [open, setOpen] = useState(!collapsible);
  const nameRef = useRef(null);
  const expand = () => {
    setOpen(true);
    setTimeout(() => nameRef.current && nameRef.current.focus(), 0);
  };
  const [name, setName] = useState("");
  const [contact, setContact] = useState("");
  const [consent, setConsent] = useState(false);
  const [honeypot, setHoneypot] = useState("");
  const [status, setStatus] = useState("idle"); // idle | sending | done | error
  const [error, setError] = useState("");

  const type = contactType(contact);
  const isPhone = type === "phone";

  const onSubmit = async (e) => {
    e.preventDefault();
    if (!open) return expand();
    setError("");
    if (!name.trim()) return setError("Please enter your name.");
    if (type !== "email" && type !== "phone") return setError("Enter a valid email or phone number.");
    if (isPhone && !consent) return setError("Please check the box to agree to text messages.");
    setStatus("sending");
    try {
      const res = await fetch("/api/signup", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, contact, source, smsConsent: isPhone && consent, company: honeypot }),
      });
      if (!res.ok) {
        const body = await res.json().catch(() => ({}));
        throw new Error(body.error || "Something went wrong. Please try again.");
      }
      setStatus("done");
    } catch (err) {
      setStatus("error");
      setError(err.message);
    }
  };

  if (status === "done") {
    return (
      <div className={`notify notify-${variant} notify-done`} role="status">
        <span className="notify-check" aria-hidden="true">✓</span>
        <span>You're on the list — we'll reach out when the next drop lands.</span>
      </div>
    );
  }

  const id = `notify-${source}`;
  return (
    <form className={`notify notify-${variant} ${compact ? "notify-compact" : ""} ${collapsible ? "notify-collapsible" : ""}`} onSubmit={onSubmit} noValidate>
      <div className={`notify-fields ${open ? "" : "notify-fields-closed"}`}>
        <div className="notify-reveal">
        <label className="sr-only" htmlFor={`${id}-name`}>Name</label>
        <input
          id={`${id}-name`}
          ref={nameRef}
          className="notify-input"
          type="text"
          autoComplete="name"
          placeholder="Name"
          value={name}
          maxLength={100}
          onChange={(e) => setName(e.target.value)}
        />
        <label className="sr-only" htmlFor={`${id}-contact`}>Email or phone number</label>
        <input
          id={`${id}-contact`}
          className="notify-input"
          type="text"
          inputMode="email"
          autoComplete="email"
          placeholder="Email or phone number"
          value={contact}
          maxLength={254}
          onChange={(e) => setContact(e.target.value)}
        />
        </div>
        <input
          className="notify-hp"
          type="text"
          tabIndex={-1}
          autoComplete="off"
          aria-hidden="true"
          value={honeypot}
          onChange={(e) => setHoneypot(e.target.value)}
        />
        <button className="btn btn-primary notify-btn" type="submit" disabled={status === "sending"}>
          {status === "sending" ? "Sending…" : NOTIFY_LABEL}
        </button>
      </div>
      {isPhone && (
        <label className="notify-consent">
          <input type="checkbox" checked={consent} onChange={(e) => setConsent(e.target.checked)} required />
          <span>I agree to receive recurring marketing text messages from ProSauce at this number.</span>
        </label>
      )}
      {error && <div className="notify-error" role="alert">{error}</div>}
      {open && <p className="notify-fine">{SMS_CONSENT_TEXT}</p>}
    </form>
  );
}

// ---------- Top Marquee ----------
function Marquee() {
  const items = [
    "FREE SHIPPING ON 6-PACK",
    "12G PROTEIN · 160 CAL",
  ];
  const stream = Array.from({ length: 8 }, () => items).flat();
  return (
    <div className="marquee">
      <div className="marquee-track">
        {stream.map((t, i) => (
          <span key={i} className="marquee-item">
            <span className="marquee-dot" />
            {t}
          </span>
        ))}
      </div>
    </div>
  );
}

// ---------- Nav ----------
function Nav() {
  const [scrolled, setScrolled] = useState(false);
  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 24);
    window.addEventListener("scroll", onScroll);
    return () => window.removeEventListener("scroll", onScroll);
  }, []);
  return (
    <nav className={`nav ${scrolled ? "nav-scrolled" : ""}`}>
      <div className="nav-inner">
        <div className="nav-left">
          <a href="#flavors" className="nav-link">Flavors</a>
          <a href="#sweet-smoke" className="nav-link">Sweet Smoke</a>
          <a href="#drop" className="nav-link">Next Drop</a>
        </div>
        <a href="#top" className="wordmark">
          <span>ProSauce</span>
        </a>
        <div className="nav-right">
          <button className="cart-btn" onClick={scrollToDrop}>
            <span>Notify Me</span>
          </button>
        </div>
      </div>
    </nav>
  );
}

// ---------- Hero ----------
function Hero() {
  return (
    <section className="hero" id="top">
      <div className="hero-grid">
        <div className="hero-copy">
          <div className="eyebrow">
            <span className="eyebrow-dash" />
            <span>Premium Sauce</span>
          </div>
          <h1 className="hero-title">
            <span>Better</span>
            <span>sauces,</span>
            <span className="hero-title-italic">upgraded</span>
            <span>nutrition.</span>
          </h1>
          <div className="hero-specs">
            <div className="spec">
              <div className="spec-num">12<span className="spec-unit">g</span></div>
              <div className="spec-label">Protein<br/>per serving</div>
            </div>
            <div className="spec-divider" />
            <div className="spec">
              <div className="spec-num">160</div>
              <div className="spec-label">Calories<br/>per serving</div>
            </div>
          </div>
          <p className="hero-sub">
            Two real sauces — Sweet Smoke and Ranch. Restaurant-style flavor.
            Smooth, never chalky.
          </p>
          <div className="hero-notify">
            <div className="hero-notify-label">
              <span className="sold-out-pill">Sold out</span>
              <span>The first drop is gone. Get first dibs on the next one.</span>
            </div>
            <NotifyForm source="hero" />
          </div>
        </div>

        <div className="hero-stage">
          <div className="hero-bigword" aria-hidden="true">
            <span>PRO</span>
            <span>SAUCE</span>
          </div>
          <div className="hero-bottle hero-bottle-back">
            <img src={PRODUCTS[1].image} alt="" />
          </div>
          <div className="hero-bottle hero-bottle-front">
            <img src={PRODUCTS[0].image} alt="ProSauce Sweet Smoke bottle" />
          </div>
          <div className="hero-tag hero-tag-tl">
            <div className="hero-tag-num">02</div>
            <div className="hero-tag-text">Restaurant<br/>Ranch</div>
          </div>
          <div className="hero-tag hero-tag-br">
            <div className="hero-tag-num">01</div>
            <div className="hero-tag-text">Sweet<br/>Smoke</div>
          </div>
          <div className="hero-stamp">
            <svg viewBox="0 0 200 200" width="120" height="120">
              <defs>
                <path id="circ" d="M 100,100 m -78,0 a 78,78 0 1,1 156,0 a 78,78 0 1,1 -156,0" />
              </defs>
              <text className="stamp-text">
                <textPath href="#circ" startOffset="0">
                  · 12G PROTEIN · 160 CALORIES · RESTAURANT STYLE ·
                </textPath>
              </text>
              <text x="100" y="95" textAnchor="middle" className="stamp-num">12g</text>
              <text x="100" y="115" textAnchor="middle" className="stamp-sub">PROTEIN</text>
            </svg>
          </div>
        </div>
      </div>
    </section>
  );
}

// ---------- Section Heading ----------
function SectionHead({ kicker, title, num }) {
  return (
    <div className="section-head">
      <div className="section-kicker">
        <span className="section-num">{num}</span>
        <span className="section-line" />
        <span>{kicker}</span>
      </div>
      <h2 className="section-title">{title}</h2>
    </div>
  );
}

// ---------- Product Card ----------
function ProductCard({ product }) {
  const [hovered, setHovered] = useState(false);
  return (
    <div
      className="product product-sold-out"
      style={{ "--accent": product.accent, "--cap": product.cap, "--sauce": product.sauce, "--deep": product.deep }}
      onMouseEnter={() => setHovered(true)}
      onMouseLeave={() => setHovered(false)}
    >
      <div className="product-stage">
        <div className="product-stage-bg" />
        <div className="product-stage-letters" aria-hidden="true">
          {product.id === "sweet-smoke" ? "01" : "02"}
        </div>
        <img
          className={`product-bottle ${hovered ? "product-bottle-hover" : ""}`}
          src={product.image}
          alt={product.fullName}
        />
        <div className="product-badge product-badge-sold">SOLD OUT</div>
      </div>

      <div className="product-info">
        <div className="product-row">
          <div>
            <div className="product-eyebrow">{product.tagline}</div>
            <h3 className="product-name">{product.fullName}</h3>
          </div>
          <div className="product-price">$12.99</div>
        </div>

        <p className="product-desc">{product.descriptor}</p>

        <div className="product-specs">
          <div className="pspec">
            <div className="pspec-num">12g</div>
            <div className="pspec-label">PROTEIN</div>
          </div>
          <div className="pspec">
            <div className="pspec-num">160</div>
            <div className="pspec-label">CAL</div>
          </div>
        </div>

        <div className="product-use">
          <span>USE WITH</span>
          <span className="product-use-items">{product.use}</span>
        </div>

        <NotifyForm source={`product-card-${product.id}`} compact collapsible />
      </div>
    </div>
  );
}

// ---------- Product Lineup ----------
function Lineup() {
  return (
    <section className="lineup" id="flavors">
      <div className="lineup-inner">
        <SectionHead num="01" kicker="The Lineup" title={<>Two flavors.<br/>Built for everything.</>} />
        <div className="lineup-grid">
          {PRODUCTS.map((p) => (
            <ProductCard key={p.id} product={p} />
          ))}
        </div>
      </div>
    </section>
  );
}

// ---------- Lifestyle / On Anything ----------
function Lifestyle() {
  const tiles = [
    { id: "tenders-dip", label: "CHICKEN TENDERS", flavor: "Sweet Smoke", n: "01", img: "images/dip-orange-sauce.jpg", alt: "Hand dipping a crispy chicken tender into orange dipping sauce", pos: "center 40%" },
    { id: "crispy-dip", label: "CRISPY CHICKEN", flavor: "Ranch", n: "02", img: "images/dip-white-sauce.jpg", alt: "Hand dipping crispy chicken into a pot of creamy white sauce", pos: "center 45%" },
    { id: "nuggets", label: "NUGGETS", flavor: "Ranch", n: "03", img: "images/nuggets-herb-sauce.jpg", alt: "Crispy nuggets with a bowl of white herb dipping sauce", pos: "40% center" },
    { id: "tenders", label: "CRISPY TENDERS", flavor: "Ranch", n: "04", img: "images/tenders-ramekin.jpg", alt: "Crispy fried chicken with a ramekin of white dipping sauce", pos: "center 62%" },
  ];
  return (
    <section className="lifestyle" id="ways">
      <div className="lifestyle-inner">
        <SectionHead num="02" kicker="On Anything" title={<>Use it<br/>like a real sauce.</>} />
        <div className="lifestyle-grid">
          {tiles.map((t, i) => (
            <PhotoTile key={t.id} tile={t} idx={i} />
          ))}
        </div>
      </div>
    </section>
  );
}

function PhotoTile({ tile, idx }) {
  return (
    <div className={`tile tile-pos-${idx}`}>
      <div className="tile-img">
        <img src={tile.img} alt={tile.alt} loading="lazy" style={{ objectPosition: tile.pos }} />
        <div className="tile-meta-tl">
          <div className="tile-num">{tile.n}</div>
          <div className="tile-flavor">{tile.flavor}</div>
        </div>
        <div className="tile-meta-br">
          <div className="tile-label">{tile.label}</div>
        </div>
      </div>
    </div>
  );
}

// ---------- Sweet Smoke feature ----------
function SweetSmoke() {
  return (
    <section className="sweet" id="sweet-smoke">
      <div className="sweet-inner">
        <div className="sweet-photo">
          <img
            src="images/dip-orange-sauce.jpg"
            alt="Chicken tender dipped in ProSauce Sweet Smoke sauce"
            loading="lazy"
          />
          <div className="sweet-photo-tag">Sweet Smoke</div>
        </div>
        <div className="sweet-copy">
          <div className="section-kicker sweet-kicker">
            <span className="section-num">03</span>
            <span className="section-line" />
            <span>Sweet Smoke</span>
          </div>
          <h2 className="section-title">Taste familiar?</h2>
          <p className="sweet-body">
            Our Sweet Smoke sauce is inspired by one of the most popular chicken sauces on the
            market. We just made it better.
          </p>
          <button className="btn btn-primary btn-large" onClick={scrollToDrop}>
            {NOTIFY_LABEL}
          </button>
        </div>
      </div>
    </section>
  );
}

// ---------- Next Drop signup ----------
function NextDrop() {
  return (
    <section className="cta" id="drop">
      <div className="cta-inner">
        <div className="cta-bigword" aria-hidden>PROSAUCE</div>
        <div className="cta-content">
          <div className="cta-kicker">
            <span className="sold-out-pill sold-out-pill-light">Sold out</span>
          </div>
          <h2 className="cta-line">The first drop sold out.</h2>
          <div className="cta-line cta-line-italic">Sweet Smoke and Ranch are back soon.</div>
          <p className="cta-sub">
            We're making the next batch now. Leave your name and an email or phone number and
            you'll be the first to know when it lands.
          </p>
          <NotifyForm source="drop-section" variant="dark" />
        </div>
        <div className="cta-bottles">
          <img src={PRODUCTS[0].image} alt="" />
          <img src={PRODUCTS[1].image} alt="" />
        </div>
      </div>
    </section>
  );
}

// ---------- Footer ----------
function SiteFooter() {
  return (
    <footer className="foot">
      <div className="foot-top">
        <div className="foot-brand">
          <div className="foot-wordmark">ProSauce</div>
          <div className="foot-tag">Better sauces, upgraded nutrition.</div>
        </div>
        <div className="foot-cols">
          <div className="foot-col">
            <div className="foot-col-h">Flavors</div>
            <a href="#flavors">Sweet Smoke</a>
            <a href="#flavors">Ranch</a>
            <a href="#drop">Next Drop</a>
          </div>
          <div className="foot-col">
            <div className="foot-col-h">Brand</div>
            <a>Nutrition Facts</a>
            <a>FAQ</a>
          </div>
          <div className="foot-col">
            <div className="foot-col-h">Support</div>
            <a>Contact</a>
            <a>Shipping</a>
            <a>Returns</a>
            <a>Wholesale</a>
          </div>
        </div>
      </div>
      <div className="foot-bottom">
        <div>© 2026 ProSauce Foods Co.</div>
        <div className="foot-legal">
          <span>Privacy</span>
          <span>Terms</span>
          <span>Accessibility</span>
        </div>
      </div>
    </footer>
  );
}

// ---------- App ----------
function App() {
  return (
    <div className="page">
      <Marquee />
      <Nav />
      <Hero />
      <Lineup />
      <Lifestyle />
      <SweetSmoke />
      <NextDrop />
      <SiteFooter />
    </div>
  );
}

ReactDOM.createRoot(document.getElementById("root")).render(<App />);
