import re,sys
SRC,OUT=sys.argv[1],sys.argv[2]
BLOBS={'f7fb7fc75eb90a57b3401d26bf09f48a':'label-gold.jpg','4910612f0c49c55d773e0893022636c6':'label-ranch.jpg','bb0d3d703726ac6a1a153859fdd42cd8':'flav-gold.webp','df548f08a5edb9ce86468574702abb83':'flav-ranch.webp','5cfa14f150a9fc4e986958e12f8b0b87':'cool-ranch-cutout.png','daa7e183713fbe3db835079efdf8f638':'gold-rush-cutout.png','280a4fdca1012bc22881e49d23e113e7':'comic-1-p1.webp','488665257e3b781dfa481d2a965ca2ee':'comic-1-p2.webp','d14db648fa21528780bcb920de943618':'comic-1-p3.webp','99f59a3258732444c6084ff3cec970a9':'comic-1-p4.webp','aa6d6e10b4a6b483bff06d6e657a63f8':'comic-1-p5.webp','67412214d7f5f56e2a0588f9fb763778':'comic-1-p6.webp','2d171b11115654d39adbdac00cca72e0':'cool-ranch-bottle.webp','07a84f97473ae4299816b01338cb96f1':'gold-rush-bottle.webp','0d7c67247f19fad2249d92b66b33e716':'hero-pour.jpg','eae2e239f28e5ae06a9c190a3d8220a5':'packaging.webp','aef8a89a7ba7bd61866cb23c63a6d223':'mascot-chicken.webp','3d8e39985848625c5486dbca8eaeeba0':'mascot-bee.webp','4d59e0b58768617d499a9a1a043a7ddb':'mascot-pepper.webp','ab1cc38599b81a6661b718c26aecf212':'mascot-cat.webp','0dd5d257bfb9b2f73f03415c58960666':'logo.webp','702f6e1ee142d527b7e73583fbd5b726':'grain.png','98188e94ec406a38ba00bfa51b1f7a8b':'drip.svg','006d7335a9e60e7026c26eef38042e75':'hero-goldrush.webp','8c1c8b99112ac1b6ad0c2ae228338fba':'hero-tenders.jpg','76bf21981ce160d8feb56cb0b8057378':'hero-pour2.jpg','106212bff82814d41f0d314be9388ee5':'blandville.webp','e84d1c5788028edbcdb97a8ea55f0fce':'meal-prep.jpg','11babe328185d52cb16fbce1f5b3cf6d':'meal-prep-home.jpg','9ee8f0ed693c32d369423f3bbab86a1b':'bowl.jpg','0e1539c8d508baeec3a23bb958cb8d4f':'hero.jpg','1dbdec8d80fc32b67225a04cb44a7cd8':'bottle.png','bd1337159890a5de5c304efec1cd41a0':'gary-wing.png','a79d682b85e5bcafdf98d4e4da716d02':'gary.webp','77bc7350430c66f8674bc09d02ed5fcc':'ranch-shadow.jpg'}
PAGES={'Main.dc.html':('index.html','Toon Sauce | Your favorite sauce, now with 70g of protein','Restaurant-style chicken sauce made with real honey. 7g protein per serving, 70g per bottle. Join the list for launch-day access.'),
       'Privacy.dc.html':('privacy.html','Privacy Policy | Toon Sauce','How Toon Sauce collects and uses your email address and browsing data, including the Meta Pixel and Conversions API.')}
