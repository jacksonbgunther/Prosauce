"""Build the Shopify theme in shopify-theme/ from the generated index.html and privacy.html.

Run via `bash tools/build.sh` (it runs after gen_site.py/build_html.py), so the Shopify theme
always matches the Cloudflare site. Never hand-edit files in shopify-theme/; edit gen_site.py.

Differences from the Cloudflare build:
- Signup forms are Shopify customer forms (emails land in Shopify > Customers, tagged
  newsletter + launch-list + src-<source>, subscribed to email marketing).
- The Meta Pixel Lead / QualifiedLead events fire exactly as before. If the theme setting
  "Conversions API endpoint" is filled in, the same events (same event_id) are also POSTed there.
- /privacy becomes /pages/privacy (a Shopify page using the "privacy" template).
"""
import json, os, re, shutil, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'shopify-theme')
PIXEL = '1495416545782879'
GA = 'G-BTGXZ5LCFG'

home = open(os.path.join(ROOT, 'index.html'), encoding='utf-8').read()
priv = open(os.path.join(ROOT, 'privacy.html'), encoding='utf-8').read()

css = re.search(r'<style>(.*?)</style>', home, re.S).group(1)
fonts = re.search(r'(<link rel="preconnect".*?rel="stylesheet">)', home, re.S).group(1)
default_desc = re.search(r'<meta name="description" content="([^"]*)"', home).group(1)
default_title = re.search(r'<title>(.*?)</title>', home).group(1)
cookie = re.search(r'(<div id="cookie-note".*?</div>)\n<script>', home, re.S).group(1)
body = re.search(r'<div class="dk"[^>]*>\n(.*)\n</div>\n<div id="cookie-note"', home, re.S).group(1)
pbody = re.search(r'<div class="dk"[^>]*>\n(.*)\n</div>\n<div id="cookie-note"', priv, re.S).group(1)

ASSETS = set()


def liquidize(html):
    """Asset paths -> asset_url, site links -> Shopify paths, signup forms -> customer forms."""
    def a(m):
        ASSETS.add(m.group(1))
        return "{{ '%s' | asset_url }}" % m.group(1)
    html = re.sub(r'/assets/([\w.-]+)', a, html)
    html = html.replace('href="/privacy"', 'href="/pages/privacy"')

    def form(m):
        inner, = m.groups()
        src = re.search(r'id="em-([\w-]+)"', inner).group(1)
        inner = inner.replace('name="email"', 'name="contact[email]"')
        return ("{%% form 'customer', class: 'ef', novalidate: 'novalidate' %%}"
                '<input type="hidden" name="contact[tags]" value="newsletter,launch-list,src-%s">'
                '%s{%% endform %%}') % (src, inner)
    html = re.sub(r'<form class="ef" novalidate>(.*?)</form>', form, html, flags=re.S)
    if '/assets/' in html or 'href="/privacy"' in html or '<form class="ef"' in html:
        sys.exit('build_theme: unconverted reference left')
    return html


def schema(name, extra=None):
    s = {'name': name, 'tag': 'div', 'class': 'ts-sec'}
    s.update(extra or {})
    return '\n{% schema %}\n' + json.dumps(s, indent=2) + '\n{% endschema %}\n'


def w(path, text, binary=False):
    p = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, 'w', encoding='utf-8') as f:
        f.write(text)


# --- split the home page into sections ------------------------------------------------------
chunks = re.split(r'\n(?=  (?:<section |<div class="mq"|<header |<footer ))', body)
header_html = chunks[0] + '\n' + chunks[1]          # announcement bar + header
assert '<header class="hdr">' in header_html, 'header split moved'
footer_html = next(c for c in chunks if c.lstrip().startswith('<footer'))
middle = [c for c in chunks[2:] if c is not footer_html]

if os.path.isdir(OUT):
    shutil.rmtree(OUT)

w('sections/toon-header.liquid', liquidize(header_html).replace('href="/#', 'href="{{ routes.root_url }}#') + schema('Header'))
w('sections/toon-footer.liquid', liquidize(footer_html).replace('href="#top"', 'href="{{ routes.root_url }}"') + schema('Footer'))

