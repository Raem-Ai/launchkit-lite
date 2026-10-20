"""Synthesize a sad-trombone "womp womp" sting: python3 sfx_womp.py womp.wav"""
import sys,numpy as np, scipy.io.wavfile as w
sr=44100
def note(f0,f1,dur,vib=5.5,depth=0.012):
    t=np.arange(int(sr*dur))/sr; f=f0*(f1/f0)**(t/dur); ph=2*np.pi*np.cumsum(f)/sr; x=np.zeros_like(t)
    for k in range(1,9): x+=np.sin(k*ph*(1+depth*np.sin(2*np.pi*vib*t)))/k**1.2
    env=np.minimum(1,t/0.06)*np.minimum(1,(dur-t)/0.12); wah=0.55+0.45*np.sin(np.pi*np.minimum(t/dur,1)); return x*env*wah
gap=np.zeros(int(sr*0.05))
y=np.concatenate([note(233,233,0.42),gap,note(220,220,0.42),gap,note(207.65,207.65,0.42),gap,note(196,170,1.3,vib=6.5,depth=0.02)])
y=y/np.max(np.abs(y))*0.8; w.write(sys.argv[1] if len(sys.argv)>1 else 'womp.wav',sr,(y*32767).astype(np.int16))
