#!/usr/bin/env python3
"""13 Gypsies luxe demo generator. python3 build.py [outdir]  (default ../site)"""
import os, sys, json, shutil, html
from data import *
OUT=sys.argv[1] if len(sys.argv)>1 else os.path.join(os.path.dirname(__file__),'..','site')
OUT=os.path.abspath(OUT); HERE=os.path.dirname(os.path.abspath(__file__))
os.makedirs(OUT,exist_ok=True)
for sub in ['assets']:
    if os.path.exists(f'{OUT}/{sub}'): shutil.rmtree(f'{OUT}/{sub}')
shutil.copytree(f'{HERE}/assets',f'{OUT}/assets')
shutil.copy(f'{HERE}/src/styles.css',f'{OUT}/assets/styles.css'); shutil.copy(f'{HERE}/src/script.js',f'{OUT}/assets/script.js')
for f in os.listdir(f'{HERE}/static'): shutil.copy(f'{HERE}/static/{f}',f'{OUT}/{f}')
V="5"
def img(name,alt,cls='',sizes='(max-width:900px) 92vw, 46vw',lazy=True,w=(1600,800),extra=''):
    a,b=w
    src=f"assets/img/{name}-{b}.webp"; ss=f"assets/img/{name}-{b}.webp {b}w, assets/img/{name}-{a}.webp {a}w"
    ld=' loading="lazy" decoding="async"' if lazy is True else (' decoding="async"' if lazy=='eager' else ' fetchpriority="high"')
    return f'<img class="{cls}" src="{src}" srcset="{ss}" sizes="{sizes}" alt="{alt}"{ld}{extra}>'
