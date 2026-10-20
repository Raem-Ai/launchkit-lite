/* Etsy Title Fixer · free bookmarklet · github.com/Raem-Ai/etsy-title-fixer
   Runs on etsy.com only. Reads a listing title, asks Etsy's own search-suggestion box what buyers type,
   and scores the title on how many of those buyer phrases it contains (and how early). Nothing leaves your browser. */
(async function(){
  const V='10_12672349415_19';
  const STOP=new Set('a an the and or of for with to in on by at from your my our this that is are be it as its printable digital download instant pdf template editable set kit pack bundle'.split(' '));
  const norm=s=>s.toLowerCase().replace(/[^a-z0-9 ]+/g,' ').replace(/\s+/g,' ').trim();
  async function sugg(q){
    try{const r=await fetch('/suggestions_ajax.php?version='+V+'&search_query='+encodeURIComponent(q)+'&search_type=all',{credentials:'omit'});
      const j=await r.json(); return (j.results||[]).map(x=>x.query||'').filter(q=>q&&!/[<>]/.test(q)).map(norm).filter(Boolean);}catch(e){return []}
  }
  function getTitle(){
    const i=document.querySelector('#listing-title-input, input[name="title"]'); if(i&&i.value) return i.value;
    const h=document.querySelector('h1'); if(h) return h.innerText.trim();
    return prompt('Paste the listing title:')||'';
  }
  const raw=getTitle(); if(!raw) return;
  const title=norm(raw); const words=title.split(' ');

  const seeds=new Set();
  const ww=words.filter(w=>!STOP.has(w));
  ww.forEach(w=>seeds.add(w)); for(let i=0;i<ww.length-1;i++) seeds.add(ww[i]+' '+ww[i+1]);
  const seedList=[...seeds].slice(0,24);
  const box=document.createElement('div'); box.id='etf-box';
  box.style.cssText='position:fixed;top:16px;right:16px;width:420px;max-height:90vh;overflow:auto;z-index:999999;background:#0d1012;color:#f7f4ec;font:14px/1.45 Inter,system-ui,sans-serif;border:1px solid rgba(255,255,255,.14);border-radius:16px;padding:18px 20px;box-shadow:0 30px 80px rgba(0,0,0,.6)';
  box.innerHTML='<div style="display:flex;justify-content:space-between;align-items:center"><b style="font-size:16px">Etsy Title Fixer</b><span id="etf-x" style="cursor:pointer;opacity:.7">✕</span></div><div id="etf-b" style="margin-top:10px;opacity:.8">Asking Etsy what buyers type… (0/'+seedList.length+')</div>';
  document.body.appendChild(box); box.querySelector('#etf-x').onclick=()=>box.remove();
  const status=box.querySelector('#etf-b');
  const phrases=new Map();
  let n=0;
  for(const s of seedList){
    const res=await sugg(s); n++; status.textContent='Asking Etsy what buyers type… ('+n+'/'+seedList.length+')';
    res.forEach((p,rank)=>{ if(!phrases.has(p)||phrases.get(p).rank>rank) phrases.set(p,{seed:s,rank}); });
    await new Promise(r=>setTimeout(r,120));
  }

  const hits=[],misses=[];
  for(const [p,m] of phrases){
    const idx=title.indexOf(p);
    if(idx>=0&&p.split(' ').length>=2) hits.push({p,pos:idx,rank:m.rank});
    else if(p.split(' ').length>=2){ const shared=p.split(' ').filter(w=>!STOP.has(w)&&words.includes(w)).length; if(shared>=2||(shared>=1&&m.seed.includes(' '))) misses.push({p,rank:m.rank,seed:m.seed,shared}); }
  }
  hits.sort((a,b)=>a.pos-b.pos); misses.sort((a,b)=>(b.shared-a.shared)||(a.rank-b.rank));
  const first=hits.length?hits[0].pos:999;
  let score=Math.min(60,hits.length*15)+(first===0?40:first<20?25:first<60?10:0);
  score=Math.max(0,Math.min(100,score));

  const best=hits[0]?hits[0].p:(misses.find(m=>m.p.split(' ').some(w=>!STOP.has(w)&&words.includes(w)))||{}).p;
  let rewrite='';
  if(best&&!(hits[0]&&hits[0].pos===0)){ const rest=raw.replace(new RegExp(best.replace(/ /g,'\\s+'),'i'),'').replace(/\s*[|,\-–·]\s*$/,'').replace(/^\s*[|,\-–·]\s*/,'').trim();
    rewrite=(best.replace(/\b\w/g,c=>c.toUpperCase())+' | '+rest).replace(/\s+/g,' ').slice(0,140); }
  const li=(a)=>a.length?'<ul style="margin:6px 0 0 18px;padding:0">'+a.map(x=>'<li>'+x+'</li>').join('')+'</ul>':'<div style="opacity:.6;margin-top:4px">none</div>';
  const color=score>=70?'#36d0c2':score>=40?'#d89b52':'#e5484d';
  status.outerHTML='<div style="margin-top:12px;font-size:12px;letter-spacing:.14em;text-transform:uppercase;opacity:.6">Your title</div><div style="margin-top:4px">'+raw.replace(/</g,'&lt;')+'</div>'
   +'<div style="display:flex;align-items:baseline;gap:10px;margin-top:14px"><span style="font-size:44px;font-weight:800;color:'+color+'">'+score+'</span><span style="opacity:.7">/100 · buyer-search score</span></div>'
   +'<div style="margin-top:10px"><b>Buyer phrases already in your title</b> ('+hits.length+')'+li(hits.map(h=>h.p+(h.pos===0?' <span style="color:#36d0c2">· first ✓</span>':'')))+'</div>'
   +'<div style="margin-top:12px"><b>What buyers actually type</b> (Etsy suggests these, your title doesn\'t have them)'+li(misses.slice(0,10).map(m=>m.p))+'</div>'
   +(hits[0]&&hits[0].pos===0?'<div style="margin-top:14px;color:#36d0c2;font-weight:700">Already buyer-words-first ✓ Keep it.</div>':'')+(rewrite?'<div style="margin-top:14px;padding:12px;border:1px solid #36d0c2;border-radius:12px"><div style="font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:#36d0c2">Suggested rewrite · buyer words first</div><div id="etf-rw" style="margin-top:6px">'+rewrite.replace(/</g,'&lt;')+'</div><button id="etf-cp" style="margin-top:10px;background:#36d0c2;color:#050607;border:0;border-radius:999px;padding:8px 14px;font-weight:700;cursor:pointer">Copy</button></div>':'')
   +'<div style="margin-top:14px;font-size:12px;opacity:.55">Score = how many Etsy-suggested buyer phrases your title contains, and whether one is first. Nothing leaves your browser. Free, by RAEM · carlosg.ai/challenge</div>';
  const cp=box.querySelector('#etf-cp'); if(cp) cp.onclick=()=>{navigator.clipboard.writeText(rewrite); cp.textContent='Copied'};
})();
