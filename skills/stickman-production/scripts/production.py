"""Agent-independent CLI. Core planning uses stdlib; media commands load extras."""
import argparse,json,math,shutil,wave
from pathlib import Path
from core import archive,clock,inside,read_json,validate,write_json
from mcp_stdio import MCP
from voicebox_api import Voicebox

ASSETS=Path(__file__).resolve().parents[1]/'assets'

def config(path):
    path=Path(path).resolve();data=read_json(path)
    root=(path.parent/data.get('workspace','.')).resolve()
    if not root.is_dir():raise FileNotFoundError('Initialize/configure an episode workspace first')
    return data,root

def app(cfg,root,name):
    env={'VECTORCRAFT_NO_PREFS':'1'} if name=='vectorcraft' else {'CONCAT_MCP_ROOTS':str(root)}
    return MCP(cfg[name+'_command'],root,name+'.log',cfg.get('request_timeout_seconds',90),env)

def doctor(cfg,root):
    report={}
    for name in ['vectorcraft','concat']:
        try:
            with app(cfg,root,name) as client:
                catalog=client.request('tools/list',{})['tools']
                report[name]={'available':True,'tools':[q['name'] for q in catalog]}
                write_json(root/'logs'/(name+'-tools.json'),catalog)
        except Exception as e:report[name]={'available':False,'reason':str(e)}
    try:
        vb=Voicebox(cfg['voicebox_url']);health=vb.json('/health');models=vb.json('/models/status')
        report['voicebox']={'available':True,'health':health,'models':models}
    except Exception as e:report['voicebox']={'available':False,'reason':str(e)}
    write_json(root/'doctor.json',report);print(json.dumps(report,indent=2))

def make_clock(root,data):
    takes=[]
    for line in data.get('lines',[]):
        path=inside(root,'audio/'+line['id']+'-edit.wav')
        if not path.exists():path=inside(root,'audio/'+line['id']+'.wav')
        with wave.open(str(path),'rb') as audio:duration=audio.getnframes()/audio.getframerate()
        takes.append(dict(line,duration=duration,file=path.relative_to(root).as_posix()))
    result=clock(takes,data.get('lead_seconds',0),data.get('tail_seconds',.5))
    write_json(root/'clock.json',result)
    print(json.dumps(result,ensure_ascii=False,indent=2))

def assemble(cfg,root,data,reexport=False):
    project=root/'concat-edit';render=root/'render';render.mkdir(exist_ok=True)
    fmt=data['format'];log=[]
    with app(cfg,root,'concat') as client:
        def call(tool,**args):
            value=client.call(tool,**args);log.append(dict(tool=tool,args=args,result=value));return value
        if reexport:call('project_open',path=str(project))
        else:
            if (project/'concat.json').exists():raise FileExistsError('Existing edit: use --reexport, or a new workspace/revision')
            call('project_create',location=str(root),name=project.name,
                 video={'width':fmt['width'],'height':fmt['height'],'rateNum':fmt['fps'],'rateDen':1})
            for shot in data['shots']:
                file=inside(root,shot['file'])
                if not file.is_file():raise FileNotFoundError(file)
                media=call('media_import',path=str(project),file=str(file))['createdId']
                clip=call('clip_add',path=str(project),mediaId=media,trackId='T1',start=shot['start_frame']/fmt['fps'])['createdId']
                call('clip_update',path=str(project),clipId=clip,patch={'name':shot['id']})
                camera=shot.get('camera',{})
                for at,key in [(0,'start_scale'),(1,'end_scale')]:
                    if key in camera:call('keyframe_set',path=str(project),clipId=clip,property='scale',at=at,value=camera[key])
            for layer in data.get('audio',[]):
                track=call('track_add',path=str(project))['createdId']
                media=call('media_import',path=str(project),file=str(inside(root,layer['file'])))['createdId']
                clip=call('clip_add',path=str(project),mediaId=media,trackId=track,start=layer.get('start',0))['createdId']
                call('clip_update',path=str(project),clipId=clip,patch={'name':layer.get('name','Audio'),'volume':layer.get('volume',1)})
            cues=data.get('captions',[])
            if cues:
                call('captions_add',path=str(project),captions=cues,offsetY=data.get('caption_offset_y',.25),style=data.get('caption_style',{}))
                state=call('timeline_read',path=str(project))['timeline'];top=state['tracks'][-1]['id']
                call('clips_move',path=str(project),moves=[{'clipId':q['id'],'trackId':top,'start':q['start']} for q in state['clips'] if q['kind']=='text'])
            # Integer starts prevent accumulated source-probe duration drift.
            state=call('timeline_read',path=str(project))['timeline']
            clips=sorted([q for q in state['clips'] if q['kind']=='video'],key=lambda q:q['start'])
            for clip,shot in zip(clips,data['shots']):
                duration=(shot['end_frame']-shot['start_frame'])/fmt['fps']
                if abs(clip['duration']-duration)>1e-8:
                    call('clip_trim',path=str(project),clipId=clip['id'],edge='end',delta=duration-clip['duration'])
            call('project_save',path=str(project))
        write_json(root/'concat-state.json',call('project_get',path=str(project)))
        job=call('export_start',path=str(project),output=str(render/'current.mp4'),crf=18,preset='fast',codec='h264')
        for _ in range(180):
            status=call('export_wait',job=job['job'],timeoutSeconds=20)
            if status.get('state') in ['done','failed','cancelled']:break
        else:raise TimeoutError('Export deadline reached; inspect existing job, do not duplicate the edit')
        if status['state']!='done':raise RuntimeError(status)
        write_json(root/'export-result.json',status)
    write_json(root/'logs/concat-assembly.json',log)

