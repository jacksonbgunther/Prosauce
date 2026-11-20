import sys
P = sys.argv[1]
B = lambda i: '/_blob/' + i
LOGO = B('0dd5d257bfb9b2f73f03415c58960666')
HERO = '/assets/hero-pour-cream-soft.jpg'   # hero photo on cream; use a NEW filename when swapping (browsers cache assets for 4h)
BOTTLE = '/assets/bottle-clean.png'   # bottle cutout with cleaned edges (original: assets/bottle.png)
WING = B('bd1337159890a5de5c304efec1cd41a0')     # assets/gary-wing.png

# ---- fill these in -------------------------------------------------------
LAUNCH = 'soon'        # e.g. 'in March'  -> "Launching in March"
CALORIES = '120'       # from the current Gold Rush nutrition label
CONTACT = ''           # e.g. 'hello@toonsauce.com'
# --------------------------------------------------------------------------

CSS = r'''
:root{--bg:#141414;--bg2:#1c1c1c;--cream:#F6EEDF;--amber:#F2A93B;--ink:#141414;--line:rgba(246,238,223,.16)}
*{box-sizing:border-box}
body{margin:0;background:var(--bg)}
a{color:inherit}
img{max-width:100%}
.wrap{max-width:1440px;margin:0 auto;padding-left:clamp(20px,4.6vw,70px);padding-right:clamp(20px,4.6vw,70px)}
.d{font-family:'Lilita One',system-ui,sans-serif;font-weight:400;letter-spacing:.005em;line-height:1.06;margin:0}
.dk .d{color:var(--cream);text-shadow:0 2px 0 rgba(90,40,8,.35),0 10px 34px rgba(0,0,0,.45)}
.h2{font-size:clamp(34px,3.8vw,56px)}
.amb{color:var(--amber)}
.sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}
:focus-visible{outline:3px solid var(--amber);outline-offset:3px}
.pill{display:inline-flex;align-items:center;justify-content:center;gap:10px;min-height:52px;padding:0 26px;border-radius:999px;background:var(--amber);color:var(--ink);text-decoration:none;font-family:'Fredoka',system-ui,sans-serif;font-weight:600;font-size:16.5px;border:0;cursor:pointer;white-space:nowrap;transition:transform .2s ease,background .2s ease}
.pill:hover{transform:translateY(-1px);background:#ffbb55}
.pill-cream{background:var(--cream)}.pill-cream:hover{background:#fff7ea}
.ann{background:var(--amber);color:var(--ink);text-align:center;padding:10px 16px;font-size:14.5px;font-weight:600}
.hdr{background:var(--bg);border-bottom:1px solid var(--line);position:sticky;top:0;z-index:20}
.hdr .in{display:flex;align-items:center;justify-content:space-between;gap:20px;height:72px}
.hdr nav{display:flex;gap:6px;font-size:16.5px}
.hdr nav a{text-decoration:none;color:var(--cream);opacity:.92;padding:12px 12px;border-radius:999px}
.hdr nav a:hover{opacity:1;background:rgba(246,238,223,.08)}
.hdr .pill{min-height:44px;padding:0 20px;font-size:15px}
@media (max-width:640px){.hdr nav{display:none}}
/* hero */
.hero{position:relative;background:var(--cream)}
.hero .bgw{position:absolute;inset:0;overflow:hidden}
.hero .bgimg{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:62% 72%}
.hero .shade{position:absolute;inset:0}
@media (min-width:861px){.hero .bgimg{object-position:100% 50%}}
.hero .sub,.hero .spec{text-shadow:0 0 3px rgba(246,238,223,1),0 0 10px rgba(246,238,223,.95),0 0 22px rgba(246,238,223,.9)}
@media (min-width:861px){.hero .micro{display:inline-block;margin-top:12px;padding:6px 14px;border-radius:999px;background:rgba(246,238,223,.92);color:#2E2822}}
@media (max-width:860px){.hero .bgw{bottom:auto;height:440px}.hero .shade{display:none}.hero .bgimg{object-position:62% 50%}.hero .in{padding-top:20px!important;padding-bottom:48px!important;gap:28px!important}.hero .stage{order:-1;min-height:420px}}
.hero .in{position:relative;z-index:1;display:grid;grid-template-columns:minmax(0,1.3fr) minmax(0,.7fr);align-items:center;gap:24px;min-height:clamp(640px,86vh,820px);padding-top:56px;padding-bottom:56px}
.hero .copy{display:flex;flex-direction:column;align-items:flex-start;gap:20px}
.hero h1,.dk .hero h1{font-size:clamp(38px,4.1vw,64px);color:var(--ink);text-shadow:none}
.hero h1 .ln{white-space:nowrap}@media (max-width:860px){.hero h1 .ln{white-space:normal}}
.hero .sub{margin:0;font-size:19px;line-height:1.5;color:#2E2822;max-width:36ch}
.hero .spec{color:rgba(20,20,20,.72)}
.hero .ef input{background:rgba(255,251,243,.92);border-color:rgba(20,20,20,.22);color:var(--ink)}
.hero .ef input::placeholder{color:rgba(20,20,20,.5)}
.hero .err{color:#B3261E}
.hero .micro{color:#5B5348}
.hero .ok .okh,.hero .ok .q{color:var(--ink)}
.hero .qs button{background:rgba(255,251,243,.92);border-color:rgba(20,20,20,.2);color:var(--ink)}
.hero .qs button:hover{background:rgba(242,169,59,.2)}
.hero .ok .done{color:#8A5300}
.stage{position:relative;align-self:stretch;min-height:520px}
.bw{position:absolute;left:50%;bottom:0;height:min(94%,640px);transform:translateX(-50%)}
.bw .bottle{display:block;height:100%;width:auto;max-width:none;filter:drop-shadow(0 30px 36px rgba(60,32,8,.38)) drop-shadow(0 6px 10px rgba(20,20,20,.3))}
.stats{position:absolute;right:calc(100% - 70px);bottom:8%;display:flex;flex-direction:row-reverse;align-items:center;gap:10px;z-index:2}
.stk{--s:clamp(132px,11vw,160px);flex:0 0 auto;position:relative;width:var(--s);height:var(--s);border-radius:50%;background:radial-gradient(circle at 35% 30%,#2A2433 0%,#15121C 70%);border:calc(var(--s)*.035) solid #F7832B;box-shadow:0 0 0 calc(var(--s)*.025) #15121C,0 0 0 calc(var(--s)*.055) #FFC23D,0 20px 50px rgba(0,0,0,.55);display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;line-height:1;transform:rotate(-10deg)}
.stk b{font-family:'Shrikhand',Georgia,serif;font-weight:400;font-size:calc(var(--s)*.34);color:#FFF8EE;text-shadow:calc(var(--s)*.018) calc(var(--s)*.018) 0 #D9401F}
.stk span{font-family:'Fredoka',system-ui,sans-serif;font-weight:700;font-size:calc(var(--s)*.078);letter-spacing:.1em;text-transform:uppercase;color:#FFC23D;margin-top:calc(var(--s)*.04);max-width:72%;line-height:1.15}
.stk i{font-style:normal;font-family:'Fredoka',system-ui,sans-serif;font-weight:500;font-size:calc(var(--s)*.075);color:#F6EEDF;margin-top:calc(var(--s)*.04)}
.spec{margin:-4px 0 4px;display:flex;flex-wrap:wrap;align-items:center;gap:6px 0;font-size:14.5px;font-weight:500;color:rgba(246,238,223,.82)}
.spec span+span:before{content:"";display:inline-block;width:5px;height:5px;border-radius:50%;background:var(--amber);margin:0 12px 2px;vertical-align:middle}
.cal{display:inline-flex;align-items:center;min-height:40px;padding:8px 16px;border-radius:999px;background:rgba(20,20,20,.88);border:1px solid rgba(242,169,59,.7);color:var(--cream);font-size:14.5px;font-weight:500;white-space:nowrap;box-shadow:0 10px 24px rgba(0,0,0,.4)}
/* form */
.signup{width:100%;max-width:540px}
.ef{display:flex;gap:8px;width:100%}
.ef input{flex:1;min-width:0;height:52px;border-radius:999px;border:1px solid rgba(246,238,223,.4);background:rgba(20,20,20,.6);color:var(--cream);padding:0 22px;font:inherit;font-size:16.5px;outline:none;transition:border-color .2s ease}
.ef input::placeholder{color:rgba(246,238,223,.6)}
.ef input:focus{border-color:var(--amber);box-shadow:0 0 0 3px rgba(242,169,59,.25)}
.ef input[aria-invalid=true]{border-color:#FF8A65}
.ef .pill{min-height:52px}
.ef button[disabled]{opacity:.7;cursor:progress}
.err{margin:10px 4px 0;color:#FFB08F;font-size:14.5px}
.micro{margin:12px 4px 0;font-size:13.5px;line-height:1.5;color:rgba(246,238,223,.7)}
.micro a{color:inherit}
.ok{display:flex;flex-direction:column;gap:14px}
.ok .okh{margin:0;font-family:'Lilita One',system-ui,sans-serif;font-size:clamp(22px,2vw,28px);line-height:1.2;color:var(--cream)}
.ok .q{margin:4px 0 0;font-size:17px;color:var(--cream)}
.qs{display:grid;grid-template-columns:1fr 1fr;gap:8px}
.qs button{min-height:48px;padding:10px 14px;border-radius:14px;border:1px solid rgba(246,238,223,.35);background:rgba(20,20,20,.6);color:var(--cream);font:inherit;font-size:15.5px;cursor:pointer;text-align:left;transition:background .15s ease,border-color .15s ease}
.qs button:hover{border-color:var(--amber);background:rgba(242,169,59,.12)}
.ok .done{margin:0;font-size:17px;color:var(--amber);font-weight:600}
@media (max-width:560px){.ef{flex-direction:column}.ef input{flex:0 0 auto;width:100%}.ef .pill{width:100%}.qs{grid-template-columns:1fr}}
/* strip */
.mq{overflow:hidden;background:var(--ink);color:var(--cream);white-space:nowrap;position:relative;z-index:2}
.mq .t{display:inline-flex;padding:13px 0;animation:mq 46s linear infinite;font-size:15px;font-weight:500}
.mq .t span{padding:0 18px}.mq .t span:before{content:"\2022";margin-right:18px;color:var(--amber)}
@keyframes mq{from{transform:translateX(0)}to{transform:translateX(-50%)}}
@media (prefers-reduced-motion:reduce){.mq .t{animation:none}}
/* sections */
.sec{padding-top:clamp(72px,8vw,120px);padding-bottom:clamp(72px,8vw,120px)}
.cr{background:var(--cream);color:var(--ink)}
.cr .d,.dk .cr .d{color:var(--ink);text-shadow:none}
.mark{white-space:nowrap;background:linear-gradient(180deg,transparent 58%,rgba(242,169,59,.75) 58%,rgba(242,169,59,.75) 92%,transparent 92%);padding:0 .06em}
.cmp{display:grid;grid-template-columns:1fr 1fr;gap:clamp(14px,2vw,28px);max-width:1240px;margin:clamp(32px,4vw,52px) auto 0}
.cg{display:flex;align-items:center;gap:clamp(12px,1.6vw,22px)}
.cg .cc{flex:1;min-width:0}
.cb{flex:0 0 auto;height:clamp(170px,16vw,240px);width:auto;max-width:none}
.cb.ours{filter:drop-shadow(0 18px 22px rgba(60,32,8,.3))}
.cb.theirs{height:clamp(140px,13vw,196px);opacity:.9}
@media (max-width:760px){.cmp{grid-template-columns:1fr}.cb{height:130px}.cb.theirs{height:100px}.cc .big{font-size:44px}}
.cc{border-radius:20px;padding:clamp(26px,3vw,40px);display:flex;flex-direction:column;gap:12px;min-height:clamp(0px,18vw,250px)}
.cc .lb{font-size:16px;font-weight:600;letter-spacing:.02em}
.cc .big{font-family:'Lilita One',system-ui,sans-serif;font-size:clamp(52px,6vw,84px);line-height:1}
.cc p{margin:0;font-size:18px;line-height:1.45}
.cc.muted{background:#E3DACA;color:#6E665B}
.cc.muted .big{color:#8E8679}
.cc.hero2{background:var(--ink);color:var(--cream);box-shadow:inset 0 0 0 2px var(--amber),0 24px 50px rgba(20,20,20,.25)}
.cc.hero2 .lb{color:var(--amber)}
.cc.hero2 .big{color:var(--amber)}
.note{text-align:center;margin:18px 0 0;font-size:14.5px;color:#6E665B}
/* blandville */
.bvh{max-width:760px;margin:0 auto;text-align:center;display:flex;flex-direction:column;align-items:center;gap:18px}
.bvh p{margin:0;font-size:19px;line-height:1.55;color:#3D362E;max-width:52ch}
.vid{position:relative;max-width:1040px;margin:clamp(32px,4vw,52px) auto 0;aspect-ratio:16/9;border-radius:20px;overflow:hidden;background:var(--ink);box-shadow:0 0 0 2px var(--ink),0 28px 60px rgba(20,20,20,.25)}
.vid img{display:block;width:100%;height:100%;object-fit:cover}
.vtag{position:absolute;left:16px;bottom:16px;padding:9px 16px;border-radius:999px;background:rgba(20,20,20,.88);color:var(--cream);font-size:14.5px;font-weight:600}
.gary{position:relative;overflow:hidden;background:var(--bg)}
.gary .in{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);align-items:center;gap:24px;min-height:clamp(320px,30vw,420px)}
.gary .tx{display:flex;flex-direction:column;align-items:flex-start;gap:20px;position:relative;z-index:1}
.gary .tx p{margin:0;font-size:19px;line-height:1.55;color:var(--cream);max-width:36ch}
.gary .wing{position:absolute;right:-2%;top:50%;transform:translateY(-50%) rotate(-6deg);width:min(58vw,820px);filter:drop-shadow(0 0 1.5px rgba(242,169,59,.7)) drop-shadow(0 24px 40px rgba(0,0,0,.6))}
@media (max-width:860px){.gary .in{grid-template-columns:1fr;padding-bottom:260px}.gary .wing{top:auto;bottom:24px;transform:rotate(-6deg);width:118vw;right:-30vw}}
.faqg{display:grid;grid-template-columns:1fr 1.4fr;gap:clamp(28px,5vw,80px);align-items:start}
@media (max-width:860px){.faqg{grid-template-columns:1fr}}
.faq details{border-bottom:1px solid rgba(20,20,20,.16)}
.faq details:first-child{border-top:1px solid rgba(20,20,20,.16)}
.faq summary{list-style:none;cursor:pointer;display:flex;justify-content:space-between;align-items:center;gap:20px;min-height:64px;padding:16px 0;font-size:19.5px;font-weight:600;color:var(--ink)}
.faq summary::-webkit-details-marker{display:none}
.faq summary:after{content:"+";font-size:26px;font-weight:500;color:#b8740f;transition:transform .2s ease}
.faq details[open] summary:after{transform:rotate(45deg)}
.faq p{margin:0 0 22px;font-size:17px;line-height:1.6;color:#3D362E;max-width:60ch}
/* gold rush product */
.prod{background:var(--bg)}
.pdp{display:grid;grid-template-columns:minmax(0,1.15fr) minmax(0,1fr);gap:clamp(28px,4vw,64px);align-items:start}
@media (max-width:900px){.pdp{grid-template-columns:1fr}}
.gal{display:flex;flex-direction:column;gap:10px}
.gal .main{position:relative;border-radius:8px;overflow:hidden;aspect-ratio:1/1;background:radial-gradient(70% 70% at 50% 58%,#a85a17 0%,#4a230a 45%,#120803 100%)}
.gal .sl{display:none;position:absolute;inset:0}
.gal .sl>img{display:block;width:100%;height:100%;object-fit:cover}
.gal .sl.s0>img{object-fit:contain;padding:6% 0 3%;transform:rotate(7deg);filter:drop-shadow(0 30px 40px rgba(0,0,0,.6))}
.gal .cap{position:absolute;left:0;right:0;bottom:0;padding:70px 26px 22px;background:linear-gradient(180deg,rgba(0,0,0,0) 0%,rgba(0,0,0,.72) 100%);font-family:'Lilita One',system-ui,sans-serif;font-size:clamp(28px,3vw,42px);color:var(--cream);text-shadow:0 2px 0 rgba(90,40,8,.5)}
.thumbs{display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:8px}
.thumbs label{cursor:pointer;aspect-ratio:1;border-radius:6px;overflow:hidden;background:#1c1c1c;display:block;line-height:0;min-height:44px}
.thumbs label img{width:100%;height:100%;object-fit:cover;opacity:.55;transition:opacity .2s ease}
.thumbs label:hover img{opacity:1}
@media (max-width:560px){.thumbs{grid-template-columns:repeat(3,minmax(0,1fr))}}
#g0:checked~.main .s0{display:block}#g0:checked~.thumbs label[for=g0]{outline:2px solid var(--amber);outline-offset:2px}#g0:checked~.thumbs label[for=g0] img{opacity:1}#g0:focus-visible~.thumbs label[for=g0]{outline:3px solid var(--amber);outline-offset:3px}#g1:checked~.main .s1{display:block}#g1:checked~.thumbs label[for=g1]{outline:2px solid var(--amber);outline-offset:2px}#g1:checked~.thumbs label[for=g1] img{opacity:1}#g1:focus-visible~.thumbs label[for=g1]{outline:3px solid var(--amber);outline-offset:3px}#g2:checked~.main .s2{display:block}#g2:checked~.thumbs label[for=g2]{outline:2px solid var(--amber);outline-offset:2px}#g2:checked~.thumbs label[for=g2] img{opacity:1}#g2:focus-visible~.thumbs label[for=g2]{outline:3px solid var(--amber);outline-offset:3px}#g3:checked~.main .s3{display:block}#g3:checked~.thumbs label[for=g3]{outline:2px solid var(--amber);outline-offset:2px}#g3:checked~.thumbs label[for=g3] img{opacity:1}#g3:focus-visible~.thumbs label[for=g3]{outline:3px solid var(--amber);outline-offset:3px}#g4:checked~.main .s4{display:block}#g4:checked~.thumbs label[for=g4]{outline:2px solid var(--amber);outline-offset:2px}#g4:checked~.thumbs label[for=g4] img{opacity:1}#g4:focus-visible~.thumbs label[for=g4]{outline:3px solid var(--amber);outline-offset:3px}#g5:checked~.main .s5{display:block}#g5:checked~.thumbs label[for=g5]{outline:2px solid var(--amber);outline-offset:2px}#g5:checked~.thumbs label[for=g5] img{opacity:1}#g5:focus-visible~.thumbs label[for=g5]{outline:3px solid var(--amber);outline-offset:3px}
.info{display:flex;flex-direction:column;gap:18px;align-items:flex-start;position:sticky;top:96px}
@media (max-width:900px){.info{position:static}}
.info .eb{font-size:15px;font-weight:600;color:var(--amber)}
.info p.ds{margin:0;font-size:18px;line-height:1.55;color:rgba(246,238,223,.88);max-width:44ch}
.specs{width:100%;display:grid;grid-template-columns:repeat(3,1fr);border-top:1px solid var(--line);border-bottom:1px solid var(--line)}
.specs div{padding:16px 6px;text-align:center;border-left:1px solid var(--line)}.specs div:first-child{border-left:0}
.specs b{display:block;font-family:'Lilita One',system-ui,sans-serif;font-weight:400;font-size:30px;line-height:1;color:var(--cream)}
.specs span{font-size:13.5px;color:rgba(246,238,223,.65)}
.drop{width:100%;background:#1c1c1c;border-radius:10px;padding:22px;display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:14px}
.drop p{margin:0;font-size:17px;color:var(--cream)}
/* cool ranch teaser */
.cs{position:relative;overflow:hidden;min-height:clamp(560px,52vw,720px);background:#000}
.cs .shot{position:absolute;left:calc(50% - 160px);top:0;height:100%;width:auto;max-width:none;filter:brightness(.5) contrast(1.15);-webkit-mask-image:linear-gradient(90deg,transparent 0%,#000 55%),linear-gradient(0deg,transparent 0%,#000 18%);-webkit-mask-composite:source-in;mask-image:linear-gradient(90deg,transparent 0%,#000 55%),linear-gradient(0deg,transparent 0%,#000 18%);mask-composite:intersect}
.cs:after{content:"";position:absolute;inset:0;background:linear-gradient(90deg,#000 0%,rgba(0,0,0,.4) 40%,rgba(0,0,0,0) 60%);pointer-events:none}
.cs .tx{position:relative;z-index:2;min-height:inherit;display:flex;flex-direction:column;justify-content:center;align-items:flex-start;gap:20px}
.cs .tx .k{font-size:15px;font-weight:600;color:#5FD3D1}
.cs .tx p{margin:0;font-size:18px;line-height:1.55;color:#bdbdbd;max-width:36ch}
.cs .flg{width:min(80%,340px);filter:brightness(.55) saturate(.8) drop-shadow(0 0 18px rgba(95,211,209,.25))}
.pill-ghost{background:transparent;color:var(--cream);box-shadow:inset 0 0 0 1px rgba(246,238,223,.55)}.pill-ghost:hover{background:rgba(246,238,223,.08)}
@media (max-width:860px){.cs{min-height:900px}.cs .tx{justify-content:flex-start;padding-top:56px;min-height:0}.cs .shot{left:auto;top:auto;bottom:0;height:62%;right:-8%;-webkit-mask-image:linear-gradient(180deg,transparent 0%,#000 30%);mask-image:linear-gradient(180deg,transparent 0%,#000 30%)}.cs:after{background:linear-gradient(180deg,#000 0%,#000 42%,rgba(0,0,0,0) 62%)}}
/* new flavors signup */
.nf{padding-top:clamp(56px,6vw,96px);padding-bottom:clamp(56px,6vw,96px);background:var(--bg)}
.join{border-radius:12px;background:var(--cream);color:var(--ink);display:grid;grid-template-columns:1.2fr 1fr;align-items:center;overflow:hidden}
@media (max-width:860px){.join{grid-template-columns:1fr}}
.join .tx{padding:clamp(32px,5vw,72px);display:flex;flex-direction:column;gap:18px;align-items:flex-start}
.join .d{color:var(--ink);text-shadow:none}
.join .tx>p{margin:0;font-size:18px;line-height:1.5;color:#3D362E;max-width:40ch}
.join .vs{align-self:stretch;display:flex;align-items:flex-end;justify-content:center;min-height:300px}
.join .vs img{width:min(52%,280px);margin-bottom:-2px}
@media (max-width:860px){.join .vs{min-height:0;height:280px;overflow:hidden}.join .vs img{width:150px}}
.join .ef input{background:#fff9ef;color:var(--ink);border-color:rgba(20,20,20,.25)}
.join .ef input::placeholder{color:rgba(20,20,20,.5)}
.join .micro,.join .err{color:#5b5248}
.join .ok .okh,.join .ok .q{color:var(--ink)}
.join .qs button{background:#fff9ef;color:var(--ink);border-color:rgba(20,20,20,.2)}
.join .ok .done{color:#a8650c}
/* footer */
.ft{background:var(--bg);border-top:1px solid var(--line);color:var(--cream)}
.ft .cols{display:grid;grid-template-columns:1fr 1.2fr;gap:clamp(32px,5vw,80px);align-items:start;padding-top:64px;padding-bottom:40px}
@media (max-width:860px){.ft .cols{grid-template-columns:1fr}}
.soc{display:flex;gap:8px}
.soc a{width:48px;height:48px;border-radius:50%;display:grid;place-items:center;background:rgba(246,238,223,.08);color:var(--cream);transition:background .2s ease}
.soc a:hover{background:rgba(242,169,59,.25)}
.ft .legal{display:flex;flex-wrap:wrap;justify-content:space-between;gap:12px;font-size:14px;color:rgba(246,238,223,.65);padding-bottom:24px}
.ft .legal a{color:inherit;display:inline-block;padding:12px 0}
.wm{font-family:'Lilita One',system-ui,sans-serif;color:#222;font-size:clamp(64px,16.5vw,260px);line-height:.9;white-space:nowrap;text-align:center;overflow:hidden}
/* privacy */
.legaldoc{max-width:760px}
.legaldoc h2{font-family:'Lilita One',system-ui,sans-serif;font-weight:400;font-size:26px;margin:40px 0 10px;color:var(--cream)}
.legaldoc p,.legaldoc li{font-size:17px;line-height:1.65;color:rgba(246,238,223,.88)}
.legaldoc ul{padding-left:22px}
@media (max-width:860px){
 .hero .in{grid-template-columns:1fr;align-items:start;min-height:0;padding-top:32px;padding-bottom:0;gap:8px}
 .hero .shade{background:linear-gradient(180deg,rgba(246,238,223,.96) 0%,rgba(246,238,223,.9) 52%,rgba(246,238,223,.3) 78%,rgba(246,238,223,0) 100%)}
 .stage{min-height:420px}
 .bw{left:60%;height:400px}
 .stats{right:calc(100% - 56px);bottom:6%;flex-direction:column;align-items:flex-end}
 .stk{--s:124px}
}
@media (max-width:560px){.hero h1{font-size:38px}.hero .sub{font-size:17.5px}.hero .copy{gap:16px}}
'''

