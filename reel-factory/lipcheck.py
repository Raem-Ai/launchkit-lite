"""lipcheck.py video.mp4 line.wav [x y w h]  -> mouth-motion vs speech timing score.
Mouth motion = frame-to-frame change inside a face crop (1440x2560 source coords). Prints per-0.2s bars so you can SEE the offset."""
import sys,subprocess,numpy as np,wave
vid,aud=sys.argv[1:3]; crop=sys.argv[3:7] if len(sys.argv)>6 else None
def energy(p):
    subprocess.run(['ffmpeg','-loglevel','error','-y','-i',p,'-ac','1','-ar','16000','/tmp/_lc.wav'],check=True)
    w=wave.open('/tmp/_lc.wav'); a=np.frombuffer(w.readframes(w.getnframes()),np.int16).astype(float)
    h=1600; e=np.array([np.sqrt(np.mean(a[i:i+h]**2)) for i in range(0,len(a)-h,h)]); return e/(e.max()+1e-9)
def motion(p):
    vf='fps=10'+(f',crop={crop[2]}:{crop[3]}:{crop[0]}:{crop[1]}' if crop else '')+',scale=96:96,format=gray'
    raw=subprocess.run(['ffmpeg','-loglevel','error','-i',p,'-vf',vf,'-f','rawvideo','-'],capture_output=True,check=True).stdout
    fr=np.frombuffer(raw,np.uint8).reshape(-1,96,96).astype(float); d=np.abs(np.diff(fr,axis=0)).mean(axis=(1,2)); return d/(d.max()+1e-9)
e=energy(aud); m=motion(vid); L=min(len(e),len(m)); e,m=e[:L],m[:L]
best=max(((lag,np.corrcoef(np.roll(m,lag)[abs(lag):],e[abs(lag):])[0,1]) for lag in range(-10,11)),key=lambda x:x[1])
print(f'best lag {best[0]/10:+.1f}s corr {best[1]:.2f}  (lag>0 = mouth moves AFTER audio)')
bar=lambda v:'#'*int(v*20)
for i in range(0,L,2): print(f'{i/10:4.1f}s audio {bar(e[i]):20s} mouth {bar(m[i])}')
