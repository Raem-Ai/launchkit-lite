import json,re
import sys
W=json.load(open(sys.argv[1] if len(sys.argv)>1 else 'work8/words.json'))
# glue Whisper's split tokens back together ("$10" ",000" / "$1" ".60" / "25" "%" / "carlosg" ".ai")
G=[]
for w in W:
    if G and re.match(r'^[,.%]\w*',w['text']) and re.search(r'[\w$]$',G[-1]['text']): G[-1]=dict(text=G[-1]['text']+w['text'],start=G[-1]['start'],end=w['end'])
    else: G.append(dict(w))
W=G
# merge spoken numbers into numerals (keeps timing of the span)
REP=[(['one','hundred','dollars'],'$100'),(['ten','thousand'],'$10,000'),(['thirty','days'],'30 days'),(['zero','dollars'],'$0'),
     (['one','dollar','sixty'],'$1.60'),(['twenty-one'],'21'),(['forty-three'],'43'),(['twenty-five','percent'],'25%'),(['fifteen','days'],'15 days'),
     (['one','hundred'],'100'),(['day','one'],'Day 1'),(['day','two'],'Day 2'),(['day','three'],'Day 3'),(['thirty'],'30'),(['zero'],'0'),(['one','sale'],'1 sale')]
def norm(x): return re.sub(r'[^a-z\-]','',x.lower())
out=[];i=0
while i<len(W):
    for seq,rep in REP:
        n=len(seq)
        if [norm(w['text']) for w in W[i:i+n]]==seq:
            last=W[i+n-1]['text']; tail=re.sub(r'^[\w\-$]+','',last.split('.')[0] if last.endswith('.ai.') else '')
            punct=re.findall(r'[.,?!]+$',last); txt=rep+(punct[0] if punct else '')
            if W[i]['text'][:1].isupper() and rep[0].islower(): txt=txt[0].upper()+txt[1:]
            out.append(dict(w=txt,s=W[i]['start'],e=W[i+n-1]['end'])); i+=n; break
    else:
        out.append(dict(w=W[i]['text'],s=W[i]['start'],e=W[i]['end'])); i+=1
# chunk
C=[];cur=[]
for k,w in enumerate(out):
    cur.append(w); txt=' '.join(x['w'] for x in cur); nxt=out[k+1] if k+1<len(out) else None
    brk= nxt is None or len(txt)>=22 or (re.search(r'[.?!]$',w['w']) or (w['w'].endswith(',') and len(txt)>=10)) or (nxt and nxt['s']-w['e']>0.35) or len(cur)>=5
    if nxt and len(txt+' '+nxt['w'])>30: brk=True
    if brk: C.append(cur); cur=[]
caps=[]
for j,c in enumerate(C):
    t0=c[0]['s']-0.05; t1=c[-1]['e']+0.25
    if j+1<len(C): t1=min(t1,C[j+1][0]['s']-0.05)
    caps.append(dict(t0=round(t0,3),t1=round(t1,3),w=[dict(w=x['w'],s=x['s'],e=x['e']) for x in c]))
json.dump(caps,open(sys.argv[2] if len(sys.argv)>2 else 'work8/caps.json','w'))
print(len(caps),'chunks'); [print(c['t0'],' '.join(x['w'] for x in c['w'])) for c in caps[:12]]; print('...'); [print(c['t0'],' '.join(x['w'] for x in c['w'])) for c in caps if 46<c['t0']<52 or 109<c['t0']<121 or c['t0']>140]