ANN = '<div class="ann">First batch is limited. Join the list for launch-day access.</div>'


def header(h=''):
    return f'''<header class="hdr"><div class="wrap in">
    <div style="display: flex; align-items: center; gap: clamp(14px, 3vw, 30px)">
      <a href="{h or '#top'}" aria-label="Toon Sauce home" style="display: block; line-height: 0"><img src="{LOGO}" alt="Toon Sauce" style="height: 52px; width: auto"></a>
      <nav aria-label="Main"><a href="{h}#gold-rush">Gold Rush</a><a href="{h}#coming-soon">Coming soon</a></nav>
    </div>
    <a href="{h}#signup" class="pill pill-cream js-dibs">Get first dibs</a>
  </div></header>'''


def signup(source):
    sid = f'em-{source}'
    return f'''<div class="signup" data-source="{source}"{' id="signup"' if source == 'hero' else ''}>
          <form class="ef" novalidate><label class="sr" for="{sid}">Email address</label><input id="{sid}" type="email" name="email" required placeholder="Your email" autocomplete="email" inputmode="email" aria-describedby="{sid}-err"><button type="submit" class="pill">Get first dibs</button></form>
          <p class="err" id="{sid}-err" role="alert" hidden></p>
          <p class="micro">No spam. One email when it drops. By signing up you agree to our <a href="Privacy.dc.html">Privacy Policy</a>.</p>
        </div>'''