NAMES = {'top': 'Hero', 'mq': 'Scrolling strip', 'compare': 'Comparison', 'gold-rush': 'Gold Rush showcase',
         'blandville': 'Blandville teaser', 'coming-soon': 'Cool Ranch teaser', 'new-flavors': 'New flavors signup', 'faq': 'FAQ'}
order, sections = [], {}
for c in middle:
    m = re.search(r'<section id="([\w-]+)"', c)
    key = m.group(1) if m else 'mq'
    fname = 'toon-' + ('hero' if key == 'top' else key)
    w(f'sections/{fname}.liquid', liquidize(c.strip()) + schema(NAMES[key], {'presets': [{'name': 'Toon: ' + NAMES[key]}]}))
    sid = fname.replace('toon-', '')
    order.append(sid)
    sections[sid] = {'type': fname}
w('templates/index.json', json.dumps({'sections': sections, 'order': order}, indent=2))

# --- privacy page ---------------------------------------------------------------------------
pmain = re.search(r'(<main class="wrap sec">.*?</main>)', pbody, re.S).group(1)
w('sections/toon-privacy.liquid', liquidize(pmain) + schema('Privacy policy'))
w('templates/page.privacy.json', json.dumps({'sections': {'main': {'type': 'toon-privacy'}}, 'order': ['main']}, indent=2))

# --- generic templates (page, product, collection, cart, search, 404) -----------------------
w('sections/toon-main.liquid', r'''<main class="wrap sec ts-main">
  {%- case request.page_type -%}
    {%- when 'page' -%}
      <div class="legaldoc"><h1 class="d h2">{{ page.title | escape }}</h1>{{ page.content }}</div>
    {%- when 'collection' -%}
      <h1 class="d h2">{{ collection.title | escape }}</h1>
      <div class="ts-grid">
        {%- for p in collection.products -%}
          <a class="ts-card" href="{{ p.url }}">{%- if p.featured_image -%}{{ p.featured_image | image_url: width: 600 | image_tag: loading: 'lazy', alt: p.title }}{%- endif -%}<span>{{ p.title | escape }}</span></a>
        {%- else -%}
          <p>Nothing here yet. <a class="js-dibs" href="{{ routes.root_url }}#signup">Get first dibs</a> on launch day.</p>
        {%- endfor -%}
      </div>
    {%- when 'cart' -%}
      <h1 class="d h2">Your cart</h1>
      {%- if cart.item_count > 0 -%}
        <form action="{{ routes.cart_url }}" method="post" class="ts-cart">
          {%- for item in cart.items -%}
            <p>{{ item.quantity }} &times; {{ item.product.title | escape }} <span>{{ item.final_line_price | money }}</span></p>
          {%- endfor -%}
          <p class="ts-total">Subtotal <span>{{ cart.total_price | money }}</span></p>
          <button type="submit" name="checkout" class="pill">Check out</button>
        </form>
      {%- else -%}
        <p>Your cart is empty.</p>
      {%- endif -%}
    {%- when 'search' -%}
      <h1 class="d h2">Search</h1>
      <form action="{{ routes.search_url }}" class="ef"><label class="sr" for="q">Search</label><input id="q" type="search" name="q" value="{{ search.terms | escape }}" placeholder="Search"><button class="pill">Search</button></form>
      {%- for r in search.results -%}<p><a href="{{ r.url }}">{{ r.title | escape }}</a></p>{%- endfor -%}
    {%- else -%}
      <h1 class="d h2">This page went to Blandville.</h1>
      <p>It's not coming back. <a href="{{ routes.root_url }}">Head home</a>.</p>
  {%- endcase -%}
</main>
''' + schema('Main content'))
for t in ['page', 'collection', 'list-collections', 'cart', 'search', '404']:
    w(f'templates/{t}.json', json.dumps({'sections': {'main': {'type': 'toon-main'}}, 'order': ['main']}, indent=2))

