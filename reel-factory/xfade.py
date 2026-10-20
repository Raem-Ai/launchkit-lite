import subprocess,json,pathlib,sys
REDO=set(sys.argv[1:])
W=pathlib.Path('work'); X=W/'xf'; X.mkdir(exist_ok=True)
T=json.load(open(W/'timeline.json'))['TL']; d=0.4
src={'intro':'intro.mp4','become':'hf/become.mp4'}
vf0='scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30'
def run(c): subprocess.run(['ffmpeg','-loglevel','error','-y']+c,check=True)
enc=['-c:v','libx264','-preset','veryfast','-crf','16','-pix_fmt','yuv420p','-an']
for s in T:
    k=s['k']; D=s['t1']-s['t0']; v=src.get(k,f'synced/{k}.mp4')
    VD=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',v]).decode())
    if k in REDO or not (X/f'ext_{k}.mp4').exists(): run(['-i',v,'-vf',vf0+f',tpad=stop_mode=clone:stop_duration={max(0,D+d-VD)+d+0.2:.3f}','-t',f'{D+d:.3f}']+enc+[str(X/f'ext_{k}.mp4')])
HARD={'c1','d2'}
parts=[]
for i,s in enumerate(T):
    k=s['k']; D=s['t1']-s['t0']; st=d if (i>=2 and k not in HARD) else 0
    if i>=2 and k not in HARD:
        p=T[i-1]['k']; Dp=T[i-1]['t1']-T[i-1]['t0']
        if k in REDO or p in REDO: run(['-ss',f'{Dp:.3f}','-i',str(X/f'ext_{p}.mp4'),'-i',str(X/f'ext_{k}.mp4'),'-filter_complex',
             f'[0:v]trim=0:{d},setpts=PTS-STARTPTS[a];[1:v]trim=0:{d},setpts=PTS-STARTPTS[b];[a][b]xfade=transition=fade:duration={d}:offset=0,fps=30[v]',
             '-map','[v]','-t',f'{d}']+enc+[str(X/f'tr_{k}.mp4')])
        parts.append(f'tr_{k}.mp4')
    if k in REDO: run(['-ss',f'{st:.3f}','-i',str(X/f'ext_{k}.mp4'),'-t',f'{D-st:.3f}','-vf','fps=30']+enc+[str(X/f'body_{k}.mp4')])
    parts.append(f'body_{k}.mp4')
(X/'list.txt').write_text('\n'.join(f"file '{p}'" for p in parts))
run(['-f','concat','-safe','0','-i',str(X/'list.txt'),'-vf','tpad=stop_mode=clone:stop_duration=3.5','-c:v','libx264','-preset','veryfast','-crf','16','-pix_fmt','yuv420p',str(W/'video_xf.mp4')])
print(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',str(W/'video_xf.mp4')]).decode())
