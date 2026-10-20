"""For each shot: find speech in the clip's OWN audio (that's what the mouth was animated to),
cut the video from (speech_start - lead) and write synced/<k>.wav = that audio from the same point to speech_end+0.3.
Lip-sync is preserved because video and audio are cut at the identical time."""
import subprocess,json,sys
from align3 import load,phrases
LEAD={'c1':0.9,'d2':0.5,'d4':0.4,'d5':0.5}
MINLEAD=0.25
out={}
for k in ['c1','d1','c2','d2','d3a','d3b','d3c','c3','d4','d5','c4','d6','c5']:
    v=f'hf/{k}.mp4'
    try: a=load(v)
    except Exception as e: print(k,'no video yet'); continue
    P=phrases(a,thr=0.05)
    if not P: print(k,'NO SPEECH FOUND'); continue
    s,e=P[0][0],P[-1][1]
    lead=min(s,LEAD.get(k,MINLEAD)); t0=max(0,s-lead); t1=e+0.3
    VD=len(a)/16000
    subprocess.run(['ffmpeg','-loglevel','error','-y','-ss',f'{t0:.3f}','-i',v,'-t',f'{min(t1,VD)-t0:.3f}','-vn','-ac','1','-ar','44100',f'synced/{k}.wav'],check=True)
    subprocess.run(['ffmpeg','-loglevel','error','-y','-ss',f'{t0:.3f}','-i',v,'-an','-c:v','libx264','-preset','veryfast','-crf','14',f'synced/{k}.mp4'],check=True)
    out[k]=dict(t0=round(t0,3),speech=[round(s,3),round(e,3)],clip=round(VD,3),n=len(P))
    print(k,out[k])
json.dump(out,open('synced/cuts.json','w'),indent=1)
