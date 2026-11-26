import sys,json,re
from playwright.sync_api import sync_playwright
base=sys.argv[1]; fails=[]
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome')
    for rm in ['no-preference','reduce']:
      for w,h in [(1440,900),(390,844)]:
        ctx=b.new_context(viewport={'width':w,'height':h},reduced_motion=rm); pg=ctx.new_page(); errs=[]
        pg.on('console',lambda m: errs.append(m.text) if m.type=='error' else None)
        pg.on('pageerror',lambda e: errs.append(str(e)))
        for page in ['','menu.html','404.html']:
            r=pg.goto(base+page,wait_until='load',timeout=60000); pg.wait_for_timeout(1200)
            pg.evaluate("document.documentElement.style.scrollBehavior='auto'")
            H=pg.evaluate('document.body.scrollHeight')
            for y in range(0,H+900,450): pg.evaluate(f'scrollTo(0,{y})'); pg.wait_for_timeout(60)
            pg.wait_for_timeout(1500)
            tag=f'{rm}/{w}/{page or "index"}'
            ov=pg.evaluate('document.documentElement.scrollWidth-innerWidth')
            if ov>0: fails.append(f'{tag} overflow {ov}')
            bad=pg.evaluate("[...document.images].filter(i=>i.getClientRects().length&&(!i.complete||i.naturalWidth===0)).map(i=>i.currentSrc||i.src)")
            if bad: fails.append(f'{tag} broken imgs {bad}')
            for s in pg.evaluate("[...document.querySelectorAll('script[type=\"application/ld+json\"]')].map(s=>s.textContent)"):
                try: json.loads(s)
                except Exception as e: fails.append(f'{tag} bad jsonld {e}')
            txt=pg.inner_text('body')
            if re.search(r'\{[A-Z_]+\}',txt): fails.append(f'{tag} placeholder leak')
            names=pg.evaluate("[...document.querySelectorAll('main img')].filter(i=>i.offsetParent!==null||getComputedStyle(i.closest('figure')||i).display!=='none').map(i=>(i.currentSrc||i.src).split('/').pop().replace(/-\\d+\\.webp.*/,''))")
            # visible images only (stage vs inline are alternates)
            vis=pg.evaluate("[...document.querySelectorAll('main img')].filter(i=>{const r=i.getBoundingClientRect();return r.width>0&&r.height>0}).map(i=>(i.currentSrc||i.src).split('/').pop().replace(/-\\d+\\.webp.*/,''))")
            dup=[n for n in set(vis) if vis.count(n)>1]
            if dup: fails.append(f'{tag} duplicate photos {dup}')
            hidden=pg.evaluate("[...document.querySelectorAll('.rv-up')].filter(e=>getComputedStyle(e).opacity<0.99).length")
            if hidden: fails.append(f'{tag} {hidden} reveal elements still hidden')
            if w==390 and page=='':
                pg.evaluate('scrollTo(0,1200)'); pg.wait_for_timeout(700)
                mb=pg.evaluate("(()=>{const r=document.querySelector('.mbar').getBoundingClientRect();return [r.top,r.bottom,innerHeight]})()")
                if mb[1]>mb[2]+1: fails.append(f'{tag} mbar not visible {mb}')
            if page=='' :
                n=pg.evaluate("document.querySelectorAll('a[href$=\"#reserve\"],a[href*=\"opentable.com/r/\"]').length")
                if n<3: fails.append(f'{tag} reserve links {n}')
                if rm=='reduce' and pg.evaluate("document.querySelector('.pantry').classList.contains('live')"): fails.append(f'{tag} pantry live under reduced motion')
            if page=='menu.html':
                pg.click('.chip[data-f="pasta"]'); pg.wait_for_timeout(200)
                v=pg.evaluate("[...document.querySelectorAll('.mn-sec')].filter(s=>s.offsetParent!==null).map(s=>s.dataset.k)")
                if v!=['pasta']: fails.append(f'{tag} chip filter {v}')
        e=[x for x in errs if 'opentable' not in x.lower() and 'accelerometer' not in x.lower()]
        if e: fails.append(f'{rm}/{w} console {e[:5]}')
        ctx.close()
    b.close()
print('FAILS:' if fails else 'QA PASS', *fails, sep='\n')