w('sections/toon-product.liquid', r'''<main class="wrap sec ts-product">
  <div class="ts-pmedia">
    {%- assign img = product.selected_or_first_available_variant.featured_image | default: product.featured_image -%}
    {%- if img -%}{{ img | image_url: width: 1200 | image_tag: alt: product.title, sizes: '(min-width: 900px) 50vw, 100vw' }}{%- else -%}<img src="{{ 'bottle-v3.png' | asset_url }}" alt="{{ product.title | escape }}">{%- endif -%}
  </div>
  <div class="ts-pinfo">
    <h1 class="d h2">{{ product.title | escape }}</h1>
    <div class="ts-pdesc">{{ product.description }}</div>
    {%- if product.available and product.price > 0 -%}
      <p class="ts-price">{{ product.selected_or_first_available_variant.price | money }}</p>
      {%- form 'product', product -%}
        {%- if product.has_only_default_variant -%}
          <input type="hidden" name="id" value="{{ product.selected_or_first_available_variant.id }}">
        {%- else -%}
          <label class="sr" for="v">Option</label>
          <select id="v" name="id">{%- for v in product.variants -%}<option value="{{ v.id }}" {% unless v.available %}disabled{% endunless %}>{{ v.title | escape }}</option>{%- endfor -%}</select>
        {%- endif -%}
        <button type="submit" class="pill">Add to cart</button>
      {%- endform -%}
    {%- else -%}
      <p class="ts-soon">Not on sale yet.</p>
      <a class="pill js-dibs" href="{{ routes.root_url }}#signup">Get first dibs</a>
    {%- endif -%}
  </div>
</main>
''' + schema('Product'))
w('templates/product.json', json.dumps({'sections': {'main': {'type': 'toon-product'}}, 'order': ['main']}, indent=2))

# --- password page (what visitors see while the store is locked) ----------------------------
hero_signup = re.search(r'(<div class="signup" data-source="hero".*?</p>\s*</div>)', body, re.S).group(1)
pw_signup = liquidize(hero_signup.replace('data-source="hero" id="signup"', 'data-source="password" id="signup"').replace('em-hero', 'em-password'))
w('sections/toon-password.liquid', r'''<main class="ts-pw">
  <img class="ts-pw-logo" src="{{ 'logo.webp' | asset_url }}" alt="Toon Sauce" width="320" height="160">
  <h1 class="d">Your favorite sauce.<br><span class="amb">Now with 70g of protein.</span></h1>
  <p class="ts-pw-sub">Gold Rush drops first. Sweet, smoky, made with real honey. 7g protein per serving.</p>
  <div class="ts-pw-form">''' + pw_signup + r'''</div>
  <img class="ts-pw-bottle" src="{{ 'bottle-v3.png' | asset_url }}" alt="Toon Sauce Gold Rush bottle" width="300" height="600">
  <details class="ts-pw-owner">
    <summary>Store password</summary>
    {%- form 'storefront_password' -%}
      {%- if form.errors -%}<p class="err">Wrong password.</p>{%- endif -%}
      <label class="sr" for="pw">Password</label>
      <input id="pw" type="password" name="password" autocomplete="current-password" placeholder="Password">
      <button type="submit" class="pill pill-cream">Enter</button>
    {%- endform -%}
  </details>
  <p class="ts-pw-legal">&#169; {{ 'now' | date: '%Y' }} Toon Sauce &middot; <a href="https://www.instagram.com/toonsauce">@toonsauce</a></p>
</main>
''' + schema('Password page'))
w('templates/password.json', json.dumps({'layout': 'password', 'sections': {'main': {'type': 'toon-password'}}, 'order': ['main']}, indent=2))

