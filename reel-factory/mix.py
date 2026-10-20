import json,subprocess
T=json.load(open('work/timeline.json')); TL={x['k']:x for x in T['TL']}; TOTAL=json.load(open('work/total.json'))
P=json.load(open('work/plan.json'))
B=TL['become']['t0']; BE=TL['become']['t1']; C1=TL['c1']['t0']
DROP,BACK,DR,MUS2=P['DROP'],P['BACK'],P['DR'],P['MUS2']
S='sfx/'
ins=['-i','work/base_pad.mov']; fc=[]; mix=[]; N=[1]
def add(path,label,filt):
    ins.extend(['-i',path]); i=N[0]; N[0]+=1; fc.append(f'[{i}:a]{filt}[{label}]'); mix.append(f'[{label}]')
AF='aformat=sample_rates=48000:channel_layouts=stereo'
def music(label,a,b,vol,fin,fout,off=0):
    L=b-a; add(S+'marimba_long.mp3',label,f"{AF},atrim={off}:{off+L},asetpts=PTS-STARTPTS,volume={vol},afade=t=in:d={fin},afade=t=out:st={max(0,L-fout)}:d={fout},adelay={int(a*1000)}|{int(a*1000)}")
# marimba bed in three windows: desk → DROP (hard stop) · BACK → drumroll · close → end
music('m1',C1-0.3,DROP,0.34,1.0,0.04)
music('m2',BACK,DR-0.15,0.34,0.6,0.5,off=DROP-(C1-0.3))
music('m3',MUS2,TOTAL,0.34,0.8,1.5,off=40)
# typing loop while the robot types: from the becoming's end to the DROP, and again under the close
def typing(label,a,b,vol):
    L=b-a; add(S+'typing.mp3',label,f"{AF},aloop=loop=-1:size=2e9,atrim=0:{L},asetpts=PTS-STARTPTS,volume={vol},afade=t=in:d=0.3,afade=t=out:st={max(0,L-0.15)}:d=0.15,adelay={int(a*1000)}|{int(a*1000)}")
typing('ty1',BE-0.2,DROP,0.30)
# suspense under the strategy drop: boom on the cut, low drone bed until the music returns
add(S+'boom.mp3','boom',f"{AF},volume=0.45,adelay={int(DROP*1000)}|{int(DROP*1000)}")
L=BACK-DROP+0.4
for nm,off,vol in [('droneA',0.1,0.4),('droneB',4.7,0.4)]:
    LL=L-off; add(S+'drone.mp3',nm,f"{AF},aloop=loop=-1:size=2e9,atrim=0:{LL},asetpts=PTS-STARTPTS,volume={vol},afade=t=in:d=0.4,afade=t=out:st={LL-0.8}:d=0.8,adelay={int((DROP+off)*1000)}|{int((DROP+off)*1000)}")
typing('ty2',TL['c5']['t0']+1.0,TOTAL-3.2,0.22)
add(S+'whoosh.mp3','wh',f"{AF},volume=0.9,adelay={int((B+0.9-2.4)*1000)}|{int((B+0.9-2.4)*1000)}")
add(S+'sparkle.mp3','sp',f"{AF},volume=0.7,adelay={int((B+1.0)*1000)}|{int((B+1.0)*1000)}")
for j,c in enumerate(P['sfx']):
    add(S+c['f']+'.mp3',f'cue{j}',f"{AF},volume={c['v']},adelay={int(c['t']*1000)}|{int(c['t']*1000)}")
fc.append(f'[0:a]{AF},asplit=2[vo][sc]')
fc.append(f"{''.join(mix)}amix=inputs={len(mix)}:normalize=0:duration=longest,atrim=0:{TOTAL}[fx]")
fc.append('[fx][sc]sidechaincompress=threshold=0.06:ratio=2.5:attack=30:release=600[duck]')
fc.append('[vo][duck]amix=inputs=2:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11,alimiter=limit=0.95[aout]')
subprocess.run(['ffmpeg','-loglevel','error','-y',*ins,'-filter_complex',';'.join(fc),'-map','[aout]','-ar','48000','-t',str(TOTAL),'work/mix.wav'],check=True)
print('mix ok')