GA='''<script async src="https://www.googletagmanager.com/gtag/js?id=G-BTGXZ5LCFG"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag('js',new Date());gtag('config','G-BTGXZ5LCFG');</script>'''
for src,(dst,title,desc) in PAGES.items():
    t=open(f'{SRC}/{src}',encoding='utf-8').read()
    helmet=re.search(r'<helmet>(.*?)</helmet>',t,re.S).group(1)
    body=re.search(r'</helmet>(.*?)</x-dc>',t,re.S).group(1)
    html=f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="facebook-domain-verification" content="r4as0ai3v45suzltbwqpyd1kb8acv7" />
{GA}
<!-- Meta Pixel Code -->
<script>
!function(f,b,e,v,n,t,s)
{{if(f.fbq)return;n=f.fbq=function(){{n.callMethod?
n.callMethod.apply(n,arguments):n.queue.push(arguments)}};
if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
n.queue=[];t=b.createElement(e);t.async=!0;
t.src=v;s=b.getElementsByTagName(e)[0];
s.parentNode.insertBefore(t,s)}}(window, document,'script',
'https://connect.facebook.net/en_US/fbevents.js');
fbq('init', '1495416545782879');
fbq('track', 'PageView');
</script>
<noscript><img height="1" width="1" style="display:none"
src="https://www.facebook.com/tr?id=1495416545782879&ev=PageView&noscript=1"
/></noscript>
<!-- End Meta Pixel Code -->
<title>{title}</title>
<meta name="description" content="{desc}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="https://toonsauce.com/assets/hero.jpg">
<meta name="theme-color" content="#141414">
<link rel="icon" href="/assets/favicon.png">
{helmet.strip()}
</head>
<body>
{body.strip()}
<div id="cookie-note" hidden role="region" aria-label="Cookie notice" style="position:fixed;left:16px;right:16px;bottom:16px;z-index:50;max-width:440px;display:flex;align-items:center;gap:14px;padding:12px 12px 12px 18px;border-radius:16px;background:rgba(28,28,28,.96);border:1px solid rgba(246,238,223,.16);color:#F6EEDF;font-family:Fredoka,system-ui,sans-serif;font-size:14px;line-height:1.45;box-shadow:0 16px 40px rgba(0,0,0,.45)"><span>We use cookies and the Meta Pixel to measure our ads. <a href="/privacy" style="color:inherit">Privacy Policy</a></span><button type="button" style="flex:0 0 auto;min-width:64px;min-height:44px;border-radius:999px;border:0;background:#F2A93B;color:#141414;font:600 14px Fredoka,system-ui,sans-serif;cursor:pointer">OK</button></div>
<script>
(function(){{
  var RE=/^[^\s@]+@[^\s@]+\.[^\s@]{{2,}}$/;
  var ANSWERS=['Protein shakes','Meat & eggs','Protein snacks',"I don't really track it"];
  function ck(n){{var m=document.cookie.match('(?:^|; )'+n+'=([^;]*)');return m?decodeURIComponent(m[1]):'';}}
  function fbc(){{var c=ck('_fbc');if(c)return c;var id=new URLSearchParams(location.search).get('fbclid');return id?'fb.1.'+Date.now()+'.'+id:'';}}
  function eid(){{return (window.crypto&&crypto.randomUUID)?crypto.randomUUID():Date.now().toString(36)+'-'+Math.random().toString(36).slice(2);}}
  function post(p){{p.fbp=ck('_fbp');p.fbc=fbc();p.url=location.href;
    return fetch('/api/lead',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify(p),keepalive:true}});}}
  function esc(s){{return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/"/g,'&quot;');}}
  function fail(box,input,btn,msg){{var e=box.querySelector('.err');e.textContent=msg;e.hidden=false;input.setAttribute('aria-invalid','true');if(btn){{btn.disabled=false;btn.textContent='Get first dibs';}}input.focus();}}

  document.addEventListener('submit',function(ev){{
    var form=ev.target; if(!form.classList||!form.classList.contains('ef'))return;
    ev.preventDefault();
    var box=form.closest('.signup'),input=form.querySelector('input[type=email]'),btn=form.querySelector('button');
    var email=(input.value||'').trim().toLowerCase();
    if(!RE.test(email)){{fail(box,input,null,'Please enter a valid email address.');return;}}
    box.querySelector('.err').hidden=true;input.removeAttribute('aria-invalid');
    btn.disabled=true;btn.textContent='Saving…';
    var id=eid(),source=box.getAttribute('data-source')||'hero';
    post({{event_name:'Lead',event_id:id,email:email,source:source}})
      .then(function(r){{if(!r.ok)throw r;return r.json();}})
      .then(function(){{
        if(typeof fbq==='function')fbq('track','Lead',{{content_name:'launch_list',signup_source:source}},{{eventID:id}});
        success(box,email,source);
      }})
      .catch(function(){{fail(box,input,btn,'Something went wrong. Please try again.');}});
  }});

  function success(box,email,source){{
    box.innerHTML='<div class="ok" role="status" tabindex="-1"><p class="okh">You’re on the list. Gary says thanks. He’s not great at saying no.</p>'+
      '<p class="q">How do you usually get your protein?</p><div class="qs">'+
      ANSWERS.map(function(a){{return '<button type="button" data-a="'+esc(a)+'">'+esc(a)+'</button>';}}).join('')+'</div></div>';
    var ok=box.querySelector('.ok');ok.focus({{preventScroll:true}});
    box.querySelectorAll('.qs button').forEach(function(b){{b.addEventListener('click',function(){{
      var a=b.getAttribute('data-a'),id=eid();
      if(typeof fbq==='function')fbq('trackCustom','QualifiedLead',{{protein_source:a}},{{eventID:id}});
      post({{event_name:'QualifiedLead',event_id:id,email:email,source:source,protein_source:a}}).catch(function(){{}});
      ok.innerHTML='<p class="okh">You’re on the list. Gary says thanks. He’s not great at saying no.</p><p class="done">Got it. See you on launch day.</p>';
    }});}});
  }}

  function dibs(){{var s=document.getElementById('signup');if(!s)return false;
    s.scrollIntoView({{behavior:'smooth',block:'center'}});var i=s.querySelector('input[type=email]');
    if(i)setTimeout(function(){{i.focus({{preventScroll:true}});}},400);return true;}}
  document.addEventListener('click',function(ev){{var a=ev.target.closest&&ev.target.closest('a.js-dibs');
    if(a&&document.getElementById('signup')){{ev.preventDefault();dibs();}}}});
  if(location.hash==='#signup')window.addEventListener('load',dibs);

  var cn=document.getElementById('cookie-note');
  try{{if(cn&&!localStorage.getItem('ts_cookie_ok'))cn.hidden=false;}}catch(e){{if(cn)cn.hidden=false;}}
  if(cn)cn.querySelector('button').addEventListener('click',function(){{cn.hidden=true;try{{localStorage.setItem('ts_cookie_ok','1');}}catch(e){{}}}});
}})();
</script>
</body>
</html>
'''
    for k,v in BLOBS.items(): html=html.replace(f'/_blob/{k}',f'/assets/{v}')
    html=html.replace('href="Product.dc.html','href="/#coming-soon').replace('href="Cartoons.dc.html','href="/cartoons').replace('href="GoldRush.dc.html','href="/gold-rush').replace('href="Blandville.dc.html','href="/blandville').replace('href="Privacy.dc.html','href="/privacy').replace('href="Main.dc.html','href="/')
    if '/_blob/' in html or '.dc.html' in html: sys.exit(f'unmapped ref in {dst}')
    open(f'{OUT}/{dst}','w',encoding='utf-8').write(html)
    print('wrote',dst,len(html))
