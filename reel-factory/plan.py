import json,re
T={x['k']:x for x in json.load(open('work/timeline.json'))['TL']}; TOTAL=json.load(open('work/total.json'))
WD=json.load(open('work/words.json'))
A=lambda k,o=0: round(T[k]['t0']+o,3)
E=lambda k,o=0: round(T[k]['t1']+o,3)
def norm(s): return re.sub(r'[^a-z0-9$?]','',s.lower())
def Wt(k,word,n=1,end=False):
    a,b=T[k]['t0']-0.2,T[k]['t1']+0.2; c=0
    for w in WD:
        if a<=w['start']<=b and norm(w['text']).startswith(norm(word)):
            c+=1
            if c==n: return round(w['end'] if end else w['start'],3)
    print('MISS',k,word); return A(k)
P={}
# music/SFX anchors
DROP=A('d2')-0.05                       # music out, typing stops: the strategy drop
BACK=Wt('d3c','this')-0.1               # music returns
PLAN=Wt('d5','planner')                 # the word "PLANNER!"
DR=PLAN-2.3                             # drumroll start so its cymbal hit lands on PLANNER
WOMP=PLAN+0.55                          # sad trombone
MUS2=A('c5')-0.1                        # music back for the close
P.update(DROP=DROP,BACK=BACK,PLAN=PLAN,DR=DR,WOMP=WOMP,MUS2=MUS2)
P['full']=[dict(id='visits',a=Wt('c2','saw')-0.1,b=Wt('c2','what')-0.12,k=[Wt('c2','4'),Wt('c2','4')+0.45,Wt('c2','moving')]),
           dict(id='bets',a=Wt('d3c','this')-0.1,b=E('d3c',0.1),k=[Wt('d3c','products'),Wt('d3c','stores'),Wt('d3c','people'),Wt('d3c','whatever'),Wt('d3c','feed')]),
           dict(id='wall',a=PLAN+0.05,b=E('d5',0.05),k=[WOMP+0.1])]
P['split']=[]
iw=[w for w in WD if w['start']<T['intro']['t1']]
def iwt(word):
    for w in iw:
        if norm(w['text'])==norm(word): return w['start']
    for w in iw:
        if norm(w['text']).startswith(norm(word)): return w['start']
    return 1.0
P['scene']=[dict(id='kin',a=A('intro',0.3),b=E('intro',-0.1),k=[iwt('$100'),iwt('$10,000'),iwt('let')]),
            dict(id='band',a=A('c1',0.3),b=A('c1',2.8)),
            dict(id='newplan',a=Wt('d2','plan')-0.05,b=E('d2',0.2)),
            dict(id='six',a=Wt('d3a','4')-0.05,b=E('d3b',0.1),k=[Wt('d3a','4'),Wt('d3a','6'),Wt('d3a','slow'),Wt('d3b','one'),Wt('d3b','not')]),
            dict(id='spot',a=DR,b=PLAN+0.05),
            dict(id='sold',a=WOMP+0.1,b=E('c4',0.1)),
            dict(id='tmrw',a=Wt('d6','tomorrow')-0.05,b=E('d6',0.3)),
            dict(id='ask',a=Wt('c5','remember')-0.1,b=E('c5',0.3))]
P['zoom']=[dict(a=A('d2'),b=E('d2'),z=1.10),dict(a=A('d5'),b=E('d5'),z=1.08),dict(a=A('c4'),b=E('c4'),z=1.06)]
S=[('swipe',A('c1',0.3),0.5),('thud',P['full'][0]['k'][0],0.9),('pop',P['full'][0]['k'][1],0.4),('pop',P['full'][0]['k'][2],0.4),
   ('pop',P['scene'][2]['a'],0.5),('qwhoosh',P['full'][1]['a']-0.15,0.5)]+[('pop',t,0.4) for t in P['full'][1]['k'][:4]]+[('thud',P['full'][1]['k'][4],0.8)]
S+=[('pop',t,0.35) for t in P['scene'][3]['k'][:3]]
S+=[('drumroll',DR,1.0),('womp',WOMP,1.0),('thud',WOMP+0.1,0.7),('thud',P['scene'][6]['a'],0.8),('pop',P['scene'][7]['a'],0.45)]
P['sfx']=[dict(f=f,t=round(t,3),v=v) for f,t,v in S]
P['seg']={k:[v['t0'],v['t1']] for k,v in T.items()}; P['TOTAL']=TOTAL
json.dump(P,open('work/plan.json','w'),indent=1); print('ok',len(S),'sfx; DROP',DROP,'BACK',BACK,'DR',DR,'PLAN',PLAN,'WOMP',WOMP)
for w in P['full']+P['scene']: print(w['id'],w['a'],w['b'],w.get('k'))
