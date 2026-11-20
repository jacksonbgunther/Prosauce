(function(){
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