MARK='<span class="wm">13 Gypsies</span>'
def header(page):
    links=[('index.html#kitchen','The Kitchen'),('menu.html','Menu'),('index.html#private','Private Dining'),('index.html#visit','Visit')]
    if page=='index': links=[(h.replace('index.html',''),t) for h,t in links]
    nav=''.join(f'<a href="{h}"{" aria-current=page" if (page=="menu" and t=="Menu") else ""}>{t}</a>' for h,t in links)
    home='#top' if page=='index' else 'index.html'
    return f'''<a class="skip" href="#main">Skip to content</a>
<header class="hdr{' over' if page=='index' else ' solid'}" data-hdr>
 <a class="hdr-brand" href="{home}" aria-label="13 Gypsies, home">{MARK}</a>
 <nav class="hdr-nav" aria-label="Main">{nav}</nav>
 <div class="hdr-act"><a class="hdr-tel" href="{TEL}">{PHONE}</a><a class="btn sm" href="{'#reserve' if page=='index' else 'index.html#reserve'}">Reserve</a></div>
</header>'''
def footer():
    hrs=''.join(f'<li><span>{d}</span><span>{h}</span></li>' for _,d,h in HOURS)
    return f'''<footer class="ftr">
 <div class="ftr-in">
  <div class="ftr-brand">{MARK}<p class="ftr-tag">a peasant kitchen</p><p>Spanish tapas in historic Riverside, Jacksonville.</p><a class="btn light" href="index.html#reserve">Reserve a table</a></div>
  <div><h2 class="ftr-h">Find us</h2><p><a href="{GMAPS}" rel="noopener" target="_blank">{STREET}<br>{CITY}, {REGION} {ZIP}</a></p><p>At College &amp; Stockton, right off I‑10</p><p><a href="{TEL}">{PHONE}</a><br><a href="mailto:{EMAIL}">{EMAIL}</a></p></div>
  <div><h2 class="ftr-h">Hours</h2><ul class="ftr-hours">{hrs}</ul><p class="ftr-small">Last seating 90 minutes before close.</p></div>
  <div><h2 class="ftr-h">Follow</h2><p><a href="{IG}" rel="noopener" target="_blank">Instagram</a><br><a href="{FB}" rel="noopener" target="_blank">Facebook</a><br><a href="{OT_URL}" rel="noopener" target="_blank">OpenTable</a></p></div>
 </div>
 <p class="ftr-base">© 13 Gypsies · {ADDR} · <a href="menu.html">Menu</a> · Photos from guests on Google and OpenTable</p>
</footer>
<div class="mbar" data-mbar><a class="btn fill" href="index.html#reserve">Reserve</a><a class="btn" href="{TEL}">Call</a></div>
<aside class="demo" aria-label="Design preview notice"><span>Design preview by <b>RGWebD</b></span><button type="button" aria-label="Dismiss design preview notice">×</button></aside>'''
def ld_rest():
    days={0:'Sunday',1:'Monday',2:'Tuesday',3:'Wednesday',4:'Thursday',5:'Friday',6:'Saturday'}
    oh=[{"@type":"OpeningHoursSpecification","dayOfWeek":[days[2],days[3],days[4]],"opens":"17:00","closes":"21:00"},
        {"@type":"OpeningHoursSpecification","dayOfWeek":[days[5],days[6]],"opens":"17:00","closes":"22:00"}]
    return {"@context":"https://schema.org","@type":"Restaurant","@id":BASE+"#restaurant","name":NAME,"slogan":"A peasant kitchen","url":BASE,
      "image":[BASE+"assets/img/hero-2000.webp",BASE+"assets/og-image.jpg"],"logo":BASE+"assets/favicon-512.png","telephone":"+1-904-389-0330","email":EMAIL,
      "description":"Intimate Spanish tapas restaurant in historic Riverside, Jacksonville: seven tables, twenty seats, and nearly everything made in house, from bread and cheese to sausage and dry-cured meats.",
      "address":{"@type":"PostalAddress","streetAddress":STREET,"addressLocality":CITY,"addressRegion":REGION,"postalCode":ZIP,"addressCountry":"US"},
      "geo":{"@type":"GeoCoordinates","latitude":LAT,"longitude":LNG},"servesCuisine":["Spanish","Tapas","Mediterranean"],"priceRange":"$$",
      "openingHoursSpecification":oh,"acceptsReservations":OT_URL,"hasMenu":BASE+"menu.html","paymentAccepted":"AMEX, Discover, Mastercard, Visa",
      "aggregateRating":{"@type":"AggregateRating","ratingValue":G_RATING,"reviewCount":G_COUNT,"bestRating":5},
      "sameAs":[FB,IG,OT_URL,GMAPS]}