# --- CSS -----------------------------------------------------------------------------------
EXTRA_CSS = r'''
/* ---- Shopify-only additions ---- */
.ts-main{min-height:50vh;padding-top:clamp(40px,6vw,90px);padding-bottom:clamp(40px,6vw,90px)}
.ts-main p,.ts-main li{font-size:17px;line-height:1.6;color:rgba(246,238,223,.85)}
.ts-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:24px;margin-top:28px}
.ts-card{display:flex;flex-direction:column;gap:10px;text-decoration:none;font-weight:600}
.ts-card img{border-radius:18px;background:var(--bg2);aspect-ratio:1;object-fit:contain;width:100%;height:auto}
.ts-cart p{display:flex;justify-content:space-between;max-width:560px;border-bottom:1px solid var(--line);padding:12px 0;margin:0}
.ts-cart .pill{margin-top:22px}
.ts-product{display:grid;grid-template-columns:1fr 1fr;gap:clamp(28px,5vw,80px);align-items:center;padding-top:clamp(40px,6vw,90px);padding-bottom:clamp(40px,6vw,90px)}
.ts-pmedia img{width:100%;height:auto;max-height:640px;object-fit:contain}
.ts-pinfo{display:flex;flex-direction:column;align-items:flex-start;gap:18px}
.ts-pdesc{font-size:17px;line-height:1.6;color:rgba(246,238,223,.85)}
.ts-price{font:600 26px Fredoka,system-ui,sans-serif;margin:0;color:var(--amber)}
.ts-soon{margin:0;color:rgba(246,238,223,.7)}
.ts-product select{min-height:52px;border-radius:14px;padding:0 14px;margin-bottom:12px;font:inherit}
@media (max-width:760px){.ts-product{grid-template-columns:1fr}}
.ts-pw{min-height:100vh;display:flex;flex-direction:column;align-items:center;text-align:center;gap:20px;padding:48px 20px 32px;background:radial-gradient(ellipse at 50% 85%,rgba(242,169,59,.18),transparent 60%),var(--bg);color:var(--cream);font-family:Fredoka,system-ui,sans-serif}
.ts-pw-logo{height:auto;width:min(260px,60vw)}
.ts-pw h1{font-size:clamp(36px,5.4vw,68px)}
.ts-pw-sub{margin:0;max-width:520px;font-size:18px;line-height:1.5;color:rgba(246,238,223,.8)}
.ts-pw-form{width:100%;max-width:520px;text-align:left}
.ts-pw-bottle{width:auto;height:clamp(260px,34vh,380px);filter:drop-shadow(0 24px 40px rgba(0,0,0,.6))}
.ts-pw-owner{margin-top:auto;font-size:14px;color:rgba(246,238,223,.6)}
.ts-pw-owner summary{cursor:pointer;min-height:44px;display:flex;align-items:center;justify-content:center}
.ts-pw-owner form{display:flex;gap:10px;margin-top:10px}
.ts-pw-owner input{min-height:52px;border-radius:999px;border:1px solid var(--line);background:var(--bg2);color:var(--cream);padding:0 18px;font:inherit}
.ts-pw-legal{margin:0;font-size:13px;color:rgba(246,238,223,.5)}
'''
# CSS sits in the same CDN folder as the images, so plain relative urls work there.
w('assets/toon.css', re.sub(r'/assets/([\w.-]+)', r'\1', css) + EXTRA_CSS)

