import sys,asyncio
from playwright.sync_api import sync_playwright
base=sys.argv[1]; tag=sys.argv[2]; out='/workspace/13gypsies-luxe/shots'
import os; os.makedirs(out,exist_ok=True)
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome')
    for w,h in [(1440,900),(390,844)]:
        ctx=b.new_context(viewport={'width':w,'height':h},device_scale_factor=1 if w>1000 else 2)
        pg=ctx.new_page(); errs=[]
        pg.on('console',lambda m: errs.append(m.text) if m.type=='error' else None)
        for page in ['index','menu']:
            pg.goto(f'{base}{page}.html' if page!='index' else base,wait_until='load',timeout=60000); pg.wait_for_timeout(1800); pg.evaluate("document.documentElement.style.scrollBehavior='auto'")
            pg.screenshot(path=f'{out}/{tag}-{page}-{w}-hero.png')
            # scroll through
            H=pg.evaluate('document.body.scrollHeight')
            for y in range(0,H,500): pg.evaluate(f'scrollTo(0,{y})'); pg.wait_for_timeout(120)
            pg.wait_for_timeout(800)
            ov=pg.evaluate('document.documentElement.scrollWidth-innerWidth')
            print(page,w,'overflow',ov,'H',H)
            if page=='index':
                for sel in ['.intro','#kitchen','.atable','.house','#private','.reviews','#reserve','#visit','.ftr']:
                    pg.evaluate(f"document.querySelector('{sel}').scrollIntoView()"); pg.wait_for_timeout(1400)
                    pg.screenshot(path=f'{out}/{tag}-{w}-{sel.strip(".#")}.png')
                # pantry steps
                for i in range(5):
                    pg.evaluate(f"(()=>{{const s=document.querySelectorAll('.pt-step')[{i}];scrollTo(0,s.getBoundingClientRect().top+scrollY-innerHeight*{0.25 if w>1000 else 0.45})}})()"); pg.wait_for_timeout(2200)
                    pg.screenshot(path=f'{out}/{tag}-{w}-pt{i}.png')
            else:
                pg.evaluate('scrollTo(0,0)'); pg.wait_for_timeout(300)
                pg.screenshot(path=f'{out}/{tag}-{page}-{w}-full.png',full_page=True)
        print('errors',[e for e in errs if 'opentable' not in e.lower()][:8])
        ctx.close()
    b.close()
