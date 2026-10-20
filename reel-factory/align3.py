import numpy as np, wave, subprocess, sys
def load(p):
    subprocess.run(['ffmpeg','-loglevel','error','-y','-i',p,'-vn','-ac','1','-ar','16000','/tmp/_a.wav'],check=True)
    w=wave.open('/tmp/_a.wav'); return np.frombuffer(w.readframes(w.getnframes()),np.int16).astype(float)
def phrases(a,h=320,thr=0.06,gap=7,sr=16000):
    e=np.array([np.sqrt(np.mean(a[i:i+h]**2)) for i in range(0,len(a)-h,h)]); e/=e.max()+1e-9
    segs=[];s=None;last=-99
    for i,v in enumerate(e>thr):
        if v:
            if s is None: s=i
            last=i
        elif s is not None and i-last>gap: segs.append([s*h/sr,(last+1)*h/sr]); s=None
    if s is not None: segs.append([s*h/sr,(last+1)*h/sr])
    return [x for x in segs if x[1]-x[0]>0.15]
def merge_to(P,n):
    P=[p[:] for p in P]
    while len(P)>n:
        g=[P[i+1][0]-P[i][1] for i in range(len(P)-1)]; k=int(np.argmin(g)); P[k][1]=P[k+1][1]; del P[k+1]
    return P
def atempo(x):
    f=[]
    while x>2.0: f.append('atempo=2.0'); x/=2.0
    while x<0.5: f.append('atempo=0.5'); x/=0.5
    f.append(f'atempo={x:.5f}'); return ','.join(f)
def run(vid,ours,out):
    av=load(vid); ao=load(ours); P=phrases(av); Q=phrases(ao)
    n=max(1,min(len(P),len(Q))); P=merge_to(P,n); Q=merge_to(Q,n)
    ODUR=len(ao)/16000
    # chunk boundaries = midpoints of gaps (ours: covers whole file, nothing dropped)
    qb=[0.0]+[(Q[i][1]+Q[i+1][0])/2 for i in range(n-1)]+[ODUR]
    # target boundaries in video time: start a little before first mouth move, mid-gaps, end after last
    lead=Q[0][0]; tail=ODUR-Q[-1][1]
    pb=[max(0,P[0][0]-lead)]+[(P[i][1]+P[i+1][0])/2 for i in range(n-1)]+[P[-1][1]+tail]
    fc=[];parts=[]
    if pb[0]>0.005: fc.append(f"anullsrc=r=44100:cl=mono,atrim=0:{pb[0]:.3f}[s]"); parts.append('[s]')
    for k in range(n):
        src=qb[k+1]-qb[k]; dst=max(0.05,pb[k+1]-pb[k]); r=src/dst
        r=min(max(r,0.75),1.35)   # keep the voice natural; never chop words
        fc.append(f"[0:a]atrim={qb[k]:.3f}:{qb[k+1]:.3f},asetpts=PTS-STARTPTS,{atempo(r)}[p{k}]"); parts.append(f'[p{k}]')
    fc.append(''.join(parts)+f"concat=n={len(parts)}:v=0:a=1[o]")
    subprocess.run(['ffmpeg','-loglevel','error','-y','-i',ours,'-filter_complex',';'.join(fc),'-map','[o]','-ac','1','-ar','44100',out],check=True)
    d=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',out]).decode())
    return n,ODUR,d
if __name__=='__main__':
    print(run(*sys.argv[1:4]))