IG = '<svg width="22" height="22" viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5" fill="none" stroke="currentColor" stroke-width="2"/><circle cx="12" cy="12" r="4.2" fill="none" stroke="currentColor" stroke-width="2"/><circle cx="17.4" cy="6.6" r="1.3" fill="currentColor"/></svg>'
TT = '<svg width="22" height="22" viewBox="0 0 24 24" aria-hidden="true"><path d="M14 3v11.2a3.6 3.6 0 1 1-3.1-3.6V7.5A6.7 6.7 0 1 0 17.1 14V8.6a7.4 7.4 0 0 0 3.9 1.2V6.7A4.2 4.2 0 0 1 17 3z" fill="currentColor"/></svg>'
YT = '<svg width="24" height="24" viewBox="0 0 24 24" aria-hidden="true"><rect x="2" y="5" width="20" height="14" rx="4" fill="currentColor"/><path d="M10 9l5 3-5 3z" fill="#141414"/></svg>'


def footer(h=''):
    return f'''<footer class="ft">
    <div class="wrap cols">
      <div style="display: flex; flex-direction: column; gap: 18px; align-items: flex-start">
        <a href="{h or '#top'}" aria-label="Toon Sauce home" style="line-height: 0"><img src="{LOGO}" alt="Toon Sauce" style="height: 72px; width: auto"></a>
        <p style="margin: 0; font-size: 16px; color: rgba(246,238,223,.75)">@toonsauce</p>
        <div class="soc">
          <a href="https://www.instagram.com/toonsauce" aria-label="Toon Sauce on Instagram (@toonsauce)" target="_blank" rel="noopener">{IG}</a>
          <a href="https://www.tiktok.com/@toonsauce" aria-label="Toon Sauce on TikTok (@toonsauce)" target="_blank" rel="noopener">{TT}</a>
          <a href="https://www.youtube.com/@toonsauce" aria-label="Toon Sauce on YouTube (@toonsauce)" target="_blank" rel="noopener">{YT}</a>
        </div>
      </div>
      <div style="display: flex; flex-direction: column; gap: 14px">
        <p class="d" style="font-size: clamp(26px, 2.6vw, 36px); color: #F6EEDF">Get first dibs on launch day.</p>
        {signup('footer')}
      </div>
    </div>
    <div class="wrap legal"><span>&#169; 2026 Toon Sauce</span><a href="Privacy.dc.html">Privacy Policy</a></div>
    <div class="wm" aria-hidden="true">Toon Sauce</div>
  </footer>'''


