import json,subprocess,sys
P=json.load(open('work/plan.json')); TOTAL=P['TOTAL']
OUT=sys.argv[1] if len(sys.argv)>1 else 'out/reel.mp4'
DROP=P['DROP']
E=lambda x:f"(1-pow(1-clip({x},0,1),3))"
sat=f"1-0.45*between(t,{DROP},{DROP+0.8})*(1-clip((t-{DROP+0.4})/0.4,0,1))"
bri=f"-0.07*between(t,{DROP},{DROP+0.8})"
Z="1"+''.join(f"+{z['z']-1}*{E(f'(t-{z['a']})/({z['b']-z['a']})')}*(1-{E(f'(t-{z['b']})/0.45')})" for z in P['zoom'])
fc=f"[0:v]hue=s='{sat}',eq=brightness='{bri}':eval=frame,scale=w='2*trunc(540*({Z}))':h='2*trunc(960*({Z}))':eval=frame,crop=1080:1920:'(iw-1080)/2':'(ih-1920)/2'[g0];[1:v]format=rgba[ov];[g0][ov]overlay=0:0:shortest=1,format=yuv420p[v]"
subprocess.run(['ffmpeg','-y','-loglevel','error','-i','work/video_xf.mp4','-framerate','30','-i','ovl/f%05d.png','-i','work/mix.wav','-filter_complex',fc,
  '-map','[v]','-map','2:a','-t',str(TOTAL),'-c:v','libx264','-preset','medium','-crf','21','-c:a','aac','-b:a','192k','-movflags','+faststart',OUT],check=True)
print('done',OUT)
