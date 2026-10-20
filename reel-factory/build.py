import json,re,sys,asyncio,pathlib
from playwright.async_api import async_playwright
P=json.load(open('work/plan.json')); CAPS=json.load(open('work/caps.json'))
L={}
for n in ['gumroad','github','etsy','pinterest']:
    s=open(f'broll6/{n}.svg').read(); s=re.sub(r'<title>.*?</title>','',s)
    fill={'gumroad':'#000','github':'#181717','etsy':'#fff','pinterest':'#fff'}[n]
    L[n]=s.replace('<svg ',f'<svg fill="{fill}" ')
h=open('overlay.html').read().replace('__PLAN__',json.dumps(P)).replace('__LOGOS__',json.dumps(L)).replace('__CAPS__',json.dumps(CAPS))
open('overlay_built.html','w').write(h)
FPS=30
async def shoot(ts,out,names=None):
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1080,'height':1920})
        pg.on('pageerror',lambda e:print('JSERR',e))
        await pg.goto('file://'+str(pathlib.Path('overlay_built.html').resolve())); await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(900)
        o=pathlib.Path(out); o.mkdir(exist_ok=True)
        for i,t in enumerate(ts):
            await pg.evaluate(f'render({t})'); await pg.screenshot(path=str(o/(names[i] if names else f'f{i:05d}.png')),omit_background=True)
            if i%300==0: print(i,flush=True)
        await b.close()
if sys.argv[1]=='prev':
    ts=[float(x) for x in sys.argv[2].split(',')]; asyncio.run(shoot(ts,'prev9',[f'p{t:06.2f}.png' for t in ts]))
elif sys.argv[1]=='part':
    n,k=int(sys.argv[2]),int(sys.argv[3]); idx=[i for i in range(int(P['TOTAL']*FPS)+1) if i%k==n]
    asyncio.run(shoot([i/FPS for i in idx],'ovl',[f'f{i:05d}.png' for i in idx]))
else:
    asyncio.run(shoot([i/FPS for i in range(int(P['TOTAL']*FPS)+1)],'ovl'))