def head(title,desc,path,extra_ld=None):
    ld=[ld_rest()]+(extra_ld or [])
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{title}</title><meta name="description" content="{desc}"><link rel="canonical" href="{BASE}{path}">
<meta property="og:type" content="restaurant"><meta property="og:title" content="{title}"><meta property="og:description" content="{desc}"><meta property="og:url" content="{BASE}{path}"><meta property="og:image" content="{BASE}assets/og-image.jpg"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{title}"><meta name="twitter:description" content="{desc}"><meta name="twitter:image" content="{BASE}assets/og-image.jpg">
<meta name="theme-color" content="#F4EEE3"><link rel="icon" href="favicon.ico" sizes="any"><link rel="icon" type="image/png" sizes="32x32" href="assets/favicon-32.png"><link rel="apple-touch-icon" href="apple-touch-icon.png">
<link rel="preload" href="assets/fonts/fraunces-normal.woff2" as="font" type="font/woff2" crossorigin><link rel="preload" href="assets/fonts/jost-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="assets/styles.css?v={V}"><script>document.documentElement.classList.add('js')</script>
<script type="application/ld+json">{json.dumps(ld if len(ld)>1 else ld[0],ensure_ascii=False)}</script></head>'''
hours_rows=''.join(f'<tr data-d="{n}"><th scope="row">{d}</th><td>{h}</td></tr>' for n,d,h in HOURS)
def stars(r): return f'<span class="stars" style="--r:{r/5*100:.0f}%" aria-hidden="true"><span>★★★★★</span><span>★★★★★</span></span>'

# ---------------- index ----------------
pantry_steps=''.join(f'''<li class="pt-step" data-i="{i}"><span class="pt-num">{n}</span><h3 class="pt-h">{t}</h3><p>{d}</p><figure class="pt-inline">{img(ph,alt,'',sizes='(max-width:900px) 88vw, 40vw',w=(1200,700))}</figure></li>''' for i,(n,t,d,ph,alt) in enumerate(PANTRY))
pantry_stage=''.join(f'<figure class="pt-shot{" on" if i==0 else ""}" data-i="{i}">{img(ph,alt,"",sizes="(max-width:900px) 92vw, 44vw",w=(1200,700),lazy='eager')}</figure>' for i,(n,t,d,ph,alt) in enumerate(PANTRY))
pantry_ticks=''.join(f'<li data-i="{i}"{" class=on" if i==0 else ""}><span>{n}</span></li>' for i,(n,t,d,ph,alt) in enumerate(PANTRY))
formats=''.join(f'<div class="fm-row"><dt>{a}</dt><dd>{b}</dd></div>' for a,b in FORMATS)
revs=''.join(f'<figure class="rv"><blockquote>“{q}”</blockquote><figcaption>{n} · {s}</figcaption></figure>' for n,s,q in REV)
index=head("13 Gypsies · Spanish Tapas in Riverside, Jacksonville FL",
 "13 Gypsies is an intimate Spanish tapas restaurant in historic Riverside, Jacksonville: seven tables, twenty seats, and nearly everything made in house. Dinner Tue–Sat. Reserve on OpenTable or call (904) 389-0330.","")+f'''
<body class="p-home" id="top">
{header('index')}
<main id="main">
<section class="hero" aria-label="13 Gypsies">
 <div class="hero-ph">{img('hero','The dining room at 13 Gypsies: café tables with carnations, the harlequin bar and the kitchen pass','',sizes='100vw',lazy=False,w=(2000,1200))}</div>
 <div class="hero-in">
  <p class="hero-mark" aria-hidden="true">13 Gypsies</p>
  <p class="hero-tag">a peasant kitchen</p>
  <h1 class="hero-h1">Spanish tapas in historic Riverside, Jacksonville</h1>
  <div class="hero-cta"><a class="btn fill" href="#reserve">Reserve a table</a><a class="btn ghost" href="menu.html">View the menu</a></div>
 </div>
 <p class="hero-info"><span class="hi-h">Tue – Thu 5 – 9 PM · Fri – Sat 5 – 10 PM</span><span class="dot d1" aria-hidden="true"></span><span>{STREET}</span><span class="dot" aria-hidden="true"></span><a href="{TEL}">{PHONE}</a></p>
</section>

<section class="intro sec" aria-labelledby="intro-h">
 <p class="eyebrow">Historic Riverside · Jacksonville</p>
 <h2 id="intro-h" class="intro-h">Seven tables. Twenty seats.<br><em>Nearly everything made by hand.</em></h2>
 <p class="lede">13 Gypsies is a small, intimate tapas room on the corner of College and Stockton. The kitchen cooks creative and classic Spanish dishes with Spanish technique, and makes almost everything itself, from the morning bread to the cheese, sausage and cured meats.</p>
 <ul class="creds" aria-label="Ratings and recognition">
  <li><b>{OT_RATING}</b><span>OpenTable<br>{OT_COUNT} reviews</span></li>
  <li><b>{G_RATING}</b><span>Google<br>{G_COUNT} reviews</span></li>
  <li><b class="w">Best Overall</b><span>OpenTable diners’<br>awards, Jacksonville</span></li>
  <li><a href="{TU_URL}" rel="noopener" target="_blank"><b class="w">Romantic Jacksonville</b><span>The Florida Times‑Union<br>February 2026</span></a></li>
 </ul>
</section>

