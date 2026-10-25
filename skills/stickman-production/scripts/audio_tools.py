"""Outer-silence trimming preserves original PCM bytes, channel layout and speed."""
import array,math,sys,wave

def trim_wav(source,target):
    with wave.open(str(source),'rb') as audio:
        params=audio.getparams();payload=audio.readframes(params.nframes)
    if params.sampwidth!=2 or params.comptype!='NONE':raise ValueError('Expected uncompressed PCM16 WAV')
    samples=array.array('h');samples.frombytes(payload)
    if sys.byteorder!='little':samples.byteswap()
    window_frames=max(1,params.framerate//200);window=window_frames*params.nchannels
    energies=[math.sqrt(sum(x*x for x in samples[k:k+window])/len(samples[k:k+window])) for k in range(0,len(samples),window)]
    if not energies:raise ValueError('Empty WAV')
    threshold=max(.005*32768,max(energies)*.028);active=[i for i,e in enumerate(energies) if e>threshold]
    if not active:raise ValueError('Silent take')
    lo=max(0,active[0]*window_frames-round(.03*params.framerate))
    hi=min(params.nframes,(active[-1]+1)*window_frames+round(.08*params.framerate))
    stride=params.sampwidth*params.nchannels
    with wave.open(str(target),'wb') as output:
        output.setparams(params);output.writeframes(payload[lo*stride:hi*stride])
    return {'trim_start':lo/params.framerate,'trim_end':hi/params.framerate,'duration':(hi-lo)/params.framerate,'speech_speed':1}
