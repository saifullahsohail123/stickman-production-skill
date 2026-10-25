"""Original 3s VectorCraft wave/blink integration demo, without a cloned voice."""
import math,wave
import av,numpy as np
from PIL import Image
from production import app

def render_demo(cfg,root,data):
    if (root/'native/demo.vectorcraft').exists():raise FileExistsError('Demo already exists; use a fresh test workspace')
    if (data['format']['width'],data['format']['height'],data['format']['fps'],data['format']['duration_frames'])!=(640,360,24,72):
        raise ValueError('This integration example is 640x360, 24fps, 72 frames')
    ink='#34312e';teal='#5a9287'
    with app(cfg,root,'vectorcraft') as v:
        def command(command_id,**params):return v.call('run_command',command=command_id,params=params)
        def line(d,color=ink,width=5):return v.call('draw_path',d=d,fill='none',stroke=color,strokeWidth=width,cap='round',join='round')['id']
        def ellipse(x,y,w,h,fill='white',stroke=ink,width=4):return v.call('draw_shape',shape='ellipse',x=x,y=y,width=w,height=h,fill=fill,stroke=stroke,strokeWidth=width)['id']
        def group(ids,name):
            i=command('object.group',ids=ids)['id'];command('object.setProps',ids=[i],name=name);return i
        command('file.new',width=640,height=360,backgroundContents='white')
        v.call('draw_shape',shape='rectangle',x=0,y=0,width=640,height=360,fill='#eadbc3',stroke='none',strokeWidth=0)
        v.call('draw_shape',shape='rectangle',x=0,y=295,width=640,height=65,fill='#a9ba9c',stroke='none',strokeWidth=0)
        line('M292 247 L284 292 L270 295 M326 247 L337 292 L352 295')
        line('M282 188 L261 220 L265 247')
        line('M338 188 L365 190')
        forearm=group([line('M365 190 L365 149'),ellipse(360,139,10,11,ink,ink,1)],'Waving forearm')
        v.call('draw_path',d='M284 178 Q309 172 336 178 L342 247 Q308 255 277 247 Z',fill='#fffdf6',stroke=ink,strokeWidth=4,cap='round',join='round')
        ellipse(258,65,102,105,'#fffdf6')
        v.call('draw_path',d='M283 178 L328 184 L319 207 L308 188 L285 187 Z',fill=teal,stroke=ink,strokeWidth=2,cap='round',join='round')
        open_eyes=group([ellipse(284,108,7,12,ink,ink,0),ellipse(327,108,7,12,ink,ink,0)],'Open eyes')
        blink=group([line('M281 114 L295 114',width=3),line('M324 114 L338 114',width=3)],'Blink eyes')
        line('M282 96 Q289 91 296 96 M324 96 Q331 91 338 96',width=3)
        line('M294 141 Q310 154 327 140',width=3)
        command('object.setProps',ids=[blink],visible=False)
        v.call('save_file',path=str(root/'native/demo.vectorcraft'))
        for frame in range(72):
            v.call('open_file',path=str(root/'native/demo.vectorcraft'))
            angle=math.radians(18*math.sin(frame/24*7));c,s=math.cos(angle),math.sin(angle);x,y=365,190
            steps=[{'id':'object.transform','params':{'ids':[forearm],'matrix':[c,s,-s,c,x-c*x+s*y,y-s*x-c*y]}},
                   {'id':'object.setProps','params':{'ids':[open_eyes],'visible':frame not in [30,31,32]}},
                   {'id':'object.setProps','params':{'ids':[blink],'visible':frame in [30,31,32]}}]
            v.call('command_batch',steps=steps,stop_on_error=True)
            v.call('export',path=str(root/'frames'/f'{frame:04}.png'),scale=1,options={'background':'white'})
            if frame==24:v.call('save_file',path=str(root/'native/pose-wave.vectorcraft'))
    with av.open(str(root/'shots/s1.mp4'),'w') as output:
        stream=output.add_stream('libx264',rate=24);stream.width=640;stream.height=360;stream.pix_fmt='yuv420p';stream.options={'crf':'18','preset':'fast'}
        for frame in range(72):
            with Image.open(root/'frames'/f'{frame:04}.png') as image:
                for packet in stream.encode(av.VideoFrame.from_image(image.convert('RGB'))):output.mux(packet)
        for packet in stream.encode():output.mux(packet)
    sr=48000;audio=np.zeros(3*sr)
    for at,pitch in [(.2,392),(.9,494),(1.6,587),(2.3,784)]:
        t=np.arange(round(.45*sr))/sr;signal=.065*np.sin(2*np.pi*pitch*t)*np.exp(-t*9)*(1-np.exp(-t*200));k=round(at*sr);audio[k:k+len(signal)]+=signal
    with wave.open(str(root/'audio/chimes.wav'),'wb') as out:
        out.setparams((1,2,sr,0,'NONE','not compressed'));out.writeframes((audio*32767).astype('<i2').tobytes())
    data['audio']=[{'file':'audio/chimes.wav','start':0,'name':'Original demo chimes'}]
    data['captions']=[{'start':.2,'end':2.8,'text':'One small victory.'}]
    print('Rendered 72 original VectorCraft frames; demo has no narration.')