<section class="pantry sec" id="kitchen" aria-labelledby="pt-h" data-pantry>
 <div class="pt-head"><p class="eyebrow">The house-made pantry</p><h2 id="pt-h" class="h2">From scratch, <em>every morning</em></h2><p class="pt-sub">The kitchen makes its own bread, cheese, sausage, cured meats, pickles, spice blends and fresh pasta. Five of them, in their own words.</p></div>
 <div class="pt-grid">
  <div class="pt-stage" aria-hidden="true"><div class="pt-frame">{pantry_stage}</div><div class="pt-cap"><ol class="pt-ticks">{pantry_ticks}</ol><p class="pt-now">{PANTRY[0][1]}</p></div></div>
  <ol class="pt-steps">{pantry_steps}</ol>
 </div>
 <p class="pt-foot">Because everything is made fresh, a dish can run out during service. <em>First come, first eat.</em></p>
</section>

<section class="atable sec" aria-labelledby="tb-h">
 <figure class="tb-ph">{img('f-gambas','Garlic shrimp in a clay dish with slices of house baguette')}</figure>
 <div class="tb-tx"><p class="eyebrow">At the table</p><h2 id="tb-h" class="h2">Small plates, <em>shared slowly</em></h2>
  <dl class="fm">{formats}</dl>
  <a class="lnk" href="menu.html">See the menu</a></div>
</section>

<section class="house sec" aria-labelledby="hs-h">
 <div class="hs-tx"><p class="eyebrow">The house</p><h2 id="hs-h" class="h2">A 1923 room <em>full of saints</em></h2>
  <p>13 Gypsies sits in a two-story Spanish-style building designed in 1923 by Henrietta Dozier, Jacksonville’s only female architect in the early part of the twentieth century. Inside: the original floor tile, a harlequin bar and walls of maximalist religious iconography.</p>
  <p>In the kitchen, Chef Kevan Kimball and his crew run a true craft kitchen, with wines mainly from Spain and beer from Florida.</p>
  <blockquote class="pull">“If you start with good ingredients, preparation is minimal and the end result is good, honest food.”<cite>From the 13 Gypsies story</cite></blockquote></div>
 <figure class="hs-ph">{img('bar','The harlequin-painted bar beneath a wall of icons, candles and framed saints')}</figure>
</section>

<section class="private sec" id="private" aria-labelledby="pv-h">
 <figure class="pv-ph">{img('dining','Café tables set by the front windows on Stockton Street',sizes='(max-width:900px) 100vw, 55vw')}</figure>
 <div class="pv-tx"><p class="eyebrow">Private dining</p><h2 id="pv-h" class="h2">Reserve <em>the whole restaurant</em></h2>
  <p>Book all seven tables for an all-inclusive flat rate that covers food, alcohol and beverages, room rental, sales tax and gratuity.</p>
  <p class="pv-for">Rehearsal dinners · Holiday parties · Birthdays</p>
  <div class="pv-cta"><a class="btn fill" href="{TEL}">Call {PHONE}</a></div>
  <p class="small">Every party is different, so the details are arranged by phone.</p></div>
</section>

<section class="reviews sec" aria-labelledby="rv-h">
 <h2 id="rv-h" class="eyebrow">From our guests</h2>
 <p class="rv-line">{stars(OT_RATING)} <span>{OT_RATING} on OpenTable from {OT_COUNT} diners</span><span class="dot" aria-hidden="true"></span><span>{G_RATING} on Google from {G_COUNT} reviews</span></p>
 <div class="rv-grid">{revs}</div>
</section>

<section class="reserve sec" id="reserve" aria-labelledby="rs-h">
 <div class="rs-in">
  <p class="eyebrow">Reservations</p><h2 id="rs-h" class="rs-h">Your table <em>awaits</em></h2>
  <p class="rs-sub">There are only seven tables, and none are held for walk-ins. Reservations are highly recommended.</p>
  <div class="otw" data-rid="{OT_RID}"><p class="otload">Loading OpenTable availability…</p></div>
  <div class="rs-cta"><a class="btn fill" href="{OT_URL}" rel="noopener" target="_blank">Reserve on OpenTable</a><a class="btn" href="{TEL}">Call {PHONE}</a></div>
  <ul class="rs-notes"><li>Last seating is an hour and a half before closing.</li><li>The two sidewalk tables can’t always move inside if the weather turns.</li><li>Larger party or the whole room? Call us.</li></ul>
 </div>