# --- JS (signup + pixel + cookie notice) -----------------------------------------------------
w('assets/toon.js', r'''(function(){
  var RE=/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;
  var ANSWERS=['Protein shakes','Meat & eggs','Protein snacks',"I don't really track it"];
  var CFG=window.TOON||{};
  function ck(n){var m=document.cookie.match('(?:^|; )'+n+'=([^;]*)');return m?decodeURIComponent(m[1]):'';}
  function fbc(){var c=ck('_fbc');if(c)return c;var id=new URLSearchParams(location.search).get('fbclid');return id?'fb.1.'+Date.now()+'.'+id:'';}
  function eid(){return (window.crypto&&crypto.randomUUID)?crypto.randomUUID():Date.now().toString(36)+'-'+Math.random().toString(36).slice(2);}
  // Optional server-side Conversions API (same event_id as the pixel, for deduplication).
  function capi(p){if(!CFG.leadEndpoint)return;p.fbp=ck('_fbp');p.fbc=fbc();p.url=location.href;
    try{fetch(CFG.leadEndpoint,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(p),keepalive:true}).catch(function(){});}catch(e){}}
  function esc(s){return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/"/g,'&quot;');}
  function fail(box,input,btn,msg){var e=box.querySelector('.err');e.textContent=msg;e.hidden=false;input.setAttribute('aria-invalid','true');if(btn){btn.disabled=false;btn.textContent='Get first dibs';}input.focus();}
  function lead(box,email,source,id){
    if(typeof fbq==='function')fbq('track','Lead',{content_name:'launch_list',signup_source:source},{eventID:id});
    capi({event_name:'Lead',event_id:id,email:email,source:source});
    success(box,email,source);
  }
  var native=false;
  document.addEventListener('submit',function(ev){
    var form=ev.target; if(native||!form.classList||!form.classList.contains('ef')||!form.closest('.signup'))return;
    ev.preventDefault();
    var box=form.closest('.signup'),input=form.querySelector('input[type=email]'),btn=form.querySelector('button');
    var email=(input.value||'').trim().toLowerCase();
    if(!RE.test(email)){fail(box,input,null,'Please enter a valid email address.');return;}
    box.querySelector('.err').hidden=true;input.removeAttribute('aria-invalid');input.value=email;
    btn.disabled=true;btn.textContent='Saving…';
    var id=eid(),source=box.getAttribute('data-source')||'hero';
    fetch(form.action,{method:'POST',body:new FormData(form),credentials:'same-origin'})
      .then(function(r){
        if(/\/challenge/.test(r.url)){ // Shopify wants a captcha: hand over to a normal form post
          try{sessionStorage.setItem('ts_pending',JSON.stringify({email:email,source:source,id:id}));}catch(e){}
          native=true;form.submit();return;}
        if(!r.ok)throw r;
        lead(box,email,source,id);
      })
      .catch(function(){fail(box,input,btn,'Something went wrong. Please try again.');});
  });
  // Back from a captcha round-trip
  if(/customer_posted=true/.test(location.search)){try{var p=JSON.parse(sessionStorage.getItem('ts_pending')||'null');sessionStorage.removeItem('ts_pending');
    if(p){var b=document.querySelector('.signup[data-source="'+p.source+'"]')||document.querySelector('.signup');if(b){lead(b,p.email,p.source,p.id);b.scrollIntoView({block:'center'});}}}catch(e){}}

  function success(box,email,source){
    box.innerHTML='<div class="ok" role="status" tabindex="-1"><p class="okh">You’re on the list. Gary says thanks. He’s not great at saying no.</p>'+
      '<p class="q">How do you usually get your protein?</p><div class="qs">'+
      ANSWERS.map(function(a){return '<button type="button" data-a="'+esc(a)+'">'+esc(a)+'</button>';}).join('')+'</div></div>';
    var ok=box.querySelector('.ok');ok.focus({preventScroll:true});
    box.querySelectorAll('.qs button').forEach(function(b){b.addEventListener('click',function(){
      var a=b.getAttribute('data-a'),id=eid();
      if(typeof fbq==='function')fbq('trackCustom','QualifiedLead',{protein_source:a},{eventID:id});
      capi({event_name:'QualifiedLead',event_id:id,email:email,source:source,protein_source:a});
      ok.innerHTML='<p class="okh">You’re on the list. Gary says thanks. He’s not great at saying no.</p><p class="done">Got it. See you on launch day.</p>';
    });});
  }

  function dibs(){var s=document.getElementById('signup');if(!s)return false;
    s.scrollIntoView({behavior:'smooth',block:'center'});var i=s.querySelector('input[type=email]');
    if(i)setTimeout(function(){i.focus({preventScroll:true});},400);return true;}
  document.addEventListener('click',function(ev){var a=ev.target.closest&&ev.target.closest('a.js-dibs');
    if(a&&document.getElementById('signup')){ev.preventDefault();dibs();}});
  if(location.hash==='#signup')window.addEventListener('load',dibs);

  var cn=document.getElementById('cookie-note');
  try{if(cn&&!localStorage.getItem('ts_cookie_ok'))cn.hidden=false;}catch(e){if(cn)cn.hidden=false;}
  if(cn)cn.querySelector('button').addEventListener('click',function(){cn.hidden=true;try{localStorage.setItem('ts_cookie_ok','1');}catch(e){}});
})();
''')