def page(title, body, h, hpref=''):
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{title}</title>
<script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Lilita+One&amp;family=Fredoka:wght@400;500;600;700&amp;family=Shrikhand&amp;display=swap" rel="stylesheet">
<style>
{CSS}</style>
</helmet>

<div class="dk" style="font-family: 'Fredoka', system-ui, sans-serif; color: #F6EEDF; background: #141414; overflow-x: clip">
{body}
  {footer(hpref)}
</div>
</x-dc>
<script type="text/x-dc" data-dc-script data-props='{{"$preview":{{"width":1440,"height":{h}}}}}'>
class Component extends DCLogic {{
  renderVals() {{
    return {{}};
  }}
}}
</script>
</body>
</html>
'''


MQ_ITEMS = ['70g protein per bottle', '7g per serving', 'Made with real honey', 'Tastes like the drive-thru', 'Same dinner, more protein', f'Launching {LAUNCH}']
MQ = '<div class="mq" aria-label="Highlights"><div class="t">' + ''.join(f'<span>{x}</span>' for x in MQ_ITEMS * 6) + '</div></div>'

home = f'''
  {ANN}
  {header()}

  <!-- HERO -->
  <section id="top" class="hero" aria-labelledby="h1">
    <div class="bgw" aria-hidden="true"><img class="bgimg" src="{HERO}" alt="" data-slot="hero-pour-cream-soft.jpg"><div class="shade"></div></div>
    <div class="wrap in">
      <div class="copy">
        <h1 id="h1" class="d"><span class="ln">Your favorite sauce.</span><br><span class="ln">Now with <span class="mark">70g of protein.</span></span></h1>
        <p class="sub">Restaurant-style chicken sauce made with real honey. 7g protein per serving. Same dinner, more protein.</p>
        <p class="spec"><span>7g protein</span><span>{CALORIES} calories</span><span>per serving</span></p>
        {signup('hero')}
      </div>
      <div class="stage">
        <div class="bw">
          <img class="bottle" src="{BOTTLE}" alt="Toon Sauce Gold Rush bottle, matte black with a golden amber cap" data-slot="bottle-clean.png">
          <div class="stats">
            <div class="stk" role="img" aria-label="70 grams of protein per bottle, 7 grams per serving"><b>70g</b><span>Protein per bottle</span><i>7g per serving</i></div>
          </div>
        </div>
      </div>
    </div>
  </section>
  {MQ}

  <!-- SECTION 2: COMPARISON -->
  <section id="compare" class="cr sec" aria-labelledby="cmp-h">
    <div class="wrap">
      <h2 id="cmp-h" class="d h2" style="text-align: center">Sauce just had a <span class="mark">glow-up.</span></h2>
      <div class="cmp">
        <div class="cg"><img class="cb ours" src="/assets/bottle-clean.png" alt="Toon Sauce Gold Rush bottle" loading="lazy"><div class="cc hero2"><span class="lb">Toon Sauce Gold Rush</span><span class="big">7g protein</span><p>Same taste. Actually pulls its weight.</p></div></div>
        <div class="cg"><div class="cc muted"><span class="lb">Regular chicken sauce</span><span class="big">0g protein</span><p>Delicious. Contributes nothing.</p></div><img class="cb theirs" src="/assets/other-sauce.png" alt="A plain bottle of regular chicken sauce" loading="lazy"></div>
      </div>
      <p class="note">Per serving.</p>
    </div>
  </section>

  <!-- GOLD RUSH PRODUCT -->
  <section id="gold-rush" class="prod sec" aria-labelledby="gr-h">
    <div class="wrap pdp">
      <div class="gal"><input type="radio" name="gal" id="g0" class="sr" checked aria-label="Show image 1: Toon Sauce Gold Rush bottle"><input type="radio" name="gal" id="g1" class="sr" aria-label="Show image 2: Meal prep containers of salmon, shrimp and rice with a bowl of golden sauce"><input type="radio" name="gal" id="g2" class="sr" aria-label="Show image 3: Rice bowl with seasoned ground beef, charred corn and pico de gallo"><input type="radio" name="gal" id="g3" class="sr" aria-label="Show image 4: Homemade meal prep containers with chicken, pasta, broccoli and carrots"><input type="radio" name="gal" id="g4" class="sr" aria-label="Show image 5: Crispy chicken tenders splashed with golden sauce"><input type="radio" name="gal" id="g5" class="sr" aria-label="Show image 6: Golden sauce pouring over fried chicken"><div class="main"><div class="sl s0"><img src="/assets/bottle-clean.png" alt="Toon Sauce Gold Rush bottle"></div><div class="sl s1"><img src="/assets/meal-prep.jpg" alt="Meal prep containers of salmon, shrimp and rice with a bowl of golden sauce" loading="lazy"><span class="cap">Made for meal prep.</span></div><div class="sl s2"><img src="/assets/bowl.jpg" alt="Rice bowl with seasoned ground beef, charred corn and pico de gallo" loading="lazy"><span class="cap">Built for bowls.</span></div><div class="sl s3"><img src="/assets/meal-prep-home.jpg" alt="Homemade meal prep containers with chicken, pasta, broccoli and carrots" loading="lazy"><span class="cap">Upgrade boring meals.</span></div><div class="sl s4"><img src="/assets/hero-tenders.jpg" alt="Crispy chicken tenders splashed with golden sauce" loading="lazy"><span class="cap">Made for tenders.</span></div><div class="sl s5"><img src="/assets/hero-pour2.jpg" alt="Golden sauce pouring over fried chicken" loading="lazy"><span class="cap">Made for everything.</span></div></div><div class="thumbs"><label for="g0"><img src="/assets/bottle-clean.png" alt="" loading="lazy" style="object-fit: contain; padding: 6px"></label><label for="g1"><img src="/assets/meal-prep.jpg" alt="" loading="lazy" style=""></label><label for="g2"><img src="/assets/bowl.jpg" alt="" loading="lazy" style=""></label><label for="g3"><img src="/assets/meal-prep-home.jpg" alt="" loading="lazy" style=""></label><label for="g4"><img src="/assets/hero-tenders.jpg" alt="" loading="lazy" style=""></label><label for="g5"><img src="/assets/hero-pour2.jpg" alt="" loading="lazy" style=""></label></div></div>
      <div class="info">
        <span class="eb">Sweet &amp; smoky</span>
        <h2 id="gr-h" style="margin: 0; line-height: 0"><img src="/assets/flav-gold.webp" alt="Gold Rush" style="width: min(100%, 440px); height: auto"></h2>
        <p class="ds">Restaurant-style chicken sauce made with real honey. Sweet, smoky and golden. Your favorite sauce, now with protein.</p>
        <div class="specs"><div><b>70g</b><span>protein / bottle</span></div><div><b>7g</b><span>protein / serving</span></div><div><b>Real</b><span>honey</span></div></div>
        <div class="drop"><p>Gold Rush drops first.</p><a href="#signup" class="pill js-dibs">Get first dibs</a></div>
      </div>
    </div>
  </section>

  <!-- SECTION 3b: BLANDVILLE TEASER -->
  <section id="blandville" class="cr sec" aria-labelledby="bv-h">
    <div class="wrap">
      <div class="bvh">
        <h2 id="bv-h" class="d h2">Something&#8217;s coming out of <span class="mark">Blandville.</span></h2>
        <p>A perfectly normal town where nothing happens. Gary lives there with his roommate Plain, a boiled chicken breast who has never been excited about anything. That&#8217;s about to change.</p>
      </div>
      <!-- VIDEO PLACEHOLDER: swap this block for the "Welcome to Blandville" embed (16:9) when it's produced -->
      <div class="vid" data-slot="blandville-video">
        <img src="/assets/blandville.webp" alt="The town of Blandville, illustrated" loading="lazy">
        <span class="vtag">Episode 1 &#183; Coming soon</span>
      </div>
    </div>
  </section>

  <!-- COOL RANCH COMING SOON -->
  <section id="coming-soon" class="cs" aria-labelledby="cs-h">
    <img class="shot" src="/assets/ranch-shadow.jpg" alt="" aria-hidden="true" loading="lazy">
    <div class="wrap tx">
      <span class="k">Coming soon</span>
      <h2 id="cs-h" class="d h2">Something cool<br>is coming.</h2>
      <img class="flg" src="/assets/flav-ranch.webp" alt="Cool Ranch">
      <p>Creamy, herby and chill. The next flavor is already in the shadows.</p>
      <a href="#new-flavors" class="pill pill-ghost">Get notified first</a>
    </div>
  </section>

  <!-- NEW FLAVORS SIGNUP -->
  <section id="new-flavors" class="nf" aria-labelledby="nf-h">
    <div class="wrap"><div class="join">
      <div class="tx">
        <h2 id="nf-h" class="d h2">Be the first to try our new flavors.</h2>
        <p>Join the list and we&#8217;ll let you know the moment a new flavor drops.</p>
        {signup('flavors')}
      </div>
      <div class="vs" aria-hidden="true"><img src="/assets/gary.webp" alt="" loading="lazy"></div>
    </div></div>
  </section>

  <!-- SECTION 4: FAQ -->
  <section id="faq" class="cr sec" aria-labelledby="f-h">
    <div class="wrap faqg">
      <h2 id="f-h" class="d h2">Questions, answered.</h2>
      <div class="faq">
        <details open><summary>What does it taste like?</summary><p>A sweet, tangy, smoky restaurant-style chicken sauce made with real honey. If you&#8217;ve had the drive-thru version, you know.</p></details>
        <details><summary>How much protein is in it?</summary><p>7g per serving and about 70g per bottle.</p></details>
        <details><summary>When can I buy it?</summary><p>We&#8217;re launching {LAUNCH}. Join the list and you&#8217;ll hear first.</p></details>
        <details><summary>What do I put it on?</summary><p>Chicken, obviously. Also fries, wraps, burgers, bowls, eggs. Whatever you already eat.</p></details>
      </div>
    </div>
  </section>
