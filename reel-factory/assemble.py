import subprocess,json,pathlib
W=pathlib.Path('work'); W.mkdir(exist_ok=True)
def dur(p): return float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',p]).decode())
NAMES=['c1','d1','c2','d2','d3a','d3b','d3c','c3','d4','d5','c4','d6','c5']
seq=[('intro','intro.mp4','own'),('become','hf/become.mp4',None)]+[(n,f'synced/{n}.mp4',f'synced/{n}.wav') for n in NAMES]
vf0='scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30'
TL=[];t=0;lst=[]
for k,v,a in seq:
    VD=dur(v); D=VD; vf=vf0
    if a and a!='own':
        AD=dur(a); D=min(VD,AD+0.45); D=max(D,AD+0.30)
        if D>VD: vf+=f',tpad=stop_mode=clone:stop_duration={D-VD+0.1:.3f}'
    vf+=',format=yuv420p'; out=W/f'{k}.mov'
    if a=='own': cmd=['ffmpeg','-loglevel','error','-y','-i',v,'-t',f'{D:.3f}','-vf',vf,'-ac','2','-ar','48000']
    elif a: cmd=['ffmpeg','-loglevel','error','-y','-i',v,'-i',a,'-map','0:v','-map','1:a','-t',f'{D:.3f}','-vf',vf,'-af','apad','-ac','2','-ar','48000']
    else: cmd=['ffmpeg','-loglevel','error','-y','-i',v,'-f','lavfi','-i','anullsrc=r=48000:cl=stereo','-map','0:v','-map','1:a','-t',f'{D:.3f}','-vf',vf]
    subprocess.run(cmd+['-c:v','libx264','-preset','veryfast','-crf','17','-c:a','pcm_s16le',str(out)],check=True)
    TL.append(dict(k=k,t0=round(t,3),t1=round(t+D,3),ad=round(dur(a),3) if a and a!='own' else None)); t+=D; lst.append(f"file '{k}.mov'")
(W/'list.txt').write_text('\n'.join(lst))
subprocess.run(['ffmpeg','-loglevel','error','-y','-f','concat','-safe','0','-i',str(W/'list.txt'),'-c','copy',str(W/'base.mov')],check=True)
PAD=3.5; TOTAL=round(t+PAD,3)
subprocess.run(['ffmpeg','-loglevel','error','-y','-i',str(W/'base.mov'),'-vn','-af',f'apad=pad_dur={PAD}','-c:a','pcm_s16le',str(W/'base_pad.mov')],check=True)
json.dump(dict(TL=TL,TOTAL=round(t,3)),open(W/'timeline.json','w'),indent=1); json.dump(TOTAL,open(W/'total.json','w')); print('TOTAL',TOTAL)
for x in TL: print(x)
