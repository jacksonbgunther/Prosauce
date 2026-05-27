const { useState, useEffect, useRef, useMemo } = React;

// ---------- Data ----------
const PRODUCTS = [
  {
    id: "chicken",
    name: "Creamy Chicken",
    fullName: "Creamy Chicken Protein Sauce",
    accent: "#E78431",
    cap: "#E78431",
    sauce: "#F1A455",
    deep: "#A85618",
    image: "bottle-chicken.png",
    descriptor: "Restaurant-style. Cane's-leaning. Warm, garlicky, peppered.",
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

// ---------- Top Marquee ----------
function Marquee() {
  const items = [
    "FREE SHIPPING ON 6-PACK +",
    "12G PROTEIN · 90 CAL",
    "NO SEED OILS",
    "NOW IN 1,200+ STORES",
    "WHEY ISOLATE PROTEIN SYSTEM",
    "NO ADDED SUGAR",
  ];
  const stream = [...items, ...items, ...items];
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
function Nav({ cartCount, onOpenCart }) {
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
          <a href="#shop" className="nav-link">Shop</a>
          <a href="#flavors" className="nav-link">Flavors</a>
          <a href="#nutrition" className="nav-link">Nutrition</a>
          <a href="#stores" className="nav-link">Where to Buy</a>
        </div>
        <a href="#top" className="wordmark">
          <BullMark size={26} />
          <span>ProSauce</span>
        </a>
        <div className="nav-right">
          <a href="#account" className="nav-link nav-link-muted">Account</a>
          <button className="cart-btn" onClick={onOpenCart} aria-label="Open cart">
            <span>Cart</span>
            <span className="cart-count">{cartCount}</span>
          </button>
        </div>
      </div>
    </nav>
  );
}

// ---------- Bull Mark (matches bottle logo) ----------
function BullMark({ size = 32, color = "#C8252C" }) {
  return (
    <svg width={size} height={size} viewBox="0 0 100 100" fill="none" aria-hidden="true">
      {/* Left horn — wide sweeping arc going up and out */}
      <path
        d="M40 38
           C 30 28, 18 22, 6 18
           C 8 12, 14 8, 22 8
           C 30 12, 38 22, 44 34 Z"
        fill={color}
      />
      {/* Right horn — wide sweeping arc going up and out */}
      <path
        d="M60 38
           C 70 28, 82 22, 94 18
           C 92 12, 86 8, 78 8
           C 70 12, 62 22, 56 34 Z"
        fill={color}
      />
      {/* Inner mane tufts between horns */}
      <path
        d="M44 30 C 46 22, 48 18, 50 14 C 52 18, 54 22, 56 30 Z"
        fill={color}
      />
      {/* Head — bull head facing forward with muzzle */}
      <path
        d="M32 42
           C 32 36, 38 32, 44 32
           L 56 32
           C 62 32, 68 36, 68 42
           L 70 54
           C 70 62, 66 68, 60 72
           L 56 78
           C 54 82, 50 84, 46 82
           C 42 82, 40 78, 40 76
           L 36 70
           C 32 64, 30 58, 30 50 Z"
        fill={color}
      />
      {/* Negative space — eyes/forehead gap */}
      <path
        d="M42 48
           C 44 44, 48 42, 50 42
           C 52 42, 56 44, 58 48
           L 56 56
           C 54 60, 50 62, 50 62
           C 50 62, 46 60, 44 56 Z"
        fill="#F2EBDB"
      />
    </svg>
  );
}

// ---------- Hero ----------
function Hero({ onAdd }) {
  return (
    <section className="hero" id="top">
      <div className="hero-grid">
        <div className="hero-copy">
          <div className="eyebrow">
            <span className="eyebrow-dash" />
            <span>Premium Sauce · Est. 2026</span>
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
              <div className="spec-num">90</div>
              <div className="spec-label">Calories<br/>per serving</div>
            </div>
            <div className="spec-divider" />
            <div className="spec">
              <div className="spec-num">0<span className="spec-unit">g</span></div>
              <div className="spec-label">Added<br/>sugar</div>
            </div>
          </div>
          <p className="hero-sub">
            Two real sauces — Creamy Chicken and Ranch — built on a whey isolate protein
            system. Restaurant-style flavor. Smooth, never chalky.
          </p>
          <div className="hero-ctas">
            <a href="#shop" className="btn btn-primary">Shop Now <span aria-hidden>→</span></a>
            <a href="#flavors" className="btn btn-ghost">View Flavors</a>
          </div>
          <div className="hero-meta">
            <span>★ ★ ★ ★ ★</span>
            <span className="hero-meta-divider">·</span>
            <span>4.8 from 2,431 reviews</span>
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
            <img src={PRODUCTS[0].image} alt="ProSauce Creamy Chicken bottle" />
          </div>
          <div className="hero-tag hero-tag-tl">
            <div className="hero-tag-num">01</div>
            <div className="hero-tag-text">Creamy<br/>Chicken</div>
          </div>
          <div className="hero-tag hero-tag-br">
            <div className="hero-tag-num">02</div>
            <div className="hero-tag-text">Restaurant<br/>Ranch</div>
          </div>
          <div className="hero-stamp">
            <svg viewBox="0 0 200 200" width="120" height="120">
              <defs>
                <path id="circ" d="M 100,100 m -78,0 a 78,78 0 1,1 156,0 a 78,78 0 1,1 -156,0" />
              </defs>
              <text className="stamp-text">
                <textPath href="#circ" startOffset="0">
                  · WHEY ISOLATE PROTEIN · NO SEED OILS · NO ADDED SUGAR ·
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
function ProductCard({ product, qty, setQty, onAdd, featured }) {
  const [hovered, setHovered] = useState(false);
  return (
    <div
      className={`product ${featured ? "product-featured" : ""}`}
      style={{ "--accent": product.accent, "--cap": product.cap, "--sauce": product.sauce, "--deep": product.deep }}
      onMouseEnter={() => setHovered(true)}
      onMouseLeave={() => setHovered(false)}
    >
      <div className="product-stage">
        <div className="product-stage-bg" />
        <div className="product-stage-letters" aria-hidden="true">
          {product.id === "chicken" ? "01" : "02"}
        </div>
        <img
          className={`product-bottle ${hovered ? "product-bottle-hover" : ""}`}
          src={product.image}
          alt={product.fullName}
        />
        {featured && <div className="product-badge">HERO FLAVOR</div>}
      </div>

      <div className="product-info">
        <div className="product-row">
          <div>
            <div className="product-eyebrow">{product.tagline}</div>
            <h3 className="product-name">{product.fullName}</h3>
          </div>
          <div className="product-price">$8.50</div>
        </div>

        <p className="product-desc">{product.descriptor}</p>

        <div className="product-specs">
          <div className="pspec">
            <div className="pspec-num">12g</div>
            <div className="pspec-label">PROTEIN</div>
          </div>
          <div className="pspec">
            <div className="pspec-num">90</div>
            <div className="pspec-label">CAL</div>
          </div>
          <div className="pspec">
            <div className="pspec-num">0g</div>
            <div className="pspec-label">ADDED SUGAR</div>
          </div>
        </div>

        <div className="product-use">
          <span>USE WITH</span>
          <span className="product-use-items">{product.use}</span>
        </div>

        <div className="product-cart">
          <div className="qty">
            <button onClick={() => setQty(Math.max(1, qty - 1))} aria-label="Decrease">−</button>
            <span>{qty}</span>
            <button onClick={() => setQty(qty + 1)} aria-label="Increase">+</button>
          </div>
          <button className="btn btn-primary product-add" onClick={() => onAdd(product, qty)}>
            Add to Cart · ${(8.5 * qty).toFixed(2)}
          </button>
        </div>
      </div>
    </div>
  );
}

// ---------- Product Lineup ----------
function Lineup({ onAdd }) {
  const [qtys, setQtys] = useState({ chicken: 1, ranch: 1 });
  return (
    <section className="lineup" id="flavors">
      <div className="lineup-inner">
        <SectionHead num="01" kicker="The Lineup" title={<>Two flavors.<br/>Built for everything.</>} />
        <div className="lineup-grid">
          <ProductCard
            product={PRODUCTS[0]}
            qty={qtys.chicken}
            setQty={(q) => setQtys({ ...qtys, chicken: q })}
            onAdd={onAdd}
            featured
          />
          <ProductCard
            product={PRODUCTS[1]}
            qty={qtys.ranch}
            setQty={(q) => setQtys({ ...qtys, ranch: q })}
            onAdd={onAdd}
          />
        </div>
        <BundleStrip onAdd={onAdd} />
      </div>
    </section>
  );
}

function BundleStrip({ onAdd }) {
  return (
    <div className="bundle">
      <div className="bundle-left">
        <div className="bundle-eyebrow">SAVE 15%</div>
        <div className="bundle-title">The Duo · 2-Bottle Bundle</div>
        <div className="bundle-sub">One Creamy Chicken. One Ranch. Free shipping.</div>
      </div>
      <div className="bundle-right">
        <div className="bundle-price">
          <span className="bundle-price-old">$17.00</span>
          <span className="bundle-price-new">$14.45</span>
        </div>
        <button
          className="btn btn-dark"
          onClick={() => {
            onAdd(PRODUCTS[0], 1);
            onAdd(PRODUCTS[1], 1);
          }}
        >
          Add Bundle
        </button>
      </div>
    </div>
  );
}

// ---------- Nutrition / Quality ----------
function Nutrition() {
  const facts = [
    { k: "Protein system", v: "Whey isolate", n: "01" },
    { k: "Texture", v: "Smooth · No chalk", n: "02" },
    { k: "Built for", v: "Everyday food use", n: "03" },
    { k: "Seed oils", v: "None", n: "04" },
    { k: "Added sugar", v: "Zero grams", n: "05" },
    { k: "Sourcing", v: "U.S. dairy", n: "06" },
  ];
  return (
    <section className="nutrition" id="nutrition">
      <div className="nutrition-inner">
        <SectionHead num="02" kicker="What's Inside" title={<>The short list.</>} />
        <div className="nutrition-grid">
          {facts.map((f) => (
            <div key={f.n} className="fact">
              <div className="fact-num">{f.n}</div>
              <div className="fact-k">{f.k}</div>
              <div className="fact-v">{f.v}</div>
            </div>
          ))}
        </div>
        <div className="nutrition-note">
          <span>NO HYPE.</span>
          <span>JUST SAUCE.</span>
        </div>
      </div>
    </section>
  );
}

// ---------- Lifestyle / On Anything ----------
function Lifestyle() {
  const tiles = [
    { id: "tenders", label: "CRISPY TENDERS", flavor: "Creamy Chicken", n: "01", aspect: "tall" },
    { id: "fries", label: "SHOESTRING FRIES", flavor: "Creamy Chicken", n: "02", aspect: "wide" },
    { id: "bowl", label: "GRAIN BOWL", flavor: "Ranch", n: "03", aspect: "wide" },
    { id: "veg", label: "ROASTED VEG", flavor: "Ranch", n: "04", aspect: "tall" },
    { id: "sando", label: "TURKEY SANDO", flavor: "Ranch", n: "05", aspect: "wide" },
    { id: "wing", label: "WINGS", flavor: "Creamy Chicken", n: "06", aspect: "tall" },
  ];
  return (
    <section className="lifestyle">
      <div className="lifestyle-inner">
        <SectionHead num="03" kicker="On Anything" title={<>Use it<br/>like a real sauce.</>} />
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
    <div className={`tile tile-${tile.aspect} tile-pos-${idx}`}>
      <div className="tile-img" aria-label={`Photo placeholder: ${tile.label}`}>
        <div className="tile-stripes" />
        <div className="tile-meta-tl">
          <div className="tile-num">{tile.n}</div>
          <div className="tile-flavor">{tile.flavor}</div>
        </div>
        <div className="tile-meta-br">
          <div className="tile-label">{tile.label}</div>
          <div className="tile-tag">FOOD PHOTO</div>
        </div>
      </div>
    </div>
  );
}

// ---------- Stores / Where to Buy ----------
function Stores() {
  const stores = ["Whole Foods", "Sprouts", "Erewhon", "Wegmans", "Bristol Farms", "H-E-B", "Gelson's", "The Fresh Market"];
  return (
    <section className="stores" id="stores">
      <div className="stores-inner">
        <div className="stores-head">
          <div className="section-kicker">
            <span className="section-num">04</span>
            <span className="section-line" />
            <span>On the shelf</span>
          </div>
          <h2 className="stores-title">Find ProSauce in the refrigerated condiment aisle.</h2>
        </div>
        <div className="stores-marquee">
          <div className="stores-track">
            {[...stores, ...stores].map((s, i) => (
              <span key={i} className="store-name">{s}</span>
            ))}
          </div>
        </div>
        <div className="stores-locator">
          <input className="locator-input" placeholder="Enter ZIP code" defaultValue="" />
          <button className="btn btn-dark">Find Stores</button>
        </div>
      </div>
    </section>
  );
}

// ---------- Big Footer CTA ----------
function FooterCTA({ onAdd }) {
  return (
    <section className="cta">
      <div className="cta-inner">
        <div className="cta-bigword" aria-hidden>PROSAUCE</div>
        <div className="cta-content">
          <div className="cta-line">12g protein. 90 calories.</div>
          <div className="cta-line cta-line-italic">Available in Creamy Chicken and Ranch.</div>
          <div className="cta-buttons">
            <button
              className="btn btn-primary btn-large"
              onClick={() => {
                onAdd(PRODUCTS[0], 1);
                onAdd(PRODUCTS[1], 1);
              }}
            >
              Shop ProSauce →
            </button>
          </div>
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
          <BullMark size={36} color="#F2EBDB" />
          <div className="foot-wordmark">ProSauce</div>
          <div className="foot-tag">Better sauces, upgraded nutrition.</div>
        </div>
        <div className="foot-cols">
          <div className="foot-col">
            <div className="foot-col-h">Shop</div>
            <a>Creamy Chicken</a>
            <a>Ranch</a>
            <a>The Duo</a>
            <a>6-Pack</a>
          </div>
          <div className="foot-col">
            <div className="foot-col-h">Brand</div>
            <a>Nutrition Facts</a>
            <a>Sourcing</a>
            <a>FAQ</a>
            <a>Reviews</a>
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

// ---------- Cart Drawer ----------
function CartDrawer({ open, onClose, items, setItems }) {
  const subtotal = useMemo(
    () => items.reduce((s, it) => s + it.qty * 8.5, 0),
    [items]
  );
  const updateQty = (id, delta) => {
    setItems(items
      .map((it) => (it.id === id ? { ...it, qty: it.qty + delta } : it))
      .filter((it) => it.qty > 0)
    );
  };
  return (
    <>
      <div className={`drawer-scrim ${open ? "drawer-scrim-open" : ""}`} onClick={onClose} />
      <aside className={`drawer ${open ? "drawer-open" : ""}`} aria-hidden={!open}>
        <div className="drawer-head">
          <div className="drawer-title">Your Cart</div>
          <button className="drawer-close" onClick={onClose} aria-label="Close cart">×</button>
        </div>
        <div className="drawer-body">
          {items.length === 0 ? (
            <div className="drawer-empty">
              <div className="drawer-empty-mark"><BullMark size={48} /></div>
              <div className="drawer-empty-title">Cart's empty.</div>
              <div className="drawer-empty-sub">Add a bottle to get started.</div>
            </div>
          ) : (
            items.map((it) => {
              const p = PRODUCTS.find((p) => p.id === it.id);
              return (
                <div key={it.id} className="drawer-item">
                  <div className="drawer-item-img" style={{ background: `linear-gradient(180deg, #ECEAE5 0%, ${p.sauce}33 100%)` }}>
                    <img src={p.image} alt="" />
                  </div>
                  <div className="drawer-item-info">
                    <div className="drawer-item-name">{p.fullName}</div>
                    <div className="drawer-item-price">${(8.5 * it.qty).toFixed(2)}</div>
                    <div className="qty qty-sm">
                      <button onClick={() => updateQty(it.id, -1)}>−</button>
                      <span>{it.qty}</span>
                      <button onClick={() => updateQty(it.id, 1)}>+</button>
                    </div>
                  </div>
                </div>
              );
            })
          )}
        </div>
        {items.length > 0 && (
          <div className="drawer-foot">
            <div className="drawer-totals">
              <span>Subtotal</span>
              <span className="drawer-total-num">${subtotal.toFixed(2)}</span>
            </div>
            <div className="drawer-shipping">FREE shipping on orders over $50</div>
            <button className="btn btn-primary btn-block">Checkout →</button>
          </div>
        )}
      </aside>
    </>
  );
}

// ---------- Toast (added to cart) ----------
function Toast({ msg }) {
  if (!msg) return null;
  return (
    <div className="toast">
      <div className="toast-dot" />
      <div>{msg}</div>
    </div>
  );
}

// ---------- App ----------
function App() {
  const [cart, setCart] = useState([]);
  const [drawerOpen, setDrawerOpen] = useState(false);
  const [toast, setToast] = useState("");

  const cartCount = cart.reduce((s, it) => s + it.qty, 0);

  const addToCart = (product, qty) => {
    setCart((prev) => {
      const existing = prev.find((it) => it.id === product.id);
      if (existing) {
        return prev.map((it) =>
          it.id === product.id ? { ...it, qty: it.qty + qty } : it
        );
      }
      return [...prev, { id: product.id, qty }];
    });
    setToast(`Added · ${product.name}`);
    setTimeout(() => setToast(""), 1800);
  };

  return (
    <div className="page">
      <Marquee />
      <Nav cartCount={cartCount} onOpenCart={() => setDrawerOpen(true)} />
      <Hero onAdd={addToCart} />
      <div id="shop" />
      <Lineup onAdd={addToCart} />
      <Nutrition />
      <Lifestyle />
      <Stores />
      <FooterCTA onAdd={addToCart} />
      <SiteFooter />
      <CartDrawer
        open={drawerOpen}
        onClose={() => setDrawerOpen(false)}
        items={cart}
        setItems={setCart}
      />
      <Toast msg={toast} />
    </div>
  );
}

ReactDOM.createRoot(document.getElementById("root")).render(<App />);