def verify(root,data,deliver=False):
    import av,numpy as np
    source=root/'render/current.mp4';fmt=data['format'];wanted={0,fmt['duration_frames']//2,fmt['duration_frames']-1}
    qc=root/'qc';qc.mkdir(exist_ok=True);count=0;peak=None
    with av.open(str(source)) as media:
        stream=media.streams.video[0]
        report={'duration_seconds':media.duration/1e6,'width':stream.width,'height':stream.height,'fps':str(stream.average_rate)}
        if (stream.width,stream.height)!=(fmt['width'],fmt['height']):raise ValueError('Wrong export resolution')
        if abs(float(stream.average_rate)-fmt['fps'])>1e-8:raise ValueError('Wrong export frame rate')
        for frame in media.decode(video=0):
            if count in wanted:frame.to_image().save(qc/f'frame-{count:06}.png')
            count+=1
    if count!=fmt['duration_frames']:raise ValueError('Wrong decoded frame count')
    if abs(report['duration_seconds']-count/fmt['fps'])>.05:raise ValueError('Wrong export duration')
    with av.open(str(source)) as media:
        if media.streams.audio:
            peak=max((float(np.max(np.abs(f.to_ndarray()))) for f in media.decode(audio=0)),default=0)
            if data.get('audio') and peak==0:raise ValueError('Expected audio but export is silent')
    report.update(decoded_frames=count,audio_peak=peak,caption_visibility='inspect decoded frames',
        lip_sync='requires moving playback and listening',full_audio_audition_claimed=False,status='technical_checks_passed')
    write_json(root/'verification.json',report)
    if deliver:report['delivery']=str(archive(source,root/'deliveries',data))
    print(json.dumps(report,indent=2))

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command',choices=['init','doctor','validate','profiles','generate','clock','demo','assemble','verify'])
    parser.add_argument('--workspace',type=Path)
    parser.add_argument('--config',type=Path)
    parser.add_argument('--episode',default='episode.json')
    parser.add_argument('--reexport',action='store_true');parser.add_argument('--deliver',action='store_true')
    args=parser.parse_args()
    if args.command=='init':
        if args.workspace is None:parser.error('init requires --workspace')
        root=args.workspace.resolve();root.mkdir(parents=True,exist_ok=False)
        for name in ['native','frames','shots','audio','logs']:(root/name).mkdir()
        shutil.copy2(ASSETS/'config.example.json',root/'config.local.json')
        shutil.copy2(ASSETS/'episode.example.json',root/'episode.json')
        print(root);return
    if args.config is None:parser.error('This command requires --config')
    cfg,root=config(args.config)
    if args.command=='doctor':doctor(cfg,root);return
    if args.command=='profiles':print(json.dumps(Voicebox(cfg['voicebox_url']).json('/profiles'),ensure_ascii=False,indent=2));return
    data=validate(read_json(inside(root,args.episode)))
    if args.command=='validate':print('Manifest is valid')
    elif args.command=='generate':
        from audio_tools import trim_wav
        vb=Voicebox(cfg['voicebox_url'],cfg.get('request_timeout_seconds',90))
        for line in data.get('lines',[]):
            key=data['cast'][line['speaker']]['voice_key'];original=vb.generate(root,line,cfg['voices'][key])
            edit=original.with_name(original.stem+'-edit.wav')
            metadata=trim_wav(original,edit);write_json(original.with_name(original.stem+'-trim.json'),metadata)
    elif args.command=='clock':make_clock(root,data)
    elif args.command=='demo':
        from vector_demo import render_demo
        render_demo(cfg,root,data);write_json(inside(root,args.episode),data)
    elif args.command=='assemble':assemble(cfg,root,data,args.reexport)
    elif args.command=='verify':verify(root,data,args.deliver)

if __name__=='__main__':main()