</section>

<section class="visit sec" id="visit" aria-labelledby="vs-h">
 <figure class="vs-ph">{img('front','The 13 Gypsies storefront at 887 Stockton Street, with red chairs under the awning')}</figure>
 <div class="vs-tx"><p class="eyebrow">Visit</p><h2 id="vs-h" class="h2">On the corner of <em>College &amp; Stockton</em></h2>
  <p class="status" data-status><i aria-hidden="true"></i><span>Dinner Tuesday to Saturday from 5 PM</span></p>
  <div class="vs-cols">
   <div><h3 class="h3">Address</h3><p><a href="{GMAPS}" rel="noopener" target="_blank">{STREET}<br>{CITY}, {REGION} {ZIP}</a></p><p>Historic Riverside, right off I‑10, in the same strip as Bold Bean and Zencog.</p><p><a class="lnk" href="{DIR}" rel="noopener" target="_blank">Directions</a></p></div>
   <div><h3 class="h3">Hours</h3><table class="hours"><caption class="sr">Opening hours</caption>{hours_rows}</table></div>
   <div><h3 class="h3">Good to know</h3><ul class="gtk"><li>Street parking nearby</li><li>Casual dress, no pretense</li><li>Gluten-free and vegetarian options</li><li>Wheelchair-accessible entrance</li><li>AMEX, Discover, Mastercard, Visa</li></ul></div>
  </div></div>
</section>
</main>
{footer()}
<script src="assets/script.js?v={V}" defer></script>
</body></html>'''
open(f'{OUT}/index.html','w').write(index)

# ---------------- menu ----------------
chips='<button type="button" class="chip on" data-f="all" aria-pressed="true">All</button>'+''.join(f'<button type="button" class="chip" data-f="{k}" aria-pressed="false">{t}</button>' for k,t,_ in MENU)
secs=''.join(f'''<section class="mn-sec" data-k="{k}" aria-labelledby="mn-{k}"><h2 id="mn-{k}" class="mn-h">{t}</h2><ul class="mn-list">{''.join(f'<li><h3>{n}</h3><p>{d}</p></li>' for n,d in items)}</ul></section>''' for k,t,items in MENU)
menu_ld={"@context":"https://schema.org","@type":"Menu","name":"13 Gypsies menu","url":BASE+"menu.html","inLanguage":"en","hasMenuSection":[{"@type":"MenuSection","name":html.unescape(t),"hasMenuItem":[{"@type":"MenuItem","name":n,"description":d} for n,d in items]} for k,t,items in MENU]}
crumbs={"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":BASE},{"@type":"ListItem","position":2,"name":"Menu","item":BASE+"menu.html"}]}
menu=head("Menu · 13 Gypsies, Spanish Tapas in Jacksonville",
 "The 13 Gypsies menu: vegetables, meat and seafood, cold tapas, house pasta and daily offerings, made in house in Riverside, Jacksonville. The menu changes; call (904) 389-0330 for tonight's offerings.","menu.html",[menu_ld,crumbs])+f'''
<body class="p-menu">
{header('menu')}
<main id="main">
<section class="mn-hero sec" aria-labelledby="mn-title">
 <p class="eyebrow">The menu</p><h1 id="mn-title" class="mn-title">Small plates, <em>made in house</em></h1>
 <p class="lede">Tapas are meant for the table: order a few, share them, then order a few more. Bread, cheese, sausage, cured meats, pickles and pasta are all made here.</p>
 <dl class="mn-fmt"><div><dt>To share</dt><dd>Vegetables, meat and seafood, cold plates and house pasta</dd></div><div><dt>Daily offerings</dt><dd>Tonight’s risotto, From the Chamber and peasant bread</dd></div><div><dt>To drink</dt><dd>Mostly Spanish wines, Florida beer, cocktails and sangria</dd></div></dl>
