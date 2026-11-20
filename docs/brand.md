Toon Sauce — Website Brief for Claude Code

Context pack for building the Toon Sauce pre-launch site. Compiled Nov 19, 2026 from the project's brand bible, brand decisions log and cartoon scripts. Where sources conflict, the newest decision wins and is the one written here. Items marked OPEN are not decided; don't invent answers, leave a clearly marked placeholder.

1. What the site is (and isn't)
Purpose: pre-launch landing page that collects waitlist emails. This is Stage 2 of the launch plan; the pass bar is 500+ signups.
Only CTA: waitlist email capture. No shop button, no cart, no prices, no reviews/testimonials (product isn't on sale yet; fake reviews are off-limits).
Tracking: Meta Pixel is already installed. Add Meta Conversions API (server-side) and fire:
Lead — on successful waitlist signup.
QualifiedLead — OPEN: qualifying criteria not defined yet. Build the hook (e.g. fires when an optional follow-up question is answered, such as "Do you track protein?") and leave the rule configurable.
Deduplicate Pixel and CAPI events with a shared event_id. Hash email (SHA-256) before sending to CAPI.
Audience: adults 18–40 who track protein/macros but refuse to eat sad food. Men and women equally. Mainstream food brand, not a bodybuilding supplement brand.
2. Brand core
Name: Toon Sauce
Tagline: Add protein without changing your meals.
Big idea: Sauces with personalities. Macros with receipts.
Concept: every flavor is a cartoon character (a "Toon"). The characters make it fun; the food and the macros make people buy again. Each new flavor debuts with its own cartoon episode and joins the shared world (the "Tooniverse").
Pillars: (1) Tastes like the real thing. (2) Macros you can brag about. (3) Characters worth collecting. (4) Fun for grown-ups.
3. The product (launch SKU)
What it is: a restaurant-style chicken sauce (honey mustard + BBQ + mayo-style base).
Name on the site: Gold Rush.
Label: the bottle says TOON SAUCE with a big protein badge (NOT "Gary's Chicken Sauce" — that name is retired for now, even though older scripts still use it).
Descriptor: "Restaurant-Style Chicken Sauce"
Protein (latest, Nov 19): 7g per serving. Per-bottle figure ~70g per 12oz bottle (assumes 10 servings — OPEN: confirm servings per bottle). Lead with the per-bottle number, "7g per serving" beneath.
Ignore older figures (8g / 80g, 11g, 10–12g) found in earlier docs.
Calories: OPEN — nutrition panel isn't locked. Use a placeholder; do not publish a calorie number or a "% fewer calories" claim.
Bottle: matte black squeeze bottle, golden amber cap (
#F2A93B), cream TOON SAUCE wordmark, protein badge near logo size.
Legal / claims guardrails (must follow)
Never write "Chick-fil-A" anywhere (copy, alt text, meta tags, ad copy). Say "restaurant-style chicken sauce."
Don't say "high-protein." 7g/serving supports "good source of protein" only. Safe phrasing: "7g protein per serving," "~70g protein per bottle."
"Fewer calories than…" needs a named comparison and a % difference — leave it out until numbers are final.
Per-bottle protein callouts still need regulatory sign-off; keep them easy to edit.
Never market to children. No kid-targeted imagery or language.
4. Characters (for the site)
Gary (launch Toon): anthropomorphic chicken. Round egg-shaped body, warm golden-amber feathers, oversized muscular wings used like arms, tiny thin legs, big hopeful eyes, small orange beak, red comb, white sweatband. Cheerful, wholesome, oblivious; people-pleaser who can't say no or admit he's wrong. Catchphrase: "Love that." (older: "Put me on everything!").
Plain: Gary's roommate, a plain boiled chicken breast. Pale gray, damp, half-lidded, deadpan. Always gray, even in color scenes. Great foil for "boring diet food" jokes.
World: the town of Blandville — a normal, everyday world. Toons are chickens/food characters; townspeople are human. Gary does not work for Toon Sauce in-world.
Teaser line for the site: "Something's coming out of Blandville."
5. Visual system

Principle: premium frame, chaotic character.

Token	Value	Use
Matte black	
#141414	Base / hero background
Warm cream	
#F6EEDF	Logo, text on dark; lower-section backgrounds
Gold Rush amber	
#F2A93B	Gary + sauce color; the hero color
Protein accent	OPEN — electric lime or hot red (being tested)	Protein callout only. Make it a single CSS variable so it can be swapped.
Logo: chunky hand-lettered "TOON SAUCE" title-card wordmark; works in one color. No eyes in the double O of "TOON" — ever.
Type: rounded heavy cartoon-title display (headlines); bold condensed sans (macro numbers); clean neutral sans (body).
Illustration style: prime-time adult animation, a mix of Family Guy (main influence), The Simpsons and Bob's Burgers, without copying any of them: clean even black outlines, rounded simplified shapes, flat bright color, minimal shading, big readable expressions. Original designs only.
Photography: real glossy sauce on real food (crispy tenders, wraps, rice bowls, fries); dark moody backgrounds, warm light; the sauce is the brightest thing in frame.
Avoid: primary colors on white (reads kids'), novelty/cheap look, cartoon hiding the food.
6. Page structure (decided direction)
Hero (dark, #141414): bottle + a flat cartoon Gary wing (amber, white sweatband) reaching in for it. Headline + tagline + protein badge (~70g per bottle / 7g per serving) + email field + "Join the waitlist" button.
Lower sections (cream, #F6EEDF): suggested content —
The product: Restaurant-Style Chicken Sauce, the protein number, real-food photography.
"Meet Gary" — short character intro, Plain as the deadpan foil.
Blandville teaser / "Something's coming out of Blandville" with video slot (launch intro "Welcome to Blandville" isn't produced yet — leave an embed placeholder).
Repeat waitlist capture at the bottom.
Footer: @toonsauce socials (Instagram, TikTok, YouTube — handles not confirmed), privacy policy, email consent language.

Asset note: final bottle render, Gary art and food photography don't exist yet. Use clearly labeled placeholders sized for the final assets. The bottle is being redesigned (photoreal sauce-dipped crispy tender + flat cartoon Gary wing on front; full Gary on the back).

7. Voice & copy

Rule of two voices: the Toons are chaos; the brand is calm and confident. Never joke about the numbers — state macros flat and exact.

Do: deadpan absurdity; roast boring diet food; write for men and women equally. Don't: pun overload or kid jokes; body/weight/eating shame; hedged numbers; gym-bro clichés ("gains," "beast mode"); swearing, sexual content, drugs, politics; real people or brands.

Sample lines (adapt numbers to 7g / ~70g):

"Warning: may cause you to eat chicken on purpose."
"Your sauce had 0g protein. Ours has a backstory."
"The sauce you already love. Plus protein. Minus the regret."
"Add protein without changing your meals."
8. Open items (leave placeholders)
Servings per bottle (confirms the ~70g figure); calories; full nutrition panel.
Protein accent color: lime vs. red.
QualifiedLead definition.
Domain and social handles (not confirmed secured).
Launch date.
Show title for the cartoon.
Trademark: full attorney clearance + Class 30 filing for TOON SAUCE still pending.
9. Reference links (claude.ai artifacts)
Brand bible: https://claude.ai/artifact/NgARsaUqETXbqZk4sYhYUR (some older numbers/names)
Brand & cartoon vision: https://claude.ai/artifact/N3XY3s5xNEks1ewWbBmNBG
Series bible + pilot: https://claude.ai/artifact/CSDGC87pixjmTJ71oaZXFs (still shows "Gary's Chicken Sauce"/11g in places — ignore those)
