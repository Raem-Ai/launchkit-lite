import json,subprocess,numpy as np
from faster_whisper import WhisperModel
T={x['k']:x for x in json.load(open('work/timeline.json'))['TL']}
m=WhisperModel('small.en',device='cpu',compute_type='int8')
hint="Claude, Etsy, Gumroad, GitHub. Names and numbers your script uses go here; it helps the transcript spell them right."
files={'intro':'intro.mp4'}
for n in ['c1','d1','c2','d2','d3a','d3b','d3c','c3','d4','d5','c4','d6','c5']: files[n]=f'synced/{n}.wav'
W=[]
for k,f in files.items():
    raw=subprocess.run(['ffmpeg','-loglevel','error','-i',f,'-ac','1','-ar','16000','-f','s16le','-'],capture_output=True,check=True).stdout
    a=np.frombuffer(raw,np.int16).astype(np.float32)/32768
    segs,_=m.transcribe(a,word_timestamps=True,initial_prompt=hint,vad_filter=False)
    W+=[dict(text=w.word.strip(),start=round(w.start+T[k]['t0'],3),end=round(w.end+T[k]['t0'],3)) for s in segs for w in s.words]
out=[];i=0
NUM={'four':'4','six':'6','two':'2'}
while i<len(W):
    w=W[i]; t=w['text']; low=t.lower().rstrip('!,.?'); p=t[len(low):] if t.lower().startswith(low) else ''
    if t=='Ho': t='Oh'
    if low in NUM and w['start']>T['become']['t1']: t=NUM[low]+t[len(low):]
    if t=='$10' and i+1<len(W) and W[i+1]['text'].startswith(',000'): out.append(dict(text='$10,000.',start=w['start'],end=W[i+1]['end'])); i+=2; continue
    out.append(dict(text=t,start=w['start'],end=w['end'])); i+=1
json.dump(out,open('work/words.json','w'),indent=0)
print(len(out),'words'); print(' '.join(w['text'] for w in out))