</section>
<figure class="mn-band">{img('tile','The black-and-white harlequin bar front above the original mosaic floor tile',sizes='(max-width:900px) 100vw, 1100px',w=(1600,800))}</figure>
<section class="mn-body sec" aria-label="Dishes">
 <div class="chips" role="group" aria-label="Filter the menu">{chips}</div>
 <div class="mn-grid">{secs}</div>
 <p class="mn-note">The menu changes with the kitchen and the season, and dishes can run out during service. Desserts are made in house and change often. Call <a href="{TEL}">{PHONE}</a> for tonight’s offerings, and tell your server about any allergies.</p>
</section>
<section class="mn-cta sec"><h2 class="h2">Seven tables, <em>book yours</em></h2><div class="rs-cta"><a class="btn fill" href="{OT_URL}" rel="noopener" target="_blank">Reserve on OpenTable</a><a class="btn" href="{TEL}">Call {PHONE}</a></div></section>
</main>
{footer()}
<script src="assets/script.js?v={V}" defer></script>
</body></html>'''
open(f'{OUT}/menu.html','w').write(menu)

# ---------------- 404 ----------------
p404=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Page not found · 13 Gypsies</title><meta name="robots" content="noindex"><link rel="icon" href="/{REPO}/favicon.ico"><link rel="stylesheet" href="/{REPO}/assets/styles.css?v={V}"></head>
<body class="p-404"><main class="nf"><a class="hdr-brand" href="/{REPO}/">{MARK}</a><h1 class="mn-title">This table <em>isn’t set</em></h1><p class="lede">The page you were looking for isn’t here. The dining room is.</p><div class="rs-cta"><a class="btn fill" href="/{REPO}/">Back to 13 Gypsies</a><a class="btn" href="/{REPO}/menu.html">Menu</a></div></main></body></html>'''
open(f'{OUT}/404.html','w').write(p404)
open(f'{OUT}/robots.txt','w').write(f"User-agent: *\nAllow: /\nSitemap: {BASE}sitemap.xml\n")
open(f'{OUT}/sitemap.xml','w').write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>{BASE}</loc><priority>1.0</priority></url><url><loc>{BASE}menu.html</loc><priority>0.8</priority></url></urlset>\n')
mtxt='\n'.join(f"- {html.unescape(t)}: "+'; '.join(f"{n} ({d})" for n,d in items) for k,t,items in MENU)
open(f'{OUT}/llms.txt','w').write(f"""# 13 Gypsies

> Intimate Spanish tapas restaurant ("a peasant kitchen") in historic Riverside, Jacksonville, Florida. Seven tables, about twenty seats. Nearly everything is made in house: bread, cheese, sausage, dry-cured meats, pickled vegetables, spice blends and fresh pasta.

- Address: {ADDR} (corner of College St and Stockton St, right off I-10)
- Phone: {PHONE} · Email: {EMAIL}
- Hours: Tuesday–Thursday 5–9 PM; Friday–Saturday 5–10 PM; closed Sunday and Monday. Last seating 90 minutes before close.
- Reservations: highly recommended, on OpenTable ({OT_URL}) or by phone. Tables are not held for walk-ins.
- Private dining: the whole restaurant can be reserved for an all-inclusive flat rate (food, beverages, room, tax, gratuity). Call for details.
- Chef: Chef Kevan Kimball and crew. Building: 1923 Spanish-style building by architect Henrietta Dozier.
- Ratings: OpenTable {OT_RATING} ({OT_COUNT} reviews); Google {G_RATING} ({G_COUNT} reviews).
- Dress: casual. Parking: street parking. Gluten-free and vegetarian options.

## Pages
- Home: {BASE}
- Menu: {BASE}menu.html

## Menu (changes often; no prices listed)
{mtxt}
""")
print('built',OUT)