# --- layouts ---------------------------------------------------------------------------------
HEAD = r'''<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="facebook-domain-verification" content="r4as0ai3v45suzltbwqpyd1kb8acv7" />
<script async src="https://www.googletagmanager.com/gtag/js?id=''' + GA + r'''"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag('js',new Date());gtag('config',\'''' + GA + r'''');</script>
<!-- Meta Pixel Code -->
<script>
!function(f,b,e,v,n,t,s)
{if(f.fbq)return;n=f.fbq=function(){n.callMethod?
n.callMethod.apply(n,arguments):n.queue.push(arguments)};
if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
n.queue=[];t=b.createElement(e);t.async=!0;
t.src=v;s=b.getElementsByTagName(e)[0];
s.parentNode.insertBefore(t,s)}(window, document,'script',
'https://connect.facebook.net/en_US/fbevents.js');
fbq('init', \'''' + PIXEL + r'''');
fbq('track', 'PageView');
</script>
<noscript><img height="1" width="1" style="display:none"
src="https://www.facebook.com/tr?id=''' + PIXEL + r'''&ev=PageView&noscript=1"
/></noscript>
<!-- End Meta Pixel Code -->
{%- liquid
  assign t = page_title
  if template.name == 'index' or t == blank
    assign t = "''' + default_title + r'''"
  elsif template.name == 'password'
    assign t = "''' + default_title + r'''"
  else
    assign t = page_title | append: ' | Toon Sauce'
  endif
  assign d = page_description | default: "''' + default_desc + r'''"
  if template.name == 'index'
    assign d = "''' + default_desc + r'''"
  endif
-%}
<title>{{ t | escape }}</title>
<meta name="description" content="{{ d | escape }}">
<meta property="og:title" content="{{ t | escape }}">
<meta property="og:description" content="{{ d | escape }}">
<meta property="og:image" content="https:{{ 'hero-pour-cream-soft.jpg' | asset_url }}">
<meta name="theme-color" content="#141414">
<link rel="icon" href="{{ 'favicon.png' | asset_url }}">
<link rel="canonical" href="{{ canonical_url }}">
''' + fonts + r'''
{{ 'toon.css' | asset_url | stylesheet_tag }}
<script>window.TOON={leadEndpoint:{{ settings.lead_endpoint | json }}};</script>
{{ content_for_header }}'''
ASSETS.add('favicon.png'); ASSETS.add('hero-pour-cream-soft.jpg'); ASSETS.add('logo.webp'); ASSETS.add('bottle-v3.png')

cookie_l = liquidize(cookie)
w('layout/theme.liquid', '''<!doctype html>
<html lang="{{ request.locale.iso_code }}">
<head>
''' + HEAD + '''
</head>
<body>
<div class="dk" style="font-family: 'Fredoka', system-ui, sans-serif; color: #F6EEDF; background: #141414; overflow-x: clip">
{% section 'toon-header' %}
{{ content_for_layout }}
{% section 'toon-footer' %}
</div>
''' + cookie_l + '''
<script src="{{ 'toon.js' | asset_url }}" defer></script>
</body>
</html>
''')
w('layout/password.liquid', '''<!doctype html>
<html lang="{{ request.locale.iso_code }}">
<head>
''' + HEAD + '''
</head>
<body>
<div class="dk">
{{ content_for_layout }}
</div>
<script src="{{ 'toon.js' | asset_url }}" defer></script>
</body>
</html>
''')

# --- config / locales ------------------------------------------------------------------------
w('config/settings_schema.json', json.dumps([
    {'name': 'theme_info', 'theme_name': 'Toon Sauce', 'theme_version': '1.0.0', 'theme_author': 'Toon Sauce',
     'theme_documentation_url': 'https://toonsauce.com', 'theme_support_url': 'https://toonsauce.com'},
    {'name': 'Tracking', 'settings': [
        {'type': 'paragraph', 'content': 'Meta Pixel 1495416545782879 and GA4 G-BTGXZ5LCFG are built into the theme. Do not also connect the Pixel in the Facebook & Instagram app, or events will double-count.'},
        {'type': 'text', 'id': 'lead_endpoint', 'label': 'Conversions API endpoint (optional)',
         'info': 'If set, signups are also POSTed here with the same event_id as the Pixel, e.g. https://toonsauce.pages.dev/api/lead (the endpoint must allow CORS from this store).'}]}
], indent=2))
w('config/settings_data.json', json.dumps({'current': {'lead_endpoint': ''}}, indent=2))
w('locales/en.default.json', json.dumps({'general': {'password_page': {'login_form_heading': 'Store password'}}}, indent=2))

# --- images ----------------------------------------------------------------------------------
for name in sorted(ASSETS):
    shutil.copy(os.path.join(ROOT, 'assets', name), os.path.join(OUT, 'assets', name))
print('wrote shopify-theme/ with', len(ASSETS), 'images and sections:', ', '.join(order))