'''

contact = (f'email us at <a href="mailto:{CONTACT}">{CONTACT}</a>' if CONTACT else 'message us on Instagram at <a href="https://www.instagram.com/toonsauce">@toonsauce</a>')
privacy = f'''
  {ANN}
  {header('Main.dc.html')}
  <main class="wrap sec">
    <div class="legaldoc">
      <h1 class="d h2">Privacy Policy</h1>
      <p style="color: rgba(246,238,223,.6)">Last updated: November 2026</p>
      <p>Toon Sauce (&#8220;we,&#8221; &#8220;us&#8221;) runs toonsauce.com. This page explains what we collect and how we use it.</p>
      <h2>What we collect</h2>
      <ul>
        <li><strong>Your email address</strong>, when you join our launch list, plus where you signed up (for example, the top or bottom of the page).</li>
        <li><strong>Your answer to our optional question</strong> about how you usually get your protein, if you choose to answer.</li>
        <li><strong>Browsing information</strong> collected through cookies and similar technologies, such as pages viewed, your IP address, browser and device type, and Meta cookie identifiers.</li>
      </ul>
      <h2>How we use it</h2>
      <p>We use your email address to send you launch updates and occasional news about Toon Sauce. You can unsubscribe at any time using the link in any email. We use browsing information to understand how the site is used and to measure and improve our advertising.</p>
      <h2>Meta Pixel and Conversions API</h2>
      <p>We use the Meta Pixel and the Meta Conversions API to measure and improve our ads on Facebook and Instagram. This means we share information with Meta Platforms, Inc., including a hashed (SHA-256 encrypted) version of your email address, your IP address, browser user agent, Meta cookie identifiers, and browsing events such as page views and sign-ups. Meta may use this information as described in its own privacy policy. You can manage how Meta uses this information in your Facebook or Instagram ad settings, and you can block or delete cookies in your browser settings.</p>
      <h2>Who else sees your data</h2>
      <p>We use an email service provider to store our list and send emails. We don&#8217;t sell your email address.</p>
      <h2>Contact</h2>
      <p>Questions about this policy or your data? {contact}.</p>
    </div>
  </main>
'''

open(P + '/Main.dc.html', 'w').write(page('Toon Sauce', home, 3900))
open(P + '/Privacy.dc.html', 'w').write(page('Toon Sauce — Privacy Policy', privacy, 2100, 'Main.dc.html'))
print('ok')
